#!/bin/bash

# 获取当前时间，作为日志文件名
timestamp=$(date +"%Y%m%d_%H%M%S")

# 指定日志目录
log_dir="./logs"
mkdir -p "$log_dir"

# 运行 Python 脚本并重定向输出
python examples/main.py > "$log_dir/$timestamp.log" 2>&1
