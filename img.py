import sys
import uuid
import os
import random
from PIL import Image, PngImagePlugin
from tqdm import tqdm

# 导入webuiapi模块
import webuiapi

# 初始化WebUIApi对象，指定服务器地址、端口、采样器和步数
api = webuiapi.WebUIApi(host="127.0.0.1", port=6006, sampler="DPM++ 2M Karras", steps=20)

# 指定路径
parent_folder = "/root/autodl-tmp/genshin124/genshin_nohair"
output_folder = "/root/sdwebuiapi/imgs"
num_images_per_folder = 2  # 每个文件夹要生成的图片数量

# 获取所有子文件夹
subfolders = [folder for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))]

# 显示进度条
progress_bar = tqdm(total=len(subfolders) * num_images_per_folder, desc="Generating Images")

for subfolder in subfolders:
    # 子文件夹路径
    subfolder_path = os.path.join(parent_folder, subfolder)

    # 获取路径下所有的txt文件
    txt_files = [os.path.join(subfolder_path, file) for file in os.listdir(subfolder_path) if file.endswith(".txt")]

    # 随机选择指定数量的txt文件
    random_txt_files = random.sample(txt_files, num_images_per_folder)

    for txt_file in random_txt_files:
        # 读取txt文件内容作为prompt参数
        with open(txt_file, "r") as f:
            prompt = f.read().strip()

        lora = ",<lora:genshin_pony_v2:1>"
        # 调用api的txt2img方法
        result = api.txt2img(
            prompt=prompt + lora,
            negative_prompt="wings, nsfw, low quality, worst quality, normal quality,",
            seed=-1,
            cfg_scale=7,
            width=1024,
            height=1024,
        )

        # 获取文件夹名作为文件名
        folder_name = os.path.basename(subfolder_path)
        # 构建保存路径
        output_path = os.path.join(output_folder, f"{folder_name}.png")

        # 首先，复制图像，以避免在原始图像上进行更改
        img_copy = result.image.copy()

        # 创建一个新的meta对象，将参数作为文本添加到meta中
        meta = PngImagePlugin.PngInfo()
        parameters = f"{result.info['infotexts'][0]}"
        meta.add_text("parameters", parameters)

        # 将图像保存为PNG格式，并将信息作为文本区块添加
        img_copy.save(output_path, format="PNG", pnginfo=meta)

        # 更新进度条
        progress_bar.update(1)

progress_bar.close()
print(f"Generation completed. Images saved in {output_folder}")
