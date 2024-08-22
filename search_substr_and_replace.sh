#!/bin/bash

# 定义文件夹路径
folder_path="/home/fzy/Downloads/..."

# 读取文件夹中的所有文件
for file in "$folder_path"/*; do
  # 检查文件名中是否包含"OTA"
  if echo "$file" | grep -q "OTA"; then
    # 构建新的文件名，替换"OTA"为"Mpc"
    new_file=$(echo "$file" | sed 's/OTA/Mpc/g')
    # 重命名文件
    mv "$file" "$new_file"
    # 输出重命名的结果
    echo "Renamed '$file' to '$new_file'"
  fi
done
