import asyncio
import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class Request:
    method: str
    headers: dict[str, str]
    path: str
    query: list[dict[str, list[str]]] = field(default_factory=list)
    body: str | None = None


@dataclass
class Response:
    body: str = ""
    status_code: int = field(default=200, kw_only=True)
    content_type: str = field(default="text/html", kw_only=True)
    headers: dict[str, str] = field(default_factory=dict, kw_only=True)

    def __post_init__(self):
        if isinstance(self.body, dict):
            self.body = json.dumps(self.body, ensure_ascii=False)
        self.headers["Content-Type"] = f"{self.content_type}; charset=utf-8"
        self.headers["Content-Length"] = str(len(self.body.encode("utf-8")))
        self.headers["Status"] = str(self.status_code)


@dataclass
class JsonResponse(Response):
    content_type: str = "application/json"


@dataclass
class HTTPError(Response, BaseException):
    status_code: int = 500
    content_type: str = "application/json"


class MiniWeb:
    route_table: list[tuple[re.Pattern, str, Callable]] = []

    def route(self, path: str, method: str = "GET"):
        def decorator(func):
            self.route_table.append((re.compile(path + "$"), method.upper(), func))
            return func

        return decorator

    def get_route_func(self, path: str, method: str) -> Callable:
        return next(
            (func for pattern, _method, func in self.route_table if pattern.match(path) and method.upper() == _method),
            None,
        )

    def parse_request(self, request_str: str) -> Request:
        lines = request_str.split("\r\n")
        method, path, _ = lines[0].split(" ")
        headers = {}
        for line in lines[1:]:
            if line == "":
                break
            key, value = line.split(": ", 1)
            headers[key] = value
        body = "\r\n".join(lines[len(headers) + 2 :])
        return Request(method=method, headers=headers, path=path, body=body)

    def build_response(self, response: Response) -> str:
        response_lines = [
            f"HTTP/1.1 {response.status_code} OK",
            *[f"{key}: {value}" for key, value in response.headers.items()],
            "",
            response.body,
        ]
        return "\r\n".join(response_lines)

    async def handle_request(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            request_data = await reader.readuntil(b"\r\n\r\n")
            request_str = request_data.decode()
            request = self.parse_request(request_str)
            if (content_length := request.headers.get("Content-Length")) and int(
                request.headers.get("Content-Length")
            ) > 0:
                request.body = (await reader.read(int(content_length))).decode()
            if route_func := self.get_route_func(request.path, request.method):
                response = route_func(request)
            else:
                response = HTTPError(body=json.dumps({"error": "Not Found"}, ensure_ascii=False), status_code=404)
        except HTTPError as e:
            response = e
        except Exception as e:  # noqa: BLE001
            response = HTTPError(status_code=500, body=json.dumps({"error": str(e)}, ensure_ascii=False))
        finally:
            response_str = self.build_response(response)
            writer.write(response_str.encode("utf-8"))
            await writer.drain()
            writer.close()

    async def start_server(self, host: str = "localhost", port: int = 8000):
        server = await asyncio.start_server(self.handle_request, host, port)
        async with server:
            await server.serve_forever()

    def run(self, host: str = "localhost", port: int = 8000):
        asyncio.run(self.start_server(host, port))
