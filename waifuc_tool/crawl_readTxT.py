import os
from waifuc.action import *
from waifuc.export import *
from waifuc.source import *
import pandas as pd

# 请将以下路径替换为自己的路径
output_path = r"/root/data/a3"
character_path = r"/root/waifuc/name.csv"

# 读取角色列表
df = pd.read_csv(character_path, header=None)
characters = df.values.tolist()

# 遍历角色列表,使用waifuc进行爬取
for character in characters:
    # 读取角色名和输出目录
    tag = character[0]
    output_dir = f'{tag}/1_{tag}'
    output_dir = os.path.join(output_path, output_dir)

    tag = "_".join(tag.strip().split(" "))

    # 通过gchar扩展包提供的数据源进行爬取
    s = GelbooruSource([tag])
    # 爬取图像，处理它们，然后以给定的格式保存到目录中
    s.attach(
        # 以RGB色彩模式加载图像并将透明背景替换为白色背景
        ModeConvertAction("RGB", "white"),
        # 图像预过滤
        NoMonochromeAction(),  # 丢弃单色、灰度或素描等单色图像
        ClassFilterAction(["illustration", "bangumi"]),  # 丢弃漫画或3D图像
        # RatingFilterAction(['safe', 'r15']),  # 可选，丢弃非全年龄或R15的图像
        PersonSplitAction(),  # 将多人图像中每个人物裁出
        # CCIP，丢弃内容为非指定角色的图像
        CCIPAction(),
        # 将短边大于800像素的图像等比例调整至短边为800像素
        AlignMinSizeAction(1024),
        # 使用wd14 v2进行标注，如果不需要角色标注，将character_threshold设置为1.01
        TaggingAction(force=True),
        FilterSimilarAction("all"),  # 再次丢弃相似或重复的图像
        FirstNSelectAction(50),  # 当已有200张图像到达此步骤时，停止后继图像处理
        # MirrorAction(),  # 可选，镜像处理图像进行数据增强
        RandomFilenameAction(),  # 随机重命名图像
        FileExtAction(ext='.webp', quality=90)  # 按webp 90% 的质量保存
    ).export(
        # 保存到/data/surtr_dataset目录，可自行更改
        TextualInversionExporter(output_dir)
    )
