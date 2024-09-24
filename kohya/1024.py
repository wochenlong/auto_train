from PIL import Image  
import os  
from tqdm import tqdm  # 引入tqdm库  
import shutil  # 引入shutil库以便复制文件

# 设定源文件夹和目标文件夹路径  
source_folder = r'D:\ai\reg\xxx'  # 请根据实际情况修改路径  
target_folder = r'D:\ai\reg\xxx_new'  # 请根据实际情况修改路径  

# 确保目标文件夹存在  
if not os.path.exists(target_folder):  
    os.makedirs(target_folder)  
  
# 用于存储加载时出问题的文件名  
failed_files = []  
  
# 遍历源文件夹中的所有文件，并使用tqdm显示进度条  
for filename in tqdm(os.listdir(source_folder), desc='处理文件', total=len(os.listdir(source_folder))):  
    # 处理图像文件  
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):  
        img_path = os.path.join(source_folder, filename)  
          
        try:  
            with Image.open(img_path) as img:  
                width, height = img.size  
                  
                # 确定短边并计算新尺寸  
                if width < height:  
                    new_width = 1024  
                    new_height = int(height * (1024 / width))  
                else:  
                    new_height = 1024  
                    new_width = int(width * (1024 / height))  
                  
                # 调整图片大小  
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)  
                  
                # 保存为PNG  
                target_path = os.path.join(target_folder, filename)  
                resized_img.save(target_path, 'PNG')  
        except (OSError, IOError) as e:  
            failed_files.append(filename)  
            print(f"警告：图片 {filename} 损坏或无法加载，已跳过，错误：{e}")  
        except Exception as e:  
            failed_files.append(filename)  
            print(f"警告：处理图片 {filename} 时发生未知错误，已跳过，错误：{e}")  

    # 处理文本文件  
    elif filename.lower().endswith('.txt'):  
        src_txt_path = os.path.join(source_folder, filename)  
        target_txt_path = os.path.join(target_folder, filename)  
        
        # 复制文本文件到目标文件夹  
        try:  
            shutil.copy(src_txt_path, target_txt_path)  
        except Exception as e:  
            print(f"警告：复制文本文件 {filename} 时发生错误，已跳过，错误：{e}")  
            
# 脚本完成后输出加载时出问题的文件名  
if failed_files:  
    print("以下文件在加载时出了问题：")  
    for file in failed_files:  
        print(file)  
else:  
    print("所有图片处理完毕，没有文件在加载时出现问题。")  
  
print("图片压缩并保存为PNG完成（不包括处理时出问题的文件）！")
print("文本文件复制完成！")
