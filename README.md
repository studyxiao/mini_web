# MINI Web Framework

> 学习一个简单的 Web 框架，使用 Python 编写。该框架支持路由、请求和响应处理。

## 功能

- 仅支持 WEB 核心功能
- 类型提示


## 框架设计图

### 类图

```mermaid
classDiagram
    class Request {
        +str method
        +dict[str, str] headers
        +str path
        +list query
        +str|None body
    }
    
    class Response {
        +str body
        +int status_code
        +str content_type
        +dict[str, str] headers
        +__post_init__()
    }
    
    class JsonResponse {
        +str content_type = "application/json"
    }
    
    class HTTPError {
        +int status_code = 500
        +str content_type = "application/json"
    }
    
    class MiniWeb {
        +list route_table
        +route(path, method)
        +get_route_func(path, method)
        +parse_request(request_str)
        +build_response(response)
        +handle_request(reader, writer)
        +start_server(host, port)
        +run(host, port)
    }
    
    Response <|-- JsonResponse
    Response <|-- HTTPError
    BaseException <|-- HTTPError
```

### 请求处理流程图

```mermaid
flowchart TD
    A[客户端请求] --> B[handle_request]
    B --> C[parse_request解析请求]
    C --> D[读取请求体]
    D --> E{查找路由函数}
    E -->|找到| F[执行路由函数]
    E -->|未找到| G[返回404错误]
    F --> H[构建响应]
    G --> H
    H --> I[发送响应]
    I --> J[关闭连接]
```

### 服务器启动流程

```mermaid
flowchart TD
    A[用户调用run方法] --> B[run]
    B --> C[asyncio.run]
    C --> D[start_server]
    D --> E[asyncio.start_server]
    E --> F[server.serve_forever]
    F -->|接收请求| G[handle_request]
```

### 请求-响应序列图

```mermaid
sequenceDiagram
    participant Client as 客户端
    participant Server as MiniWeb服务器
    participant Router as 路由系统
    participant Handler as 路由处理函数
    
    Client->>Server: HTTP请求
    Server->>Server: 解析请求(parse_request)
    Server->>Server: 读取请求体(如果有)
    Server->>Router: 查找路由(get_route_func)
    
    alt 找到匹配路由
        Router->>Handler: 调用处理函数
        Handler->>Server: 返回Response
    else 未找到路由
        Router->>Server: 返回404 HTTPError
    end
    
    Server->>Server: 构建响应(build_response)
    Server->>Client: 发送HTTP响应
    Server->>Server: 关闭连接
```

## 示例

```bash
uv run examples/basic_example.py
```


## 学习

- https://github.com/kadircancetin/MostMinimalWebFramework/tree/main
