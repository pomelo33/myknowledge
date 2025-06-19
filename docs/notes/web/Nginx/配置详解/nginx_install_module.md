### 📝Nginx动态新增模块
#### 1.首先进入nginx解压包的目录中
```
# cd nginx-1.16.0
```

#### 2.查看已安装Nginx的模块
```
# nginx -V 
```

#### 3.添加需要新增的模块
`将原来的模块添加后续再跟要新增的模块)`
```
# ./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-pcre --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-threads --with-http_v2_module --with-http_flv_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --with-http_image_filter_module --with-http_slice_module --with-mail --with-mail_ssl_module --with-http_mp4_module --with-stream --with-stream_ssl_module --with-debug --with-file-aio \
-add-module=/home/liuhd/nginx-rtmp-module-1.2.1 

注意:
--add-module 为添加的第三方模块
--with..._module 表示启用的nginx模块，如此处启用了好几个模块
```

#### 4.编译
```
# make 
注意：切记不要执行make install，不然会导致覆盖原来的nginx版本

编译完成后，把./nginx-1.16.0/objs中的nginx替换掉之前的安装的/usr/local/nginx/sbin/中的nginx文件,然后重启nginx。
```
#### 5. 备份旧版，替换新版
```
备份
# cp /usr/local/nginx/sbin/nginx /usr/local/nginx/sbin/nginx.bak
更新
# mv ./nginx-1.16.0/objs/nginx /usr/local/nginx/sbin/nginx
查看
# nginx -V 
```

