import os

def add_prefix(directory, prefix):
    for root, dirs, files in os.walk(directory):
        for file_name in dirs:
            old_path = os.path.join(root, file_name)
            new_name = prefix + file_name
            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed {old_path} to {new_path}")

def remove_prefix(directory, prefix):
    for root, dirs, files in os.walk(directory):
        for file_name in dirs:
            if file_name.startswith(prefix):
                old_path = os.path.join(root, file_name)
                new_name = file_name.replace(prefix, "", 1)  # 仅替换一次前缀
                new_path = os.path.join(root, new_name)
                os.replace(old_path, new_path)
                print(f"Renamed {old_path} to {new_path}")

# 指定目录路径
directory = "/root/data/Genshin_all"

# 选择功能
function = "remove"  # 可以修改为 "remove" 来执行删除前缀的操作

# 执行选择的功能
if function == "add":
    add_prefix(directory, "1_")
    print("已添加前缀")
elif function == "remove":
    remove_prefix(directory, "1_")
    print("已删除前缀")
