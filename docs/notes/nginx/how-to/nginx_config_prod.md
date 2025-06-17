[TOC]
### ⚙️ 1.调优 Nginx 性能的实用建议（生产级）
以下是从并发性能、安全性、稳定性角度推荐的配置和调整项。
#### 🔧 1. 连接数与并发优化
```nginx
worker_processes auto;  # 核心数自动匹配
worker_rlimit_nofile 65535;

events {
    worker_connections 10240;  # 每个进程最大连接数
    use epoll;                 # Linux 高并发推荐模型
    multi_accept on;           # 一次性接受尽可能多的连接
}

```
系统层面还需配合修改：
```
ulimit -n 65535  # 提高文件描述符上限
```

#### 🚀 2. 网络性能优化
```nginx
sendfile        on;
tcp_nopush      on;
tcp_nodelay     on;
keepalive_timeout 65;
keepalive_requests 10000;
```
> 说明：
- tcp_nopush 配合 sendfile 减少网络数据碎片；
- tcp_nodelay 防止小包延迟；
- keepalive_requests 控制长连接的复用数量，提高并发响应效率。

#### 🌐 3. 压缩与缓存策略
```nginx
gzip on;
gzip_types text/plain application/json application/javascript text/css;
gzip_min_length 1k;
gzip_comp_level 6;
```
> 说明：
- 启用 Gzip 可压缩 HTML/JS/CSS 等，节省带宽；
- 不宜设置 gzip_comp_level 太高，否则 CPU 占用升高。

#### ⛑️ 4. 错误与异常保护
```nginx
limit_conn_zone $binary_remote_addr zone=addr:10m;
limit_conn addr 100;  # 限制单个 IP 并发连接数

limit_req_zone $binary_remote_addr zone=req_zone:10m rate=10r/s;
limit_req zone=req_zone burst=20;
```
> 说明：
- 防止单个 IP 发起海量请求造成服务阻塞;
- 对高频接口（如登录、支付）可单独限流。

#### 🧯 5. 健康检查机制（upstream + failover）
```nginx
upstream backend {
    server backend1 max_fails=3 fail_timeout=10s;
    server backend2 max_fails=3 fail_timeout=10s;
}
```
> 说明：
- 结合 $upstream_response_time 和 $status 可判断后端是否健康；
- 多后端服务建议部署于不同节点（跨机房冗余更稳）

#### ✅ 总结（运维建议）
| 项目           | 优化方向                    |
| ------------ | ----------------------- |
| `events`     | 合理配置连接数、事件模型，提升并发       |
| `http`       | 启用压缩、缓存、静态服务分流，减轻后端     |
| `log_format` | 精准追踪问题来源，辅助分析瓶颈         |
| `upstream`   | 配置健康检查 + 高可用            |
| `安全性`        | 限流、封 IP、防爬虫             |
| `部署方式`       | 使用 Docker/容器部署 + 配合监控工具 |

### 📄 2.生产级 nginx.conf 模板（适合高并发服务）
> 支持反向代理、负载均衡、健康检查、压缩、限流、日志结构化，适用于实际部署环境。
```nginx

# ---------------------- 全局设置 ----------------------
user  nginx;
worker_processes auto;
worker_rlimit_nofile 65535;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

# ---------------------- 事件模块 ----------------------
events {
    worker_connections 10240;
    use epoll;
    multi_accept on;
}

# ---------------------- HTTP 服务模块 ----------------------
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # 日志格式定义
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$request_time" "$upstream_response_time" '
                    '"$request_method $host$request_uri" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    # 文件传输优化
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;

    # 长连接与复用
    keepalive_timeout  65;
    keepalive_requests 10000;

    # 压缩配置
    gzip on;
    gzip_min_length 1k;
    gzip_comp_level 6;
    gzip_types text/plain application/json application/javascript text/css;

    # 限流防护配置
    limit_conn_zone $binary_remote_addr zone=addr:10m;
    limit_conn addr 100;

    limit_req_zone $binary_remote_addr zone=req:10m rate=10r/s;
    limit_req zone=req burst=20;

    # 上游服务配置
    upstream backend_api {
        server backend1:8080 max_fails=3 fail_timeout=10s;
        server backend2:8080 max_fails=3 fail_timeout=10s;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        access_log /var/log/nginx/api.access.log main;

        location / {
            proxy_pass http://backend_api;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /static/ {
            root /data/www;
            expires 30d;
            add_header Cache-Control "public";
        }
    }
}

```

#### 📊 优化前 vs 优化后性能对比示例
| 项目        | 优化前表现     | 优化后改善    | 原因与策略                           |
| --------- | --------- | -------- | ------------------------------- |
| 首页平均响应时间  | 280ms     | 120ms    | 开启 Gzip 压缩，浏览器端减压快              |
| 并发 500 用户 | 出现 502 错误 | 稳定处理     | 提高 worker\_connections 和 ulimit |
| 压测 QPS 峰值 | 1200 QPS  | 3600 QPS | 启用 keepalive + 缓存策略             |
| 服务故障恢复    | 需手动排查     | 自动切换     | 加入 `max_fails + fail_timeout`   |
| 日志分析耗时    | 分析慢       | 快速统计慢接口  | 使用 `$request_time` 日志字段         |

#### ✅ 面试讲解建议
当被问到「你做过哪些 Nginx 优化？」时，可以用 STAR 框架答：
- S（场景）：公司前端页面 + 微服务 API 网关都使用 Nginx，峰值流量在某促销日达到 2 万 QPS；
- T（任务）：优化系统稳定性、提高请求处理能力、增强故障容错；
- A（行动）：
  - 调整 worker_connections 并优化系统 ulimit -n；
  - 开启 Gzip 压缩、缓存控制、连接复用；
  - 设置 upstream 健康检查防止 502；
  - 使用结构化日志辅助分析；
- R（结果）：系统稳定提升至 3 倍并发，响应时间平均下降 60%，运维日志排查效率显著提升。
