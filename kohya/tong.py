import os
import re
from collections import Counter

directory = r"E:\data\角色\ALL\genshin"  # 指定目录路径
blacklist = ["solo", "looking_at_viewer", "blush", "simple_background", "white_background", "smile", "open_mouth"]  # 黑名单列表

# 遍历目录下的文件夹
for folder in os.listdir(directory):
    folder_path = os.path.join(directory, folder)
    if os.path.isdir(folder_path):
        folder_name = re.sub(r"^\d+_|\d+_", "", folder)
        print(f"角色名: {folder_name}")

        words = []

        # 遍历文件夹中的txt文件
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if file.endswith(".txt") and os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        # 使用英文逗号","划分单词
                        word_list = line.split(",")
                        words.extend(word_list)

        # 统计单词频率
        word_count = Counter(words)
        top_words = [word.strip() for word, count in word_count.most_common(10) if word.strip() not in blacklist]

        top_words_str = ", ".join(top_words)

        print("核心触发词:")
        print(top_words_str)
        print()
