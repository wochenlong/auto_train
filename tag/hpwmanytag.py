import os
from collections import Counter

folder_path = r'E:\data\角色\ALL\league_of_legends\1_all'
output_path = r'E:\data\角色\ALL\league_of_legends\output.txt'

# 遍历文件夹中的txt文件
words = []
league_of_legends_words = []
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    if file.endswith(".txt") and os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            word_list = content.split(",")
            words.extend(word_list)
            league_of_legends_words.extend([word for word in word_list if "league_of_legends" in word])

# 统计单词出现次数
word_counts = Counter(words)
league_of_legends_counts = Counter(league_of_legends_words)

# 按出现次数从高到低排序
sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
sorted_league_of_legends_counts = sorted(league_of_legends_counts.items(), key=lambda x: x[1], reverse=True)

# 输出结果到指定txt文件
with open(output_path, 'w', encoding='utf-8') as f:
    for word, count in sorted_league_of_legends_counts:
        f.write(f"{word}: {count}\n")
    for word, count in sorted_counts:
        if word not in league_of_legends_counts:
            f.write(f"{word}: {count}\n")
