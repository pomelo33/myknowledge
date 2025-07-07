## 🚀 Redis源码安装
> 环境说明：  
> 操作系统：Rocky 9.3  
> redis版本：8.0.3  

### 1、安装编译工具
```
yum install -y gcc gcc-c++ make tcl
```
### 2、解压源码包
```
tar -xzf redis-8.0.3.tar.gz 
```
### 3、开始编译
```
cd redis-8.0.3
make
make test # 可忽略
```
### 4、安装
```
创建并指定安装目录为/usr/local/redis
mkdir -p /usr/local/redis/{conf,logs,data}
make install PREFIX=/usr/local/redis/ 
```
### 5、将conf文件复制到/usr/local/redis/conf
```
cd /packages/redis-8.0.3
ll
cp redis.conf /usr/local/redis/conf
```
### 6、Redis基本配置
```
cd /usr/local/redis/
vim conf/redis.conf
```
#### 6.1修改redis为后台启动
```
daemonize yes
```
#### 6.2开放IP访问地址
```
找到bind 127.0.0.1所在行。
输入 i 进入编辑后，用”#”符号注释该行
```
#### 6.3关闭保护模式
```
protect  将no改成yes
```
#### 6.4密码配置
```
requirepass admin
```
### 7、修改内核参数
```
# 临时生效
sysctl  -w  vm.overcommit_memory=1
# 永久生效
echo 'vm.overcommit_memory=1' >> /etc/sysctl.conf && sysctl -p
### 可选值：0，1，2。
# 0：表示内核将检查是否有足够的可用内存供应用进程使用；如果有足够的可用内存，内存申请允许；否则，内存申请失败，并把错误返回给应用进程。
# 1：表示内核允许分配所有的物理内存，而不管当前的内存状态如何。
# 2： 表示内核允许分配超过所有物理内存和交换空间总和的内存。
```
#### 8、启动服务
```
/usr/local/redis/bin/redis-server /usr/local/redis/conf/redis.conf
```
### 9、关闭服务
#### 9.1、在客户端里面关闭
```
localhost:6379> shutdown
not connected> 
not connected> exit
[root@redis ~]# ps -ef |grep redis | grep -v grep
 ```
 
#### 9.2、单实例关闭
```
[root@redis ~]# redis-cli -a oracle shutdown
[root@redis ~]# redis-server /redis/redis.conf 
[root@redis ~]# ps -ef |grep redis | grep -v grep
root       6067      1  0 18:43 ?        00:00:00 redis-server *:6379
```
#### 9.3、多实例关闭
```
[root@redis ~]# redis-cli -p 6379,6378,6377 shutdown
```
### 10、system管理服务启停
```bash
# vim /usr/lib/systemd/system/redis.service 
[Unit]
Description=Redis
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/redis/bin/redis-server /usr/local/redis/conf/redis.conf
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID
RuntimeDirectory=redis
RuntimeDirectoryMode=0755
LimitNOFILE=65536
PrivateTmp=true

[Install]
WantedBy=multi-user.target

# systemctl deamon-reload
# systemctl start redis
# systemctl enable redis
# systemctl status redis
```