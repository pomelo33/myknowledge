## Nginx 学习笔记
[TOC]

---
### 📌 基本介绍
- 名称：Nginx
- 类型：Web服务器 / 反向代理 / 负载均衡器
- 场景：静态资源服务、动静分离、反向代理、负载均衡
  
---
### 🔧 安装方法
- apt/yum 安装
- 源码编译方式
- Docker 部署方法

---
### 🛠️ 配置示例

#### 1. 反向代理配置
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}
