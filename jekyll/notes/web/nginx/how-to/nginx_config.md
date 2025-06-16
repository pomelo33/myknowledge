---
tags:
- nginx
- how-to
title: Nginx Config
---

## 🧩 Nginx 配置文件结构理解（以生产环境为导向）

[TOC]

### 📁 一、配置结构概览（nginx.conf）
```nginx
# 全局块（global）
user  nginx;
worker_processes  auto;
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

# 事件块（events）
events {
    worker_connections  10240;
    use epoll;
    multi_accept on;
}

# HTTP 服务块（http）
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$request_time" "$upstream_response_time"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;

    gzip  on;

    # 虚拟主机配置
    include /etc/nginx/conf.d/*.conf;
}

```

### 📘 二、模块详解（重点模块 + 生产建议）
#### 1️⃣ server 配置虚拟主机
虚拟主机用于支持多个站点或服务实例（例如前后端、不同域名），一般按服务或项目拆分一个 server 块。
```nginx
server {
    listen 80;
    server_name www.example.com;

    root /var/www/example;
    index index.html index.htm;

    access_log /var/log/nginx/example.access.log main;
    error_log  /var/log/nginx/example.error.log warn;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://backend_api;
    }
}
```
💡 生产建议：
- listen + server_name 精确匹配域名，避免模糊匹配带来的性能浪费；
- access_log 分站点输出 便于排查问题；
- 多服务统一放入 /etc/nginx/conf.d/*.conf 模块化管理。
- 
#### 2️⃣ location 路由规则详解
用于定义 URI 路由逻辑：
```nginx
location = /exact { ... }             # 精确匹配
location ^~ /static/ { ... }          # 前缀匹配优先
location ~ \.php$ { ... }             # 正则匹配（区分大小写）
location /api/ { proxy_pass http://backend_api; }
```
💡 生产建议：
- 使用 location ^~ /static/ 避免正则消耗；
- 静态资源优先配置，减少后端压力；
- 避免使用多个复杂正则匹配，优先用前缀匹配优化性能。

#### 3️⃣ 静态资源服务与 MIME 类型配置
```nginx
location /assets/ {
    root /data/static;
    expires 30d;
    add_header Cache-Control "public";
}
```
- expires：设置浏览器缓存，减轻并发压力；
- add_header：可配合 CDN 控制中间缓存策略；
- /etc/nginx/mime.types：配置 MIME 映射，确保响应类型正确（例如 CSS、JS）。
💡 生产建议：
- 静态资源建议部署在独立 Nginx 实例或 CDN 前；
- gzip + expires + cache-control 组合压缩、缓存齐用。

#### 4️⃣ 日志配置与访问日志分析
```nginx
log_format main '$remote_addr [$time_local] "$request" $status '
                '$body_bytes_sent "$http_referer" "$http_user_agent" '
                '$request_time "$upstream_response_time"';

access_log /var/log/nginx/access.log main;
```
- $request_time：客户端请求总耗时；
- $upstream_response_time：后端服务响应时间；
- $status：状态码分析（500/404 异常追踪）；
💡 生产建议：
- 按天滚动日志 + logrotate 管理文件大小；
- 使用工具如 GoAccess、ELK 对日志可视化分析；
- 根据访问路径、状态码、IP 进行慢接口统计和限流配置。

### ⚙️ 三、性能调优建议（高并发环境）
```
worker_processes auto;
```
- 自动设为 CPU 核心数，处理并发请求性能最大化；
```
worker_connections 10240;
```
- 每个 worker 可同时连接的客户端数；
- 并发理论值 = worker_processes × worker_connections
```
use epoll;
```
- Linux 高效事件模型，适合高并发访问；
```
tcp_nopush / tcp_nodelay
```
- 控制 TCP 打包/传输策略，提高大包或小包性能；
```
keepalive_timeout 65;
```
- 设置连接保持时间，调优客户端连接重用；
  
### 🧯 生产常见问题与建议
| 场景             | 建议                                         |
| -------------- | ------------------------------------------ |
| **高并发场景响应变慢**  | 检查后端响应时间（`$upstream_response_time`），建议加缓存层 |
| **访问日志过大**     | 使用 `logrotate` 或按小时分目录切割                   |
| **CDN 缓存不生效**  | 检查是否正确配置了 `Cache-Control`、`Expires` 头      |
| **连接超时或拒绝连接**  | 增加 `worker_connections` 和 `ulimit -n` 系统参数 |
| **Nginx 启动报错** | 通常为配置文件格式错误，建议 `nginx -t` 先检查              |

### ✅ 小结：高质量生产级 Nginx 配置思路
1. 拆分模块（每个站点单独一个 conf.d/*.conf）
2. 明确资源类型路径、缓存策略；
3. 配置合理的负载均衡策略（如 least_conn、ip_hash）；
4. 日志结构化 + 数据化，辅助压测与调优；
5. 配置合理的连接数、内核参数、TCP 优化选项；
6. 定期灰度重启，避免长期运行引发连接泄露或缓慢增长问题

