---
tags:
- nginx
- examples
- flask-nginx-lb
title: Readme
---

## 🚀 Flask + Nginx 负载均衡实战（含健康检查 + Redis + 故障模拟） 

[TOC]
---
###  📁 项目完整目录结构
```plaintext
flask-nginx-lb/
├── app/
│   ├── app_redis.py                    # Flask 应用代码（redis）
│   ├── app.py                    # Flask 应用代码
│   └── Dockerfile               # Flask 镜像构建文件
├── nginx/
│   └── nginx.conf               # Nginx 配置文件（含负载均衡与健康检查）
├── scripts/
│   └── curl_test.sh             # 请求统计脚本
├── docs/
│   └── architecture.png         # 架构图（建议使用 draw.io 设计）
├── docker-compose.yml          # Docker Compose 编排文件
└── README.md                   # 项目说明文档（含部署步骤与问题排查）
```
### 📌 项目简介
为深入理解 Nginx 的负载均衡原理及容器化微服务的部署与管理流程，设计一个完整的“前端 Nginx 反向代理 + 后端多实例 Flask 服务 + Redis 缓存”的架构系统，支持健康检查、故障恢复、请求统计等功能。包括如下：
- 健康检查配置
- 模拟服务实例故障
- 集成 Redis（Flask 缓存计数器）
- curl 脚本统计请求轮询结果

---
### 🧭 架构图设计
![](docs/architecture.drawio.png) 

---
### 🧱 技术栈
- Flask（Web服务）
- Nginx（反向代理、轮询负载均衡、健康检查）
- Docker & Docker Compose
- Redis （计数器功能）
- Bash Shell

---

### 📌 启动服务
在项目目录下运行：
docker-compose up --build -d

访问浏览器或命令行：
curl http://localhost

会交替看到：
Hello from flask_app1!
Hello from flask_app2!

### ⚙️ 负载均衡策略
修改 nginx.conf 中的 upstream 部分
```
ip_hash（按 IP 绑定实例）
upstream flask_app {
    ip_hash;
    server app1:5000;
    server app2:5000;
}

least_conn（最少连接）
upstream flask_app {
    least_conn;
    server app1:5000;
    server app2:5000;
}
```

### ⚙️ 健康检查设置
在nginx.conf中添加配置  
当某个 Flask 实例 10 秒内失败超过 3 次，请求将暂时不分发给它。
```
upstream flask_app {
    server app1:5000 max_fails=3 fail_timeout=10s;
    server app2:5000 max_fails=3 fail_timeout=10s;
}

🧪 模拟挂掉一个实例
# 停掉 app2
docker stop flask_app2

# 连续请求
curl http://localhost
你将始终看到来自 flask_app1 的响应，说明负载均衡机制生效。
```
### 🔁 curl 请求统计脚本
[curl测试脚本](scripts/curl_test.sh)  

```
执行脚本：
bash scripts/curl_test.sh
```

### 🗃️ Redis 集成（计数器）
更新 app.py 支持 Redis：app/app_redis.py
```
docker-compose.yml 添加：
  redis:
    image: redis:7.4
    container_name: redis

Dockerfile 修改运行.py脚本名称
```

### 🧯 常见问题排查

| 问题                  | 可能原因                          | 解决方案                                              |
| --------------------- | --------------------------------- | ----------------------------------------------------- |
| 502 Bad Gateway       | Flask 容器未就绪或挂掉            | 检查 app1/app2 是否正常运行                           |
| Nginx 配置不生效      | 缓存未刷新                        | 修改后重启 Nginx 容器：`docker-compose restart nginx` |
| curl 总是访问同一实例 | 使用了浏览器缓存 / DNS 轮询未更新 | 测试时尽量使用 curl 或禁用缓存访问                    |
| Redis 报连接错误      | Flask 代码未正确连接 Redis 容器   | 确保使用 `redis` 作为 Redis 主机名                    |







