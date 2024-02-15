import os
import json
import argparse

def process_txt_file(input_file):
    # 读取 txt 文件
    with open(input_file, 'r') as f:
        content = f.read().strip()

    # 检查是否存在同名图片文件
    img_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    img_files = [input_file.replace('.txt', ext) for ext in img_extensions if os.path.exists(input_file.replace('.txt', ext))]

    if len(img_files) == 0:
        return
    elif len(img_files) > 1:
        print("发现多个同名不同后缀的图片文件:")
        for img_file in img_files:
            print(img_file)
        print("请处理后重试")
        return

    img_path = img_files[0]

    # 构建数据结构
    data = {}
    data['img_path'] = img_path
    data['general_tags'] = content.split('\n')
    data['character_tags'] = [] #后续增加处理方法
    data['series_tags'] = []    #后续增加处理方法
    data['artist_tags'] = []    #后续增加处理方法

    # 写入 JSON 文件
    output_json = input_file.replace('.txt', '.json')
    with open(output_json, 'w') as f:
        json.dump(data, f, indent=4)

def process_txt_files_in_folder(folder_path):
    # 处理目录下的所有 txt 文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            input_file = os.path.join(folder_path, filename)
            process_txt_file(input_file)
            os.remove(input_file)

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='TXT to JSON converter')
    parser.add_argument('input', help='the input file or folder')
    args = parser.parse_args()

    # 处理单个文件或目录
    if os.path.isfile(args.input):
        process_txt_file(args.input)
    elif os.path.isdir(args.input):
        process_txt_files_in_folder(args.input)
