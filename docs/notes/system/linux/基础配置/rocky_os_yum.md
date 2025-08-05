### 🛠️Rocky9更换国内镜像源
- 高校镜像推荐 mirror.sjtu.edu.cn 和 mirrors.zju.edu.cn。
- 商业公司镜像推荐 mirrors.aliyun.com。
- 其他多数镜像不全，要么没有 almalinux，要么没有 rocky。

#### 默认镜像源
Rocky Linux 9 默认 repo 如下：  
```
[root@localhost ~]# dnf repolist
repo id                                               repo name
appstream                                             Rocky Linux 9 - AppStream
baseos                                                Rocky Linux 9 - BaseOS
extras                                                Rocky Linux 9 - Extras
# 安装 epel 后增加
epel                                                  Extra Packages for Enterprise Linux 9 - x86_64
```
#### 文件列表如下
```
[root@localhost ~]# ll /etc/yum.repos.d/
epel.repo
epel-testing.repo
epel-cisco-openh264.repo
rocky-addons.repo
rocky-devel.repo
rocky-extras.repo
rocky.repo
# 注意 (sysin)：Rocky 8 的文件名首字母大写 R
官方镜像列表
官方镜像列表：https://mirrors.rockylinux.org/mirrormanager/mirrors，CN 开头的站点。
```
#### 国内源替换步骤
该项配置方法兼容 Rocky Linux 8 和 9。  
Rocky Linux 国内镜像源更换方法如下。  
##### 上海交通大学示例  
```
mirror.sjtu.edu.cn = mirrors.sjtug.sjtu.edu.cn
sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=https://mirror.sjtu.edu.cn/rocky|g' \
    -i.bak \
    /etc/yum.repos.d/[Rr]ocky*.repo
    # 注意 8 系列 Rocky R 大些，9 系列 r 小写 (sysin)
```
- 恢复 (sysin)
```
sed -e 's|^#mirrorlist=|mirrorlist=|g' \
    -e 's|^baseurl=https://mirror.sjtu.edu.cn/rocky|#baseurl=http://dl.rockylinux.org/$contentdir|g' \
    -i.bak \
    /etc/yum.repos.d/[Rr]ocky*.repo
更换其他镜像，对应按照上面替换 Mirror Name 即可，注意路径 “/rocky”，但是阿里云镜像是 “/rockylinux”。
```
##### 阿里云示例
```
sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=https://mirrors.aliyun.com/rockylinux|g' \
    -i.bak \
    /etc/yum.repos.d/[Rr]ocky*.repo
    # 注意 8 系列 Rocky R 大些，9 系列 r 小写 (sysin)
    # 阿里云文档有误无法匹配：https://developer.aliyun.com/mirror/rockylinux
```
- 恢复 (sysin)  
```
sed -e 's|^#mirrorlist=|mirrorlist=|g' \
    -e 's|^baseurl=https://mirrors.aliyun.com/rockylinux|#baseurl=http://dl.rockylinux.org/$contentdir|g' \
    -i.bak \
    /etc/yum.repos.d/[Rr]ocky*.repo
EPEL
```

#### epel修改步骤
```
上海交通大学 epel 示例：
# 注意：上海交通大学地址多一个 fedora
sed -e 's|^metalink=|#metalink=|g' \
    -e 's|^#baseurl=https://download.example/pub|baseurl=https://mirror.sjtu.edu.cn/fedora|g' \
    -i.bak \
    /etc/yum.repos.d/epel{,-testing}.repo
    # 说明：之前为 /etc/yum.repos.d/epel*.repo，新版多了一个 epel-cisco-openh264.repo 无镜像，将其过滤

# 恢复 (sysin)
sed -e 's|^#metalink=|metalink=|g' \
    -e 's|^baseurl=https://mirror.sjtu.edu.cn/fedora|#baseurl=https://download.example/pub|g' \
    -i.bak \
    /etc/yum.repos.d/epel{,-testing}.repo
    # 说明：之前为 /etc/yum.repos.d/epel*.repo，新版多了一个 epel-cisco-openh264.repo 无镜像，将其过滤

阿里云 epel 示例：
sed -e 's|^metalink=|#metalink=|g' \
    -e 's|^#baseurl=https://download.example/pub|baseurl=https://mirrors.aliyun.com|g' \
    -i.bak \
    /etc/yum.repos.d/epel{,-testing}.repo
    # 说明：之前为 /etc/yum.repos.d/epel*.repo，新版多了一个 epel-cisco-openh264.repo 无镜像，将其过滤

# 恢复 (sysin)
sed -e 's|^#metalink=|metalink=|g' \
    -e 's|^baseurl=https://mirrors.aliyun.com|#baseurl=https://download.example/pub|g' \
    -i.bak \
    /etc/yum.repos.d/epel{,-testing}.repo
    # 说明：之前为 /etc/yum.repos.d/epel*.repo，新版多了一个 epel-cisco-openh264.repo 无镜像，将其过滤

其他替换地址如：
mirrors.zju.edu.cn
mirrors.nju.edu.cn（无 rocky）
mirrors.ustc.edu.cn（无 almalinux）
补充：epel-cisco-openh264.repo 即 Cisco OpenH264 仓库似乎暂无国内镜像，速度慢禁用即可。
```

#### 替换后更新缓存记录
```
yum -y install yum-utils
yum-config-manager --enable epel-cisco-openh264
# 或者编辑 /etc/yum.repos.d/epel-cisco-openh264.repo 修改 enabled=0
清理并重新生成软件包信息缓存：
# 备注：yum=dnf
yum clean all
rm -rf /var/cache/yum
yum makecache
yum autoremove #此命令需要已经 makecache
```
