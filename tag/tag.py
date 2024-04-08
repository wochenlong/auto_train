import os
import re
import sys

# 获取命令行参数
args = sys.argv[1:]
# 提取工作目录参数
work_dir = args[0]

# 遍历目录中的所有文件
for filename in os.listdir(work_dir):
    # 检查文件是否是文本文件
    if filename.endswith(".txt"):
        file_path = os.path.join(work_dir, filename)
        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # 处理每一行
        processed_lines = []
        for line in lines:
            # 按,分割内容
            split_content = [x.strip() for x in line.split(",")]
            # 去除重复内容
            unique_content = list(set(split_content))
            # 正则匹配结尾为hair/eyes/bangs/horn的内容并删除
            pattern = re.compile(r"(.*?)(hair|eyes|pupils|bangs|braid|bun|ears|horns|twintails|ahoge|hair_ornament|tail|halo )$", re.IGNORECASE)
            filtered_content = [x for x in unique_content if not pattern.search(x)]
            # 组合成以", "分割的内容
            processed_line = ", ".join(filtered_content)
            processed_lines.append(processed_line)

        # 写回原来的txt文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(processed_lines)

print("处理完成。")
