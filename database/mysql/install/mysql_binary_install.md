### 📝 mysql二进制安装
mysql 有三种安装方式“源码编译安装、二进制安装、rpm包安装”。  
二进制包安装，是经过源码编译后的二进制包，里面包含了已经编译完成,可以直接运行的程序。  
源码包是开源的，里面装的是程序的源代码，我们将源码包下载到本地之后，进行解压、编译生成二进制文件之后，才可以运行。这个操作一般会有 configure、make、make install 三步。  

#### 1.准备工作

mysql 依赖于 libaio 库。如果未在本地安装此库，则数据目录初始化和后续服务器启动步骤将失败。如有必要，请使用适当的包管理器进行安装。
```
$ yum install libaio -y
```
#### 2.安装步骤
```
1.下载 mysql 二进制包，地址如下：<https://dev.mysql.com/downloads/mysql/>
$ cd /tmp
$  wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.15-linux-glibc2.12-x86_64.tar.xz

2.解压
$ tar -xvf mysql-8.0.15-linux-glibc2.12-x86_64.tar.xz
$ mv  mysql-8.0.15-linux-glibc2.12-x86_64 mysql

解压二进制包，为了以后方便使用，然后将解压后的二进制文件改下名字改成 mysql，这里官方文档给出个提示就是：“ 在 MySQL Server 8.0.12中，压缩算法从 Gzip 更改为 XZ; 并且通用二进制文件的文件扩展名从 .tar.gz 更改为 .tar.xz”
```
#### 3.创建一个mysql用户和组
```
$ groupadd mysql
$ useradd -r -g mysql -s /sbin/nologin mysql
建立 mysql 用户和 mysql 用户组，然后将 mysql 用户放入到 mysql 组中。只是需要为 /usr/local/mysql/ 文件夹修改权限为 mysql，所以禁用掉此用户登录服务器权限。
```
#### 4.修改mysql目录所属权限
```
$ cd /mysql
$ chown -R mysql.mysql /mysql
```
#### 5.初始化mysql生成临时密码
```
创建数据目录
$ mkdir data

# 使用 --initialize 参数初始化 mysql 时产生的密码，将密码保存在 log 日志中
bin/mysqld --initialize --user=mysql --datadir=/mysql/data --basedir=/mysql 

# 使用 --initialize-insecure 参数初始化，这个时候初始化的 root 是没有初始密码的
bin/mysqld --initialize-insecure --user=mysql --datadir=/mysql/data --basedir=/mysql

$ bin/mysqld  --initialize --user=mysql  --basedir=/mysql  --datadir=/data
输出内容
....
2021-03-28T00:08:52.768064Z 5 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: qeTKG#u8?ijx
....

初始化数据库过程中会为账户生成随机初始化密码，比如刚刚的 root\@localhost: *-?Q#\<k/K5;h其中的“*-?Q#\<k/K5;h”就是待会要登录的初始密码。
```
参数说明

*   \--user ：运行mysql的用户
*   \--basedir：mysql安装目录
*   \--datadir：mysql服务数据目录路径

#### 6.修改my.cnf配置文件
```
# vi /mysql/my.cnf                              
[mysqld]
user=mysql
basedir=/mysql/
datadir=/mysql/data
character_set_server=utf8mb4
collation-server=utf8mb4_general_ci

#只能用IP地址检查客户端的登录，不用主机名,跳过域名解析
skip-name-resolve=1
 
#日志时间
log_timestamps=SYSTEM
 
#慢日志
long_query_time=3
slow_query_log=ON
slow_query_log_file=/mysql/logs/slow_query.log
 
#通用日志
general_log=1
general_log_file=/mysql/logs/mysql_general.log
 
#错误日志
log-error=/mysql/logs/mysql-error.log
 
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
 
# 默认使用"mysql_native_password"插件认证
default_authentication_plugin=mysql_native_password
 
port=3306
socket=/tmp/mysql.sock
max_connections=1000
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
max_allowed_packet=300M
 
[mysql]
 port=3306
socket=/tmp/mysql.sock
```
#### 7.添加用户环境变量
```
以root用户为例
$ vim /root/.bash_profile
export MYSQL_HOME=/mysql/bin
export PATH=$PATH:$MYSQL_HOME
```
#### 8.启动mysql服务
```
$ mysqld_safe --defaults-file=/mysql/my.cnf&

或者配置system管理mysql
 
vim /etc/systemd/system/mysqld.service
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
 
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/app/mysql/bin/mysqld --defaults-file=/etc/my.cnf
LimitNOFILE = 5000
```

#### 9.修改临时密码
```
$ mysql -uroot -p"qeTKG#u8?ijx"
> alter user 'root'@'localhost' identified by 'root';
> flush privileges;

如果不修改临时密码，mysql 是不让进行操作的，所以必须要修改临时密码
```