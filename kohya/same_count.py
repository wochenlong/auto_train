import os
import re
import math

def count_image_files_in_folder(folder):
    image_extensions = ['.webp', '.png', '.jpg', '.jpeg', '.gif']  # 根据需要添加更多格式
    return sum(1 for file in os.listdir(folder) if any(file.lower().endswith(ext) for ext in image_extensions))

def rename_and_update_folders(folder_path, image_limit=1000,image_min_limit=50):
    for root, dirs, files in os.walk(folder_path, topdown=False):  
        if not dirs:  
            image_count = count_image_files_in_folder(root)
            if image_count > 0 and image_count >= image_min_limit:  
                base_name = os.path.basename(root)
                folder_name_parts = base_name.split('_', 1) 
                if len(folder_name_parts) > 1 and folder_name_parts[0].isdigit():
                    new_prefix = max(1, math.ceil(image_limit / image_count))
                    new_folder_name = f"{new_prefix}_{folder_name_parts[1]}"
                else:
                    new_prefix = max(1, math.ceil(image_limit / image_count))
                    new_folder_name = f"{new_prefix}_{base_name}"
                
                new_folder_path = os.path.join(os.path.dirname(root), new_folder_name)
                os.rename(root, new_folder_path)
                print(f"'{root}' 有 '{image_count}' 张图片，已重命名为 '{new_folder_path}'")
            else: 
                print(f"'{root}' 有 '{image_count}' 张图片，少于'{image_min_limit}' 张，不进行重命名")

# 设置目标文件夹路径
folder_path = r"F:\data\all\blue_archive\test"
image_limit=200   #平衡基准数量
image_min_limit=30 # 图片数量大于多少进行重命名，可根据需求选择
rename_and_update_folders(folder_path,image_limit,image_min_limit)
