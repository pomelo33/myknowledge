#!/bin/bash
declare -A counter

for i in {1..20}; do
  resp=$(curl -s http://localhost)
  echo $resp
  ((counter["$resp"]++))
done

echo "=== 汇总统计 ==="
for key in "${!counter[@]}"; do
  echo "$key 被请求 ${counter[$key]} 次"
done