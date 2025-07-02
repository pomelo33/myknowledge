### 📘 生产环境下的 log_format 日志格式优化建议

#### ✅ 优化目标：
- 记录完整的用户请求行为；
- 包含性能指标（响应时间）；
- 支持故障快速定位（状态码、后端耗时）；
- 便于用 ELK、GoAccess 等工具进行结构化分析。

#### 🧩 推荐 log_format 模板（高可观测性版本）
```nginx
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                  '$status $body_bytes_sent "$http_referer" '
                  '"$http_user_agent" "$request_time" "$upstream_response_time" '
                  '"$host" "$server_name" "$request_uri" "$request_method" '
                  '"$http_x_forwarded_for" "$connection" "$connection_requests"';

```

#### 📖 字段解释
| 字段                                     | 说明                                         |
| -------------------------------------- | ------------------------------------------ |
| `$remote_addr`                         | 客户端真实 IP 地址（可用 `$http_x_forwarded_for` 补充） |
| `$request_time`                        | 客户端请求总耗时（从接收到响应）                           |
| `$upstream_response_time`              | 后端服务响应耗时（网络、程序响应瓶颈判断）                      |
| `$status`                              | HTTP 状态码（200、404、500）                      |
| `$request_uri`                         | 实际请求的 URI                                  |
| `$request_method`                      | GET / POST / PUT 等                         |
| `$http_referer`                        | 引用来源页                                      |
| `$http_user_agent`                     | 终端浏览器或客户端信息                                |
| `$connection` / `$connection_requests` | 当前连接 ID 及请求次数，定位多请求问题                      |
| `$server_name`                         | 当前请求命中的虚拟主机名                               |
| `$host`                                | 请求头中的域名                                    |

#### 📋 日志使用建议
- 使用按天切分的日志文件 /var/log/nginx/access_$(date +%F).log；
- 利用 logrotate 设置自动归档、压缩、保留；[nginx日志切割](nginx_logs.md)
- 配合 GoAccess 可实现实时流量、访问分析；
- 配合 fail2ban 或 WAF 对恶意 IP / User-Agent / Referer 做规则封锁。