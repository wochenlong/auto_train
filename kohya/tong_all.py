import os
import re
from collections import Counter

directory = r"F:\data\all\touhou\touhou_146\touhou_145"  # 指定目录路径
blacklist = ["solo", "looking_at_viewer", "blush", "simple_background", "white_background", "smile", "open_mouth", "commentary_request", "highres"]  # 黑名单列表

output_file_path = r"F:\data\all\touhou\touhou_146\touhou_145\result_1.txt"  # 指定输出结果的txt文件路径

# 遍历目录下的文件夹
with open(output_file_path, "w", encoding="utf-8") as output_file:
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            folder_name = re.sub(r"^\d+_|\d+_", "", folder)
            output_file.write(f"角色名: {folder_name}\n")

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
            # 过滤黑名单并获取前20个高频词
            top_words = [word.strip() for word, count in word_count.most_common() if word.strip() not in blacklist]
            top_words = top_words[:20]  # 只保留前20个

            # 将1girl和1boy放在前面
            prioritized_words = [word for word in top_words if word in ["1girl", "1boy"]]
            other_words = [word for word in top_words if word not in prioritized_words]
            final_top_words = prioritized_words + other_words

            top_words_str = ", ".join(final_top_words)

            output_file.write("核心触发词:\n")
            output_file.write(top_words_str + "\n\n")
