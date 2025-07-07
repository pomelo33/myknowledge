## 🚀 java程序启停脚本
### 🔧 1.启动脚本
```
#!/bin/bash
# 设置Java的路径
JAVA_HOME="/usr/local/java"
JAVA="$JAVA_HOME/bin/java"

# 设置应用的根目录和Jar文件名
APP_HOME="/path/to/your/app"   # 应用的安装目录
APP_NAME="app.jar"

# JVM 参数
JAVA_OPTS="-Xms512m -Xmx1024m -XX:+UseG1GC"

# 应用参数（根据需要添加）
APP_OPTS=""

# 日志文件路径
LOG_DIR="$APP_HOME/logs"
LOG_FILE="$LOG_DIR/app.log"

# 检查日志目录是否存在，不存在则创建
if [ ! -d "$LOG_DIR" ]; then
  mkdir -p "$LOG_DIR"
fi

# 启动命令
START_CMD="$JAVA $JAVA_OPTS -jar $APP_HOME/$APP_NAME $APP_OPTS"
echo "Starting $APP_NAME..."
nohup $START_CMD > "$LOG_FILE" 2>&1 &
# 获取启动的进程ID
PID=$!

# 将进程ID写入pid文件
echo $PID > "$APP_HOME/app.pid"
echo "$APP_NAME started with PID $PID. Logs are in $LOG_FILE"

# 延迟几秒以确保应用开始写入日志 
sleep 3
# 实时查看日志文件
 tail -f "$LOG_FILE"
```
> 说明
> - JAVA_HOME：设置 Java 安装路径。
> - APP_HOME：应用根目录，包含 Jar 文件。
> - JAVA_OPTS：JVM 启动参数，可根据需要调整内存、GC 等参数。
> - APP_OPTS：应用运行参数。
> - LOG_DIR 和 LOG_FILE：日志存放路径和文件。
> - 使用 nohup 和 & 后台运行程序，并将输出重定向到日志文件中。
> - 脚本会在应用根目录下生成一个 app.pid 文件，用来存储 Java 进程 ID，方便后续管理

### 🔧 2.停止脚本
```
#!/bin/bash
# 设置应用的根目录
APP_HOME="/path/to/your/app"  # 应用的安装目录
PID_FILE="$APP_HOME/app.pid"

# 检查pid文件是否存在
if [ ! -f "$PID_FILE" ]; then
  echo "PID file not found! Is the application running?"
  exit 1
fi

# 获取进程ID
PID=$(cat "$PID_FILE")

# 检查进程是否存在
if ps -p $PID > /dev/null 2>&1; then
  echo "Stopping application with PID $PID..."
  kill $PID

  # 等待进程终止
  sleep 3

  # 确认进程已终止
  if ps -p $PID > /dev/null 2>&1; then
    echo "Failed to stop application gracefully. Forcing shutdown..."
    kill -9 $PID
  fi

  echo "Application stopped."

  # 删除pid文件
  rm -f "$PID_FILE"
else
  echo "No process found with PID $PID. Application may already be stopped."
  rm -f "$PID_FILE"  # 删除无效的pid文件
fi
```
> 说明
> - PID_FILE：启动脚本中创建的 app.pid 文件路径。
> - kill $PID：使用 kill 命令发送终止信号以停止应用。
> - sleep 3：等待几秒以确保进程能正常退出。
> - kill -9 $PID：如果进程没有正常终止，使用 kill -9 强制关闭进程。
> - 删除 app.pid 文件，以防止无效的 PID 文件残留。