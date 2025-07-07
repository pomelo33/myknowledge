## 🚀 redis数据快速写入脚本
### 脚本内容
```bash
#!/bin/bash
DCS_HOST="192.168.10.100"
DCS_PORT="6379"
DCS_PASS="admin123"
KEY_PREFIX="memfill:"
DATA_SIZE_MB=1
TTL=86400
TOTAL_MEMORY=$((4 * 1024 * 1024 * 1024))
TARGET_MEMORY=$((TOTAL_MEMORY / 2))
# 获取redis当前内存使用量
current_used=$(redis-cli -h $DCS_HOST -p $DCS_PORT -a $DCS_PASS --no-auth-warning info memory | grep "used_memory:" | awk -F: '{print $2}'|tr -d '\r')
if [ -z "$current_used" ]; then
  echo "错误：无法获取DCS内存信息，请检查连接配置！"
  exit 1
fi
#redis需要快速写入的数据量
needed_bytes=$((TARGET_MEMORY - current_used))
if [ $needed_bytes -le 0 ]; then
  echo "内存已达标（当前使用：$((current_used / 1024 / 1024))MB），无需操作"
  exit 0
fi

num_keys=$(( (needed_bytes + (1024*1024 - 1)) / (1024*1024) ))
echo "目标填充: $((needed_bytes / 1024 / 1024))MB | 需插入 $num_keys 条数据（每条1MB）"
# 开始写入数据
start_time=$(date +%s)
for i in $(seq 1 $num_keys); do
  key="${KEY_PREFIX}$(date +%s%N)_$i"
  value=$(head -c 786431 /dev/urandom | base64 -w 0)
  
  if (( i % 10 == 0 )); then
    echo "SETEX $key $TTL $value" | redis-cli -h $DCS_HOST -p $DCS_PORT -a $DCS_PASS --no-auth-warning >/dev/null 2>&1
    progress=$((i * 100 / num_keys))
    echo -ne "进度: $i/$num_keys ($progress%) | 已写入: $((i * DATA_SIZE_MB))MB\r"
  else
    echo "SETEX $key $TTL $value" >> /tmp/redis_pipe.txt
  fi
done

if [ -f /tmp/redis_pipe.txt ]; then
  cat /tmp/redis_pipe.txt | redis-cli -h $DCS_HOST -p $DCS_PORT -a $DCS_PASS --no-auth-warning >/dev/null 2>&1
  rm -f /tmp/redis_pipe.txt
fi
final_used=$(redis-cli -h $DCS_HOST -p $DCS_PORT -a $DCS_PASS --no-auth-warning info memory | grep "used_memory:" | awk -F: '{print $2}' | tr -d '\r')
echo -e "\n操作完成！最终内存使用: $((final_used / 1024 / 1024))MB | 耗时: $(( $(date +%s) - start_time ))秒"
```

### 检测脚本
```bash
#!/bin/bash
DCS_HOST="192.168.10.100"
DCS_PORT="6379"
DCS_PASS="admin123"
KEY_PREFIX="memfill:"
DATA_SIZE_MB=1
TTL=86400
TOTAL_MEMORY=$((4 * 1024 * 1024 * 1024))
TARGET_MEMORY=$((TOTAL_MEMORY / 2))
current_used=$(redis-cli -h $DCS_HOST -p $DCS_PORT -a $DCS_PASS --no-auth-warning info memory | grep "used_memory:" | awk -F: '{print $2}'| td -d '\r')
current_ratio=$(awk "BEGIN {printf \"%.2f\", $current_used / $TOTAL_MEMORY * 100}")
if (( $(echo "$current_ratio < 47" | bc -l) )); then
  echo "$(date) - 当前使用率 ${current_ratio}% 低于47%，触发填充..."
  test.sh >> /var/log/dcs_maintain.log
elif (( $(echo "$current_ratio > 53" | bc -l) )); then
  echo "$(date) - 当前使用率 ${current_ratio}% 高于53%，触发清理..."
  redis-cli -h $DCS_HOST -p $DCS_PORT -a $DCS_PASS --no-auth-warning --scan --pattern "${KEY_PREFIX}*" | head -n 100 | xargs redis-cli del >/dev/null
else
  echo "$(date) - 使用率正常（${current_ratio}%）"
fi
```