### 📝 Sysbench压测系统cpu、内存等
使用 Sysbench 压测内存和 CPU，使其利用率维持在 50% 左右，需要根据系统资源情况动态调整测试参数。以下是具体步骤和方法。

#### 1. 压测 CPU 并控制利用率
#### 1.1 压测 CPU 的基本命令
```
sysbench cpu --cpu-max-prime=20000 run
--cpu-max-prime：计算的最大质数，值越大，CPU 负载越高。
```

#### 1.2 控制 CPU 利用率
```
目标：将 CPU 利用率维持在 50% 左右。
方法：
使用 top 或 htop 监控 CPU 利用率。
调整 --cpu-max-prime 参数，降低或增加计算负载。
使用 --threads 参数控制并发线程数。
示例：
sysbench cpu --cpu-max-prime=10000 --threads=2 run
如果 CPU 利用率过高，降低 --cpu-max-prime 或减少 --threads。
如果 CPU 利用率过低，增加 --cpu-max-prime 或增加 --threads。
```

#### 1.3 动态调整
```
使用脚本动态调整参数，使 CPU 利用率维持在 50% 左右：
#!/bin/bash
TARGET_UTILIZATION=50
while true; do
    CURRENT_UTILIZATION=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}')
    if (( $(echo "$CURRENT_UTILIZATION < $TARGET_UTILIZATION" | bc -l) )); then
        sysbench cpu --cpu-max-prime=20000 --threads=4 run &
    else
        pkill sysbench
    fi
    sleep 5
done
```

### 2. 压测内存并控制利用率
#### 2.1 压测内存的基本命令
```
sysbench memory --memory-block-size=1K --memory-total-size=10G run
--memory-block-size：每次操作的内存块大小。
--memory-total-size：总操作内存大小。
```

#### 2.2 控制内存利用率
```
目标：将内存利用率维持在 50% 左右。
方法：
使用 free -m 或 top 监控内存利用率。
调整 --memory-total-size 参数，控制总内存使用量。
示例：
sysbench memory --memory-block-size=1K --memory-total-size=5G run
如果内存利用率过高，减少 --memory-total-size。
如果内存利用率过低，增加 --memory-total-size。
```
#### 2.3 动态调整
```
使用脚本动态调整参数，使内存利用率维持在 50% 左右：
#!/bin/bash
TARGET_UTILIZATION=50
TOTAL_MEMORY=$(free -m | awk '/^Mem:/{print $2}')
while true; do
    CURRENT_UTILIZATION=$(free -m | awk '/^Mem:/{print $3/$2 * 100}')
    if (( $(echo "$CURRENT_UTILIZATION < $TARGET_UTILIZATION" | bc -l) )); then
        sysbench memory --memory-block-size=1K --memory-total-size=${TOTAL_MEMORY}M run &
    else
        pkill sysbench
    fi
    sleep 5
done
```

### 3. 同时压测 CPU 和内存
#### 3.1 使用多个 Sysbench 实例
```
启动 CPU 压测：
sysbench cpu --cpu-max-prime=10000 --threads=2 run
启动内存压测：
sysbench memory --memory-block-size=1K --memory-total-size=5G run
```

#### 3.2 动态调整
```
使用脚本同时控制 CPU 和内存利用率：
#!/bin/bash
TARGET_CPU_UTILIZATION=50
TARGET_MEMORY_UTILIZATION=50
TOTAL_MEMORY=$(free -m | awk '/^Mem:/{print $2}')

while true; do
    CURRENT_CPU_UTILIZATION=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}')
    CURRENT_MEMORY_UTILIZATION=$(free -m | awk '/^Mem:/{print $3/$2 * 100}')

    if (( $(echo "$CURRENT_CPU_UTILIZATION < $TARGET_CPU_UTILIZATION" | bc -l) )); then
        sysbench cpu --cpu-max-prime=10000 --threads=2 run &
    else
        pkill sysbench
    fi

    if (( $(echo "$CURRENT_MEMORY_UTILIZATION < $TARGET_MEMORY_UTILIZATION" | bc -l) )); then
        sysbench memory --memory-block-size=1K --memory-total-size=${TOTAL_MEMORY}M run &
    else
        pkill sysbench
    fi

    sleep 5
done
```