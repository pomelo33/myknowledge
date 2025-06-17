### 📝 删除lvm


`思路：`
`需要提前把数据备份好，然后依次删除`
* 逻辑卷
* 卷组
* 物理卷

#### 1.取消挂载
```shell
[root@uos01 ~]# umount /funlyp-lv01 
```
#### 2.删除逻辑卷mylv01
```shell
[root@uos01 ~]# lvremove /dev/myvg01/mylv01
Do you really want to remove active logical volume myvg01/mylv01? [y/n]: y
  Logical volume "mylv01" successfully removed.

[root@uos01 ~]# lvs /dev/myvg01
  LV     VG     Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  mylv02 myvg01 -wi-a----- 400.00m                                                    
  mylv03 myvg01 -wi-a-----   7.30g   
已成功删除逻辑卷mylv01，此时查看还有卷组myvg01上还存在两个逻辑卷。
```

#### 3.删除卷组myvg01
```shell
直接删除卷组，会提示先删除卷组下的逻辑卷，然后再删除卷组。
[root@uos01 ~]# vgremove myvg01 
Do you really want to remove volume group "myvg01" containing 2 logical volumes? [y/n]: y
Do you really want to remove active logical volume myvg01/mylv02? [y/n]: y
  Logical volume "mylv02" successfully removed.
Do you really want to remove active logical volume myvg01/mylv03? [y/n]: y
  Logical volume "mylv03" successfully removed.
  Volume group "myvg01" successfully removed
```
#### 4.删除物理卷
```shell
查看本机上的物理卷pv
[root@uos01 ~]# pvs
  PV         VG  Fmt  Attr PSize   PFree 
  /dev/sda3  uos lvm2 a--  <23.50g     0 
  /dev/sdb       lvm2 ---   10.00g 10.00g
  /dev/sdc       lvm2 ---   10.00g 10.00g
  /dev/sde       lvm2 ---   10.00g 10.00g

删除物理卷/dev/sdb /dev/sdc /dev/sde
[root@uos01 ~]# pvremove /dev/sdb /dev/sdc /dev/sde
  Labels on physical volume "/dev/sdb" successfully wiped.
  Labels on physical volume "/dev/sdc" successfully wiped.
  Labels on physical volume "/dev/sde" successfully wiped.

查看lvm相关信息，是否还有残留
[root@uos01 ~]# lvs
  LV   VG  Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  root uos -wi-ao---- <17.50g                                                    
  swap uos -wi-ao----   4.00g                                                    
  var  uos -wi-ao----   2.00g                                                    
[root@uos01 ~]# 
[root@uos01 ~]# pvs
  PV         VG  Fmt  Attr PSize   PFree
  /dev/sda3  uos lvm2 a--  <23.50g    0 
[root@uos01 ~]# 
[root@uos01 ~]# vgs
  VG  #PV #LV #SN Attr   VSize   VFree
  uos   1   3   0 wz--n- <23.50g    0 
```