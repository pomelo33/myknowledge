## nginx日志切割
配置 Nginx 日志保存 6 个月，通过 logrotate 来管理日志文件的轮转、压缩和清理。Nginx 本身不支持按日期自动删除日志，只能设置日志路径和格式；日志保留策略通常由 Linux 的日志轮转工具 logrotate 控制。   

### ✅ 一、确认 Nginx 日志位置
在 Nginx 配置文件中（如 /etc/nginx/nginx.conf 或某个 server 块）：
```
http {
    access_log /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log warn;
}
```

### 🧰 二、配置 logrotate 保留日志 6 个月（约 26 周）
编辑或创建文件 /etc/logrotate.d/nginx：
```
sudo vim /etc/logrotate.d/nginx
示例配置如下：
/var/log/nginx/*.log {
    daily                          # 每天切割（你也可以用 weekly 或 monthly）
    rotate 180                     # 保留 180 天（半年）
    compress                     # 启用 gzip 压缩旧日志
    delaycompress                # 推迟一周压缩上周日志
    missingok                    # 如果日志不存在，不报错
    notifempty                   # 如果日志为空，不轮转
    dateext                        # 启用日期命名，如 access.log-20250630
    dateformat -%Y-%m-%d           # 自定义日期格式为：-2025-06-30
    create 0640 www-data adm     # 重新创建文件，指定权限和属主
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
} 
```
> ✅ rotate 180 表示每天保留    180个备份，即大约 6 个月。


### 📅 三、强制测试日志轮转
你可以使用以下命令手动测试配置是否生效：
```
sudo logrotate -f /etc/logrotate.d/nginx
```

### 🔍 四、补充说明
日志文件一般存储在 /var/log/nginx/ 目录下。  
如果你想改为 按月轮转，可把 weekly 改为 monthly，rotate 6 保留 6 个月：
```
monthly
rotate 6
```