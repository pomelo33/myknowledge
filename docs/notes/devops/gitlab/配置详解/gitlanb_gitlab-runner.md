## 🚀 安装并配置 GitLab Runner

> gitlab runner 官方文档：https://gitlab.cn/docs/runner/install/linux-repository.html

### 🧱 一、GitLab Runner 是什么？
GitLab Runner 是 GitLab CI/CD 执行任务的核心组件，它负责从 GitLab 接收 .gitlab-ci.yml 的 pipeline 配置，然后执行实际的构建、测试、部署等步骤。

### 🧰 二、安装 GitLab Runner（以 Ubuntu 为例）
#### ✅ 1. 添加官方源并安装 Runner
```
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt install gitlab-runner
```