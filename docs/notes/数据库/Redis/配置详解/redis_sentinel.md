## 🚀 Redis哨兵模式
### 一、前期规划
#### 1. 架构设计
Redis 哨兵模式的典型结构：
- 1个 Master 节点
- 至少2个 Slave 节点（推荐 2-3 台）
- 至少3个 Sentinel 实例（奇数个）
⚠️注意：Sentinel 本身不存储数据，它通过投票机制进行主从切换，必须保证大多数 Sentinel 节点存活。
```
[Client] 
   |——> Redis Sentinel × 3（用于监控和自动切换）
   |
   |——> Redis Master
         |
         ├── Redis Slave 1
         └── Redis Slave 2
```
#### 2.部署策略
- 主从节点分布在不同物理主机或虚拟机上
- 哨兵进程与 Redis 节点分开部署（也可以共用主机，但需防资源竞争）
- 建议部署在内网或通过 VPN 通信
- 配置统一的监控与告警（如 Prometheus + AlertManager）

### 二、系统层面优化建议
#### 1. 操作系统优化
- 文件句柄数：ulimit -n 设置为 100000+
- 关闭 Transparent Huge Pages (THP)
```
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```
- 禁用内存交换：
```
vm.swappiness = 0
```
#### 2. 网络优化
- 打开内核 TCP backlog：
```
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 8192
```
- 保证 Redis 端口（默认 6379）和 Sentinel 端口（默认 26379）在防火墙/安全组中开放
- 使用静态 IP 或 DNS（哨兵识别主从节点地址依赖 IP）

### 三、Redis 配置与部署步骤
#### 1. 安装 Redis
[Redis源码安装](redis_install.md)

#### 2.配置主从
master 节点 redis.conf（示例）：  
主节点不需要设置 replicaof，只需配置基础项  
```
# Redis监听端口，默认是6379
port 6379

# 绑定IP，建议写 0.0.0.0（或指定内网地址）
bind 0.0.0.0

# 是否启用保护模式（生产建议关闭）
protected-mode no

# 日志文件
logfile "/usr/local/redis/logs/redis.log"

# 持久化方式：AOF方式追加日志
appendonly yes

# AOF文件刷盘策略
appendfsync everysec  # 每秒写盘一次，平衡性能与数据安全

# 后台运行
daemonize yes

# 工作目录，持久化文件会放在这里
dir /usr/local/redis

# 设置访问密码
requirepass myRedisPassword
```
slave 节点 redis.conf（示例）：
```
# Redis监听端口，默认是6379
port 6379

# 绑定IP，建议写 0.0.0.0（或指定内网地址）
bind 0.0.0.0

# 是否启用保护模式（生产建议关闭）
protected-mode no

# 日志文件
logfile "/usr/local/redis/logs/redis.log"

# 持久化方式：AOF方式追加日志
appendonly yes

# AOF文件刷盘策略
appendfsync everysec  # 每秒写盘一次，平衡性能与数据安全

# 后台运行
daemonize yes

# 工作目录，持久化文件会放在这里
dir /usr/local/redis

# 设置访问密码
requirepass myRedisPassword

# 指定主节点IP和端口
replicaof 192.168.1.10 6379

# 如果主节点设置了密码，这里也要设置认证
masterauth myRedisPassword

# 可选，从节点是否可读（建议设为 yes 以支持读写分离）
replica-read-only yes

```
> 启动方式：
```
redis-server /path/to/redis.conf
```
> 验证主从
```
redis-cli -h <slave-ip> info replication
```
### 四、Sentinel 哨兵配置与部署
#### 1. 编写 Sentinel 配置文件
sentinel.conf 示例（3 份不同主机部署）：
```
# Sentinel 监听端口，默认26379
port 26379

# 日志文件路径
logfile "/usr/local/redis/logs/redis-sentinel.log"

# 后台运行
daemonize yes

sentinel monitor mymaster 192.168.1.10 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 10000
sentinel parallel-syncs mymaster 1

# 使用 Redis 的 requirepass 后，sentinel 需加此项
sentinel auth-user mymaster default
sentinel auth-pass mymaster myRedisPassword

```
> 参数说明：
- mymaster：主节点的标识名称（任意命名）
- 192.168.1.10：主节点IP地址
- 6379：主节点端口
- 2：最少多少个 Sentinel 同意主节点下线，才执行切换（需过半数）
| 配置项                                              | 说明                           | 推荐值            |
| ------------------------------------------------ | ---------------------------- | -------------- |
| `sentinel down-after-milliseconds mymaster 5000` | 判定主节点失联的时间（ms）               | 5000 \~ 10000  |
| `sentinel failover-timeout mymaster 10000`       | 故障转移的最大时长                    | 10000 \~ 30000 |
| `sentinel parallel-syncs mymaster 1`             | 故障转移后允许并行同步新主的从节点数量          | 1              |
| `sentinel auth-pass mymaster myRedisPassword`    | 如果 Redis 设置了密码，需要告知 Sentinel | 与 Redis 一致     |
| `sentinel config-epoch mymaster <自动生成>`          | 配置版本号，系统自动维护                 | 无需手动设置         |


#### 2. 启动 Sentinel 服务
```
redis-sentinel /path/to/sentinel.conf
或后台启动：
redis-server /path/to/sentinel.conf --sentinel
```
#### 3. 验证 Sentinel 状态
```
redis-cli -p 26379
> SENTINEL get-master-addr-by-name mymaster
```
### 六、哨兵模式参数详解
| 参数项                                | 说明                          |
| ---------------------------------- | --------------------------- |
| `sentinel monitor`                 | 配置监控的主节点                    |
| `sentinel down-after-milliseconds` | 哨兵多久无响应后认为主节点下线             |
| `sentinel failover-timeout`        | 故障转移所允许的最大时间                |
| `sentinel parallel-syncs`          | 同时允许几个从节点复制新的主节点            |
| `sentinel auth-pass`               | 若 Redis 设置密码，Sentinel 需配置认证 |

### 七、进阶实践建议
#### 1. 使用 systemd 管理服务
```
[Unit]
Description=Redis Sentinel
After=network.target

[Service]
ExecStart=/usr/local/bin/redis-sentinel /etc/redis/sentinel.conf
Restart=always

[Install]
WantedBy=multi-user.target
```
#### 2. 日志与监控接入
- 配置 logfile 输出
- 使用 Redis Exporter 接入 Prometheus
- 告警规则示例：
    - Sentinel 节点 down
    - 主节点切换
    - 延迟过高  

#### 3. 故障模拟与切换验证
- 停掉 Master，观察 Sentinel 响应时间和新主节点选举情况
- 检查新主从同步关系，确保客户端连接自动恢复

### 五、生产实践建议
1.配置持久化目录为挂载磁盘或 RAID 设备  
2.Sentinel 不要和主节点部署在同一台机器（避免节点挂掉导致失去选票）  
3.每台服务器部署多个 Sentinel 时，端口不要冲突  
4.使用 systemd 启动服务，统一管理和自动重启  
5.定期备份配置文件和 RDB/AOF 文件  