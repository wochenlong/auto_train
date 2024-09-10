import os
import re
from collections import Counter

directory = r"F:\data\all\touhou\touhou_146\touhou_145"  # 指定目录路径
blacklist = ["solo", "looking_at_viewer","background","ID","blush", "smile", "mouth", "holding", "request", "fruit", "food", "highres", "absurdres"]  # 黑名单列表

output_file_path = r"F:\data\all\touhou\touhou_146\touhou_145\result_5.txt"  # 指定输出结果的txt文件路径

# 定义标签分类
def categorize_word(word):
    if any(tag in word for tag in ["hair", "bangs", "twintails", "pantyhose", "braid", "side_up", "bun"]):
        return "hair"
    elif "eye" in word:
        return "eye"
    elif any(tag in word for tag in ["skin", "horn", "ear", "breasts", "wings", "tail"]):
        return "body"
    elif any(tag in word for tag in ["halo", "ornament", "bow", "headwear", "mark", "shirt", "sleeves", "skirt", "apron", "dress", "kimono", "maid","clothes", "thighhighs", "pants", "hat", "cap", "vest", "ribbon", "scarf", "necklace", "bell"]):
        return "clothing"
    return "other"

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
            top_words = [
                word.strip() for word, count in word_count.most_common()
                if not any(black in word.strip().lower() for black in blacklist)
            ][:20]  # 只保留前20个高频词

            # 将1girl和1boy放在前面
            prioritized_words = [word for word in top_words if word in ["1girl", "1boy"]]
            other_words = [word for word in top_words if word not in prioritized_words]

            # 按标签分类
            categorized_words = {
                "main": [],
                "hair": [],
                "eye": [],
                "body": [],
                "clothing": [],
                "other": []
            }

            # 先添加频率最高的词
            if other_words:
                categorized_words["main"].append(other_words[0])  # 最高频词

            # 添加主体标签
            for word in other_words[1:]:
                if "girl" in word or "boy" in word:
                    categorized_words["main"].append(word)
                else:
                    category = categorize_word(word)
                    categorized_words[category].append(word)

            # 按顺序输出
            sorted_top_words = (
                categorized_words["main"] +
                categorized_words["hair"] +
                categorized_words["eye"] +
                categorized_words["body"] +
                categorized_words["clothing"] +
                categorized_words["other"]
            )

            top_words_str = ", ".join(sorted_top_words)

            output_file.write("核心触发词:\n")
            output_file.write(top_words_str + "\n\n")
