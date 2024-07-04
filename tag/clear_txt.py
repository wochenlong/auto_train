import os

def delete_txt_without_image(folder_path):
    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            txt_file = os.path.join(folder_path, filename)
            image_file = os.path.join(folder_path, os.path.splitext(filename)[0])
            # 检查是否存在同名的图片文件
            if not any([os.path.isfile(image_file + ext) for ext in [".webp", ".jpeg",".jpg", ".png"]]):
                # 删除没有同名图片文件的txt文件
                os.remove(txt_file)
                print(f"Deleted {txt_file}")

# 指定文件夹路径
folder_path = r"C:\Users\PC\Downloads\魔道\train\wangji_new"
delete_txt_without_image(folder_path)
