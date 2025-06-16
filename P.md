🔧 第1~2周：Nginx 深度实战
✅ 第1周（基础 + 配置）
安装：Nginx 编译版与系统包版本区别，推荐使用官方稳定版；
配置文件结构理解（nginx.conf）
常用模块：
server 配置虚拟主机
location 路由规则
静态资源服务与 MIME 类型配置
日志配置与访问日志分析（log_format）

实战任务：
启动两个本地服务（如 Python Flask） → Nginx 配置反向代理；
配置支持多虚拟主机 + 设置日志分开输出。

📝 文档产出建议：
README.md：Nginx 快速入门说明
how-to/nginx_reverse_proxy.md：反向代理配置案例
troubleshooting.md：常见错误（403、502、404）


✅ 第2周（负载均衡 + HTTPS + 高可用）
负载均衡算法：轮询、ip_hash、least_conn
配置 HTTPS（Let's Encrypt 或自签证书）
动静分离配置（静态资源独立服务）
搭配 Keepalived 实现双主热备（了解 VIP 概念）
📝 文档产出建议：
how-to/nginx_https_balancer.md：HTTPS + 负载均衡案例
architecture.md：加上 Nginx 架构与 HA 设计图


🧭 第3~4周：注册中心（以 Nacos 为主）
✅ 第3周（服务注册与配置中心）

Nacos 单机部署（或 Docker 版）
UI 界面操作：注册服务、查看服务、配置中心使用
服务注册机制（临时/永久实例，心跳机制）
配置中心功能演示：Spring Boot 应用动态刷新配置

实战任务：
部署一个简单的 Spring Boot demo → 注册到 Nacos
使用 Nacos 配置中心替代 application.yml

📝 文档产出建议：
README.md 更新 Nacos 简介与安装说明
how-to/nacos_service_register.md：服务注册实战
reference.md 添加 Nacos 常用 API/命令

✅ 第4周（集群部署 + 故障排查）
Nacos 集群搭建（建议本地 3 节点 Docker）
数据持久化配置（MySQL 后端）
服务发现异常调试、健康检查机制深入
与 Nginx 联合使用，实现多服务管理

📝 文档产出建议：
architecture.md：更新为“注册中心 + Nginx 路由”架构
troubleshooting.md：添加 Nacos 启动失败、注册失败案例分析


2. HTTPS 配置
3. 负载均衡配置（轮询、ip_hash、least_conn）
🧠 核心概念
worker 进程模型

connection 与请求处理流程

keepalive、gzip、缓存配置

📈 性能优化参数
worker_connections

sendfile、tcp_nopush、tcp_nodelay

🧪 实战演练
项目名称：设备管理系统

实现内容：使用 Nginx 反向代理多个服务并配置 HTTPS

🔍 故障排查
错误码说明：403、502、499

日志分析技巧