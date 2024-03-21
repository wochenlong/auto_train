import os
from waifuc.action import *
from waifuc.export import *
from waifuc.source import *
from subprocess import run

if __name__ == "__main__":
    save_path = r"E:\data\角色\nieta\MAN\nakahara_chuuya\1_bu_new"
    source = LocalSource(r"E:\data\角色\nieta\MAN\nakahara_chuuya\1_bu")
    source = source.attach(
        FilterSimilarAction('all'),  # 再次丢弃相似或重复的图像
        FileExtAction(ext='.webp', quality=90),
        TaggingAction(force=True),
        TagOverlapDropAction(),
        FirstNSelectAction(500)  # 当已有500张图像到达此步骤时，停止后继图像处理
    )
    source.export(TextualInversionExporter(save_path))

    # Add prefix to the content of each TXT file in the save_path directory
    prefix = 'nakahara_chuuya' # 为txt 添加前缀

    # Get the list of TXT files in the save_path directory
    txt_files = [f for f in os.listdir(save_path) if f.endswith('.txt')]

    # Add the prefix to the content of each TXT file
    for file_name in txt_files:
        file_path = os.path.join(save_path, file_name)

        # Read the content of the TXT file
        with open(file_path, 'r') as file:
            content = file.read()

        # Add the prefix to the content
        content_with_prefix = f"{prefix}, {content}"

        # Write the modified content back to the TXT file
        with open(file_path, 'w') as file:
            file.write(content_with_prefix)

    print("触发词已加入!")
