import os  
import sys  
  
def replace_chars_in_files(folder_path):  
    # 确保提供的路径确实是一个目录  
    if not os.path.isdir(folder_path):  
        print(f"错误：'{folder_path}' 不是一个有效的目录。")  
        return  
  
    # 遍历指定文件夹  
    for root, dirs, files in os.walk(folder_path):  
        for file in files:  
            # 检查文件是否以.txt结尾  
            if file.endswith(".txt"):  
                file_path = os.path.join(root, file)  
                  
                # 读取文件内容  
                with open(file_path, 'r', encoding='utf-8') as f:  
                    content = f.read()  
                  
                # 替换下划线和反斜杠  
                modified_content = content.replace('_', ' ').replace('\\', '')  
                  
                # 将修改后的内容写回文件  
                with open(file_path, 'w', encoding='utf-8') as f:  
                    f.write(modified_content)  
  
if __name__ == "__main__":  
    # 检查命令行参数数量  
    if len(sys.argv) != 2:  
        print("使用方法：python clear_tag.py folder_path")  
        sys.exit(1)  
  
    # 获取命令行提供的文件夹路径  
    folder_path = sys.argv[1]  
  
    # 调用函数处理文件  
    replace_chars_in_files(folder_path)  
  
    print("所有的空格和转义已被处理！")
