# history_manager.py

import json
import os
from threading import Lock

# 使用线程锁来防止多线程同时读写文件导致数据错乱
file_lock = Lock()


def save_history(file_path: str, private_history: dict, group_history: dict):
    """
    将私聊和群聊的历史记录完整保存到JSON文件中。
    """
    with file_lock:
        try:
            full_history = {
                "private": private_history,
                "group": group_history
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(full_history, f, ensure_ascii=False, indent=4)
            print(f"聊天记录已成功保存到 {file_path}")
        except Exception as e:
            print(f"错误：保存聊天记录失败 - {e}")


def load_history(file_path: str) -> (dict, dict):
    """
    从JSON文件中加载历史记录。
    如果文件不存在或为空，返回两个空的字典。
    """
    with file_lock:
        if not os.path.exists(file_path):
            print(f"历史记录文件 {file_path} 不存在，将创建新的历史记录。")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
            f.close()
            return {}, {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                f.close()
                if not content:  # 处理文件为空的情况
                    print(f"历史记录文件 {file_path} 为空，将创建新的历史记录。")
                    return {}, {}
                data = json.loads(content)
                private_history = data.get("private", {})
                group_history = data.get("group", {})
                print(f"聊天记录已从 {file_path} 加载。")
                return private_history, group_history
        except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
            print(f"警告：加载聊天记录失败 - {e}。将使用空的聊天记录。")
            return {}, {}