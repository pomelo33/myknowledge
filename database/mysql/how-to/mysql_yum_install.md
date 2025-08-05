### yum安装mysql5.7以及默认root密码查看并修改

#### 1.mysql的yum仓库
```
https://dev.mysql.com/downloads/repo/yum  
```
#### 2.安装mysql服务器  
```
# yum localinstall https://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
# yum install -y mysql-community-server
```
#### 3.启动mysql服务
```
# systemctl start mysqld
```
此时mysql会为root随机生成一个密码在/var/log/mysqld.log日志中。
```
# grep "password" /var/log/mysqld.log  查看随机密码
```
登录mysql修改密码时报错：Your password does not satisfy the current policy requirements. 问题
如果只是修改为一个简单的密码，会报以下错误：
```
mysql>  ALTER USER USER() IDENTIFIED BY '12345678';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
```
- 设置mysql密码规则
```
set global validate_password_policy=0;  
set global validate_password_length=4;  
set password for 'fred'@'localhost'=password('passwd');
flush privileges;

```

###### 详解随机密码

为了加强安全性，MySQL5.7为root用户随机生成了一个密码，在error log中，关于error log的位置，如果安装的是RPM包，则默认是/var/log/mysqld.log。

一般可通过log_error设置

```
mysql> select @@log_error;
+---------------------+
| @@log_error         |
+---------------------+
| /var/log/mysqld.log |
+---------------------+
1 row in set (0.00 sec)

```

可通过# grep "password" /var/log/mysqld.log 命令获取MySQL的临时密码

```
2016-01-19T05:16:36.218234Z 1 [Note] A temporary password is generated for root@localhost: waQ,qR%be2(5
```

用该密码登录到服务端后，必须马上修改密码，不然会报如下错误：

```
mysql> select user();
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
```

如果只是修改为一个简单的密码，会报以下错误：

```
mysql>  ALTER USER USER() IDENTIFIED BY '12345678';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
```

validate_password_policy有以下取值：

| Policy          | Tests Performed                                              |
| --------------- | ------------------------------------------------------------ |
| `0` or `LOW`    | Length                                                       |
| `1` or `MEDIUM` | Length; numeric, lowercase/uppercase, and special characters |
| `2` or `STRONG` | Length; numeric, lowercase/uppercase, and special characters; dictionary file |

默认是1，即MEDIUM，所以刚开始设置的密码必须符合长度，且必须含有数字，小写或大写字母，特殊字符。

只想设置root的密码为123456。必须修改两个全局参数：

首先，修改validate_password_policy参数的值

```
mysql> set global validate_password_policy=0;
Query OK, 0 rows affected (0.00 sec)
```

这样，判断密码的标准就基于密码的长度了。这个由validate_password_length参数来决定。

```
mysql> select @@validate_password_length;
+----------------------------+
| @@validate_password_length |
+----------------------------+
|                          8 |
+----------------------------+
1 row in set (0.00 sec)
```

validate_password_length参数默认为8，它有最小值的限制，最小值为：

```
validate_password_number_count
validate_password_special_char_count
validate_password_mixed_case_count)

其中，validate_password_number_count指定了密码中数据的长度，validate_password_special_char_count指定了密码中特殊字符的长度，validate_password_mixed_case_count指定了密码中大小字母的长度。

这些参数，默认值均为1，所以validate_password_length最小值为4，如果你显性指定validate_password_length的值小于4，尽管不会报错，但validate_password_length的值将设为4。如下所示：

mysql> select @@validate_password_length;
+----------------------------+
| @@validate_password_length |
+----------------------------+
|                          8 |
+----------------------------+
1 row in set (0.00 sec)

mysql> set global validate_password_length=1;
Query OK, 0 rows affected (0.00 sec)

mysql> select @@validate_password_length;
+----------------------------+
| @@validate_password_length |
+----------------------------+
|                          4 |
+----------------------------+
1 row in set (0.00 sec)


如果修改了validate_password_number_count，validate_password_special_char_count，validate_password_mixed_case_count中任何一个值，则validate_password_length将进行动态修改。

mysql> select @@validate_password_length;
+----------------------------+
| @@validate_password_length |
+----------------------------+
|                          4 |
+----------------------------+
1 row in set (0.00 sec)

mysql> select @@validate_password_mixed_case_count;
+--------------------------------------+
| @@validate_password_mixed_case_count |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
1 row in set (0.00 sec)

mysql> set global validate_password_mixed_case_count=2;
Query OK, 0 rows affected (0.00 sec)

mysql> select @@validate_password_mixed_case_count;
+--------------------------------------+
| @@validate_password_mixed_case_count |
+--------------------------------------+
|                                    2 |
+--------------------------------------+
1 row in set (0.00 sec)

mysql> select @@validate_password_length;
+----------------------------+
| @@validate_password_length |
+----------------------------+
|                          6 |
+----------------------------+
1 row in set (0.00 sec)
```