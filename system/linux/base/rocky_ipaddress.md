### 🛠️rocky9配置静态IP
#### 1、系统
```bash
[root@localhost ~]# hostnamectl 
   Static hostname: (unset)                          
Transient hostname: localhost
         Icon name: computer-vm
           Chassis: vm 🖴
        Machine ID: 8404ce97c6d146bab7b287a791b3d6df
           Boot ID: 0ba74603221948bb9dbf922dd4b40676
    Virtualization: vmware
  Operating System: Rocky Linux 9.3 (Blue Onyx)      
       CPE OS Name: cpe:/o:rocky:rocky:9::baseos
            Kernel: Linux 5.14.0-362.8.1.el9_3.x86_64
      Architecture: x86-64
   Hardware Vendor: VMware, Inc.
    Hardware Model: VMware Virtual Platform
  Firmware Version: 6.00
```
#### 2、进入  /etc/NetworkManager/system-connections/ 目录
```bash
[root@localhost ~]# cd /etc/NetworkManager/system-connections/
[root@localhost system-connections]# ls
ens160.nmconnection  ens192.nmconnection
[root@localhost system-connections]#
```

#### 3、修改配置文件
```
[root@localhost system-connections]# vim ens160.nmconnection
在ipv4下修改如下内容，然后保存退出：
...
[ipv4]
method=manual                                ## 手动IP
address1=192.168.66.160/24,192.168.66.200    ## ip，子网掩码，网关
dns=114.114.114.114;8.8.8.8                  ## DNS
...
```

#### 4、加载配置文件
```
[root@localhost system-connections]# ls
ens160.nmconnection
[root@localhost system-connections]# nmcli connection load  /etc/NetworkManager/system-connections/ens160.nmconnection 
```

#### 5、激活配置文件
```
[root@localhost system-connections]# ls
ens160.nmconnection
[root@localhost system-connections]# nmcli connection up  /etc/NetworkManager/system-connections/ens160.nmconnection 
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/2)
```

#### 6、查看IP
```
[root@localhost ~]# ip a 
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:0c:29:8a:ab:36 brd ff:ff:ff:ff:ff:ff
    altname enp3s0
    inet 192.168.66.160/24 brd 192.168.66.255 scope global noprefixroute ens160
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fe8a:ab36/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
[root@localhost ~]#
```

#### 7、测试网络
```
[root@localhost ~]# ping -c 3 www.baidu.com
PING www.a.shifen.com (220.181.38.149) 56(84) bytes of data.
64 bytes from 220.181.38.149 (220.181.38.149): icmp_seq=1 ttl=127 time=47.1 ms
64 bytes from 220.181.38.149 (220.181.38.149): icmp_seq=2 ttl=127 time=47.7 ms
64 bytes from 220.181.38.149 (220.181.38.149): icmp_seq=3 ttl=127 time=30.1 ms

--- www.a.shifen.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 6126ms
rtt min/avg/max/mdev = 30.088/41.608/47.688/8.150 ms
[root@localhost ~]#
```