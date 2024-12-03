# auto_train
风吟关于一键炼丹的各种好用小工具

画师标签与角色特征处理依赖于此项目：https://github.com/shiertier/xl_train_json2tag

## toml的使用

LORA
```
accelerate launch --dynamo_backend no --dynamo_mode default --mixed_precision fp16 --num_processes 1 --num_machines 1 --num_cpu_threads_per_process 2 /root/kohya_ss/sd-scripts/sdxl_train_network.py --config_file  /root/config_lora-20241101-192359.toml
```
DB
```
accelerate launch --dynamo_backend no --dynamo_mode default --mixed_precision bf16 --num_processes 1 --num_machines 1 --num_cpu_threads_per_process 2 /root/kohya_ss/sd-scripts/sdxl_train.py --config_file  /root/config_dreambooth-20241121-191436.toml     
```
# sdeval的使用
## 依赖安装
```
pip install collections  # 不需要单独安装，collections是Python标准库的一部分
pip install tags         # 假设tags是一个第三方库
pip install webuiapi
pip install tqdm
pip install pandas
pip install sdeval       # 这个应该包含了fidelity, controllability, corrupt子模块
```
## 运行sdeval
```
python  eval_lora.py
```
## 在autodl上运行运行sdeval

```
pip install openpyxl
```


```
HF_ENDPOINT=https://hf-mirror.com python eval_lora.py
```

xlsl 文件保存在python的实际运行目录

# 继续训练的脚本

指定目录中的每个子文件夹中随机抽取50张webp图片和同名的txt文件，并将它们复制到指定的目标文件夹中。
```
import os
import shutil
import random
from tqdm import tqdm

def copy_files(src_dir, dst_dir, num_files=50):
    # 确保目标目录存在
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # 获取所有子文件夹
    sub_dirs = [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]

    # 遍历每个子文件夹并处理文件
    for sub_dir in sub_dirs:
        sub_dir_path = os.path.join(src_dir, sub_dir)
        webp_files = [f for f in os.listdir(sub_dir_path) if f.endswith('.webp')]

        # 如果图片数量少于指定数量，则全部复制
        if len(webp_files) <= num_files:
            selected_files = webp_files
        else:
            selected_files = random.sample(webp_files, num_files)

        # 创建进度条
        with tqdm(total=len(selected_files), desc=f"Copying from {sub_dir}", unit="file") as pbar:
            for webp_file in selected_files:
                base_name = os.path.splitext(webp_file)[0]
                txt_file = base_name + '.txt'

                # 复制 .webp 文件
                src_webp_path = os.path.join(sub_dir_path, webp_file)
                dst_webp_path = os.path.join(dst_dir, webp_file)
                shutil.copy2(src_webp_path, dst_webp_path)

                # 复制 .txt 文件
                src_txt_path = os.path.join(sub_dir_path, txt_file)
                dst_txt_path = os.path.join(dst_dir, txt_file)
                if os.path.exists(src_txt_path):
                    shutil.copy2(src_txt_path, dst_txt_path)

                # 更新进度条
                pbar.update(1)

if __name__ == "__main__":
    src_directory = r'F:\data\all\arknights\arknights_0.9'
    dst_directory = r'F:\data\all\arknights\v1_86'
    copy_files(src_directory, dst_directory)
```
