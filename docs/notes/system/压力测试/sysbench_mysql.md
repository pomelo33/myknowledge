### 📝 Sysbench压测Mysql数据库
#### 1.依赖包安装及部署
```
将包上传
yum -y install make automake libtool pkgconfig libaio-devel
# For MySQL support, replace with mysql-devel on RHEL/CentOS 5
yum -y install mariadb-devel openssl-devel
# For PostgreSQL support
yum -y install postgresql-devel
tar -xzf sysbench-1.0.20.tar.gz
cd ../../sysbench-1.0.20
#查看目录下内容
ls 
./autogen.sh
./configure
make -j
make install
```

#### 2.创建压测数据
```
sysbench  --db-driver=mysql --mysql-host=<数据库IP> --mysql-port=<数据库端口> --mysql-user=<数据库用户名> --mysql-password=<数据库密码> --mysql-db=<库名> --tables=10 --table-size=100000 oltp_read_only prepare

启动测试程序
sysbench  --db-driver=mysql --mysql-host=<数据库IP> --mysql-port=<数据库端口> --mysql-user=<数据库用户名> --mysql-password=<数据库密码> --mysql-db=<库名>  --tables=10 --threads=1 --time=0  --report-interval=30 oltp_read_only run > sysbench_read.log 2>&1 &

查看日志
tail -f sysbench_read.log

查看进程
ps aux |grep sysbench

停止sysbench进程
pkill sysbench
```