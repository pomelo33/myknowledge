## 🚀 gitlab登录密码重置
### 1.使用 Rake 任务 
#### 登录到 GitLab 服务器：
> 通过 SSH 以具有 sudo 权限的用户身份登录到你的 GitLab 服务器。执行 Rake 任务：
```
运行以下命令。它会提示你输入 root 用户的用户名 (如果 root 用户名没有被更改过，默认就是 root)，以及两次新密码。
sudo gitlab-rake "gitlab:password:reset"

当你运行这个命令后，会看到类似以下的提示：
Enter username: root  # 输入 root
Enter new password:   # 输入你的新密码 (输入时不会显示字符)
Confirm new password: # 再次输入新密码
Password successfully updated for user with username root.
```
尝试登录：  
现在，可以尝试使用新的 root 密码登录 GitLab 的 Web 界面了。