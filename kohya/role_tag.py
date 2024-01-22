import os

root_folder = '/root/data/Genshin_all'

# 遍历根文件夹下的所有子文件夹
for foldername in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, foldername)

    # 检查子文件夹是否为目录
    if os.path.isdir(folder_path):
        # 提取角色名作为标签
        _, tag = foldername.split('_', 1)

        # 遍历子文件夹内的所有txt文件
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                # 打开文件并添加标签
                with open(file_path, 'r+') as file:
                    content = file.read()
                    file.seek(0, 0)  # 将文件指针移动到文件开头
                    file.write(tag + ' ' + content)
