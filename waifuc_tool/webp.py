# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 18:52:06 2023
@author: rezer
"""

import os
import concurrent.futures
from PIL import Image
from tqdm import tqdm


def resize_image(source_path, target_dir):
    # 构建目标文件路径
    target_path = os.path.join(
        target_dir,
        os.path.relpath(os.path.dirname(source_path), source_dir),
        os.path.basename(source_path),
    )

    # 创建目标文件夹
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    # 读取图片文件
    image = Image.open(source_path)

    # 获取短边长度
    width, height = image.size
    short_side = min(width, height)

    # 保存图片
    target_path = os.path.splitext(target_path)[0] + ".webp"
    image.save(target_path, "webp", quality=90)

    remove_sourse_file = False
    if remove_sourse_file:
        os.remove(source_path)


def resize_images(source_dir, target_dir):
    # 获取源文件夹下的所有文件
    files = []
    for root, dirs, filenames in os.walk(source_dir):
        for filename in filenames:
            # 检查文件类型是否为png/jpg
            if filename.lower().endswith(".png") or filename.lower().endswith(".jpg"):
                files.append(os.path.join(root, filename))

    # 使用多线程进行文件读取和图片处理
    with concurrent.futures.ThreadPoolExecutor() as executor:
        total_files = len(files)
        progress_bar = tqdm(total=total_files, desc="Processing Images")
        futures = [executor.submit(resize_image, file, target_dir) for file in files]
        for future in concurrent.futures.as_completed(futures):
            progress_bar.update(1)
        progress_bar.close()


# 设置源文件夹和目标文件夹路径
source_dir = r"E:\waifuc\data\柯南"
target_dir = r"E:\waifuc\data\柯南_new"

# 调用函数进行图片处理和保存
resize_images(source_dir, target_dir)
