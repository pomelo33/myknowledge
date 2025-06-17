## 🔧 Sysbench
Sysbench 是一款开源的多功能性能测试工具，广泛用于测试数据库、CPU、内存、文件系统和线程等性能。它支持多种数据库（如 MySQL、PostgreSQL）和多种测试模式，是数据库性能测试和基准测试的常用工具。

### 1、安装
```
curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.rpm.sh | sudo bash
sudo yum -y install sysbench
```
### 2、Sysbench 基本用法
#### 2.1 常用命令格式
`sysbench [options] [testname] [command]`
- testname：测试类型（如 cpu、memory、fileio、oltp）。
- command：测试阶段（如 prepare、run、cleanup）。
- options：测试参数。

#### 2.2 常用测试类型
- CPU 测试：测试 CPU 性能。
- 内存测试：测试内存性能。
- 文件 I/O 测试：测试文件系统性能。
- OLTP 测试：测试数据库性能（如 MySQL）。

#### 2.3 常用命令
- 准备阶段（prepare）：初始化测试数据。
- 运行阶段（run）：执行性能测试。
- 清理阶段（cleanup）：清理测试数据。

### 3、测试场景

#### 3.1 CPU 性能测试
```
测试命令：
sysbench cpu --cpu-max-prime=20000 run
参数说明：
--cpu-max-prime：计算的最大质数，值越大，CPU 负载越高。
输出结果：
事件数（events per second）：每秒完成的计算次数。
```
#### 3.2 内存性能测试
```
测试命令：
sysbench memory --memory-block-size=1K --memory-total-size=10G run
参数说明：
--memory-block-size：每次操作的内存块大小。
--memory-total-size：总操作内存大小。
输出结果：
传输速率（MiB/sec）：每秒传输的内存数据量。
```
#### 3.3 文件 I/O 性能测试
```
准备阶段：
<BASH>
sysbench fileio --file-total-size=10G prepare
测试命令：
sysbench fileio --file-total-size=10G --file-test-mode=rndrw run
清理阶段：
sysbench fileio --file-total-size=10G cleanup
参数说明：
--file-total-size：测试文件的总大小。
--file-test-mode：测试模式（如 seqwr 顺序写、rndrw 随机读写）。
输出结果：
读写速率（MiB/sec）：每秒读写的数据量。
```
#### 3.4 OLTP 数据库性能测试
```
准备阶段：
sysbench oltp_read_write --db-driver=mysql --mysql-host=localhost --mysql-port=3306 --mysql-user=root --mysql-password=123456 --mysql-db=test --table-size=1000000 prepare
测试命令：
sysbench oltp_read_write --db-driver=mysql --mysql-host=localhost --mysql-port=3306 --mysql-user=root --mysql-password=123456 --mysql-db=test --table-size=1000000 --threads=16 --time=60 run
清理阶段：
sysbench oltp_read_write --db-driver=mysql --mysql-host=localhost --mysql-port=3306 --mysql-user=root --mysql-password=123456 --mysql-db=test --table-size=1000000 cleanup
参数说明：
    --db-driver：数据库驱动（如 mysql、pgsql）。
    --mysql-host：MySQL 服务器地址。
    --mysql-port：MySQL 服务器端口。
    --mysql-user：MySQL 用户名。
    --mysql-password：MySQL 密码。
    --mysql-db：测试数据库名称。
    --table-size：测试表的数据量。
    --threads：并发线程数。
    --time：测试持续时间（秒）。

输出结果：
事务数（transactions per second）：每秒完成的事务数。
延迟（latency）：每个操作的平均延迟。
在使用 Sysbench 对 MySQL 进行压测时，测试结果会输出详细的性能指标。这些指标可以帮助我们分析数据库的性能瓶颈和优化方向。以下是对 MySQL 压测结果 的详细解析。
```
### 压测结果输出示例
#### 1.输出结果
```
以下是一个典型的 Sysbench OLTP 测试结果输出：
SQL statistics:
    queries performed:
        read: 100000
        write: 50000
        other: 20000
        total: 170000
    transactions: 10000 (166.66 per sec)
    latency (ms): 60.00
    errors: 0
    reconnects: 0

General statistics:
    total time: 60.0001s
    total number of events: 10000

Latency (ms):
         min: 10.00
         avg: 60.00
         max: 200.00
         95th percentile: 100.00
         sum: 600000.00

Threads fairness:
    events (avg/stddev): 625.0000/25.00
    execution time (avg/stddev): 60.0000/0.00
```
#### 2. 结果详解
##### 2.1 SQL 统计（SQL statistics）
- queries performed：
    - read：执行的读查询数量。
    - write：执行的写查询数量。
    - other：执行的其他查询数量（如事务提交、回滚）。
    - total：所有查询的总数。
- transactions：
    - 总事务数，括号内为 每秒事务数（TPS）。
    - 示例：10000 (166.66 per sec) 表示总共执行了 10000 个事务，平均每秒 166.66 个事务。
- latency (ms)：
    - 每个事务的平均延迟（毫秒）。
    - 示例：60.00 表示每个事务的平均响应时间为 60 毫秒。
- errors：
    - 测试期间发生的错误数。
    - 示例：0 表示没有错误。
- reconnects：
    - 测试期间的重连次数。
    - 示例：0 表示没有重连。

##### 2.2 总体统计（General statistics）
- total time：
    - 测试的总时间（秒）。
    - 示例：60.0001s 表示测试持续了 60 秒。
- total number of events：
    - 总事件数（即总事务数）。
    - 示例：10000 表示总共执行了 10000 个事务。

##### 2.3 延迟统计（Latency）
- min：
    -   最小延迟（毫秒）。
    - 示例：10.00 表示最快的事务响应时间为 10 毫秒。
- avg：
    - 平均延迟（毫秒）。
    - 示例：60.00 表示事务的平均响应时间为 60 毫秒。
- max：
    - 最大延迟（毫秒）。
    - 示例：200.00 表示最慢的事务响应时间为 200 毫秒。
- 95th percentile：
    - 95% 的事务延迟（毫秒）。
    - 示例：100.00 表示 95% 的事务响应时间在 100 毫秒以内。
- sum：
    - 所有事务的总延迟（毫秒）。
    - 示例：600000.00 表示所有事务的响应时间总和为 600000 毫秒。

##### 2.4 线程公平性（Threads fairness）
- events (avg/stddev)：
    - 每个线程的平均事件数和标准差。
    - 示例：625.0000/25.00 表示每个线程平均执行了 625 个事件，标准差为 25。
- execution time (avg/stddev)：
    - 每个线程的平均执行时间和标准差。
    - 示例：60.0000/0.00 表示每个线程的平均执行时间为 60 秒，标准差为 0。
