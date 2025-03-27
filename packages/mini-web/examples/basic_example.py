import json

from mini_web.core import HTTPError, JsonResponse, MiniWeb, Request, Response

# 创建应用实例
app = MiniWeb()

# 基本路由 - 返回HTML响应
@app.route(r"/")
def index(request: Request) -> Response:
    return Response(body="<h1>欢迎使用 Mini Web 框架</h1><p>这是一个简单的Web框架示例</p>")

# 返回JSON响应
@app.route(r"/api/hello")
def hello(request: Request) -> Response:
    return JsonResponse(body={"message": "你好，世界！", "status": "success"})

# 处理POST请求
@app.route(r"/api/echo", method="POST")
def echo(request: Request) -> Response:
    try:
        # 解析请求体中的JSON数据
        data = json.loads(request.body)
        return JsonResponse(body={"echo": data, "received": True})
    except json.JSONDecodeError:
        return HTTPError(status_code=400, body={"error": "无效的JSON数据"})

# 自定义状态码和头信息
@app.route(r"/custom")
def custom_response(request: Request) -> Response:
    return Response(
        body="<h1>自定义响应</h1>",
        status_code=201,
        headers={"X-Custom-Header": "custom_value"},
    )

# 错误处理示例
@app.route(r"/error")
def error_demo(request: Request) -> Response:
    raise HTTPError(status_code=500, body={"error": "这是一个示例错误"})

if __name__ == "__main__":
    # 启动服务器
    print("启动 Mini Web 服务器示例...")  # noqa: T201
    app.run(host="localhost", port=8080)
