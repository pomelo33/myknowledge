#### 📝 容器启动Mysql数据库
环境：mysql：5.7

##### Docker方式
```
docker run -itd --restart=always --name mysql -e MYSQL_ROOT_PASSWORD=123456 \ 
-e MYSQL_DATABASE=demo \
-e MYSQL_USER=liu \
-e MYSQL_PASSWORD=mysql \
-e TZ=Asia/Shanghai \
-v /my/datadir:/var/lib/mysql \
-p 3306:3306 \
mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

```

##### docker-compose方式
```
version: '3.1'
services:
    db:
        image: mysql:5.7
        ports:
            - "3306:3306"
        volumes:
            - /mysql/datadir:/var/lib/mysql
            - /mysql/conf.d/:/etc/mysql/conf.d
        environment:
            - TZ=Asia/Shanghai
            - MYSQL_ROOT_PASSWORD=123456
        restart: "always"
    
```
