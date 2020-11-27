分享提纲
## HTTP是什么
+ 基于tcp, 运行在7层上的通信协议
+ 用于客户端和服务端交换数据

## HTTP特点
+ 简单 -> 可以直接读懂
+ 可扩展 -> headers
+ 无状态 -> 可以有会话session

## HTTP使用指南
即restful api
### 请求方法
+ GET -> 获取资源
+ POST -> 创建资源
+ PUT -> 全量更新
+ DELETE -> 删除
+ PATCH -> 部分更新
+ ...
### HTTP状态码
+ 1xx -> 正在处理
+ 2xx -> 成功
+ 3xx -> 重定向
+ 4xx -> 客户端错误
+ 5xx -> 服务端错误
## [HTTP报文](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Messages)
demo--[requests](./demo_requests)


## web frame的作用
demo--[demo_web_frame](./demo_web_frame)
+ 解析http-> request, response
+ 会话
+ 路由
+ 模版
+ 提供快捷工具
  + 数据交互（ORM）
  + ...