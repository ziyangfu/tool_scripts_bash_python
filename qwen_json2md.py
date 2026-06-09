#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON 聊天导出文件转 Markdown 工具
支持 Python 3.8+
按 timestamp 时间戳排序输出对话
"""
import json
import os
import sys
from datetime import datetime

def parse_qwen_json(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Qwen 导出的 JSON 通常是一个列表，每个元素代表一个话题/会话
        for conversation_group in data:
            # 1. 提取标题 (title)
            topic_title = conversation_group.get('title', '未命名对话')
            
            all_messages = []
            chat_data = conversation_group.get('chat', {})
            history = chat_data.get('history', {})
            messages_map = history.get('messages', {})

            # 遍历消息映射表
            for msg_id, msg_body in messages_map.items():
                role = msg_body.get('role')
                # 获取基础时间戳，若无则设为 0
                ts = msg_body.get('timestamp', 0)
                
                # 处理用户消息
                if role == 'user':
                    content = msg_body.get('content', '')
                    if content:
                        all_messages.append({
                            'role': 'User',
                            'content': content,
                            'timestamp': ts
                        })
                
                # 处理助手消息
                elif role == 'assistant':
                    content_list = msg_body.get('content_list', [])
                    
                    if content_list:
                        for item in content_list:
                            # 严格过滤：仅提取 phase 为 answer 的内容，跳过 thinking_summary
                            if item.get('phase') == 'answer':
                                text = item.get('content', '')
                                item_ts = item.get('timestamp', ts)
                                if text:
                                    all_messages.append({
                                        'role': 'Assistant',
                                        'content': text,
                                        'timestamp': item_ts
                                    })
                    else:
                        # 兼容模式：直接提取 content
                        text = msg_body.get('content', '')
                        if text:
                            all_messages.append({
                                'role': 'Assistant',
                                'content': text,
                                'timestamp': ts
                            })

            # 2. 按照时间戳进行排序，确保对话流顺畅
            all_messages.sort(key=lambda x: x['timestamp'])

            # 3. 写入 Markdown 文件
            with open(output_file, 'w', encoding='utf-8') as f:
                # 插入提取到的标题
                f.write(f"# {topic_title}\n\n")
                f.write(f"> 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for msg in all_messages:
                    role_label = f"### 👤 {msg['role']}" if msg['role'] == 'User' else f"### 🤖 {msg['role']}"
                    f.write(f"{role_label}\n\n")
                    f.write(f"{msg['content']}\n\n")
                    f.write("---\n\n")

        print(f"转换成功！标题: '{topic_title}' 已提取，输出文件: {output_file}")

    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python qwen_json2md.py <input_json_file>")
    else:
        input_path = sys.argv[1]
        # 默认输出文件名与输入文件同名但后缀为 .md
        output_path = os.path.splitext(input_path)[0] + ".md"
        parse_qwen_json(input_path, output_path)