#!/bin/bash

# 启动所有的python脚本
for file in /app/*.py; do
  python "$file" &
done

# 等待所有脚本运行
wait