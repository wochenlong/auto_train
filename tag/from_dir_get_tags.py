#该脚本未经测试
import os
import json
import argparse

# 创建参数解析器
parser = argparse.ArgumentParser(description='Process JSON files in a directory.')

# 添加参数
parser.add_argument('directory', help='The root directory to process')

# 解析命令行参数
args = parser.parse_args()

# 获取命令行参数值
root_directory = args.directory

# 遍历所有子目录
for dirpath, dirnames, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename.endswith('.json'):
            json_path = os.path.join(dirpath, filename)
            with open(json_path, 'r') as f:
                data = json.load(f)
                if not data['character_tags'] and not data['series_tags']:
                    last_dir_name = os.path.basename(dirpath)
                    second_last_dir_name = os.path.basename(os.path.dirname(dirpath))
                    data['character_tags'].append(last_dir_name)
                    data['series_tags'].append(second_last_dir_name)
                    with open(json_path, 'w') as f:
                        json.dump(data, f)
