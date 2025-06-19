### 📝Python环境安装

`思路：`
1. 安装依赖包
2. 下载Python安装包
3. 解压
4. 安装
5. 配置环境变量

### 1、安装依赖包
```
# yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel
```

#### 2、下载Python安装包
```
安装包地址：https://www.python.org/ftp/python/
wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz

```
#### 3、解压
```
tar -zxvf Python-3.9.7.tgz
```

#### 4、安装.
```
cd Python-3.9.7
./configure --prefix=/usr/local/python3
make && make install
```

#### 5、配置环境变量
```
vim ~/.bash_profile
export PYTHON_HOME=/app/python3
export PATH=PATH:$PYTHON_HOME/bin
```