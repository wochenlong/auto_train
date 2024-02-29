from subprocess import run
from waifuc.action import *
from waifuc.export import *
from waifuc.source import *

if __name__ == "__main__":
    save_path = r"E:\data\Chunibyo\takanashi_rikka\1_p"

    # 通过gchar扩展包提供的数据源进行爬取
  
    s = DanbooruSource(["takanashi_rikka","solo"])
    tag_domains=['general', 'character'],

    # 爬取图像，处理它们，然后以给定的格式保存到目录中
    s.attach(
        # 以RGB色彩模式加载图像并将透明背景替换为白色背景
        ModeConvertAction("RGB", "white"),
        # 图像预过滤
        NoMonochromeAction(),  # 丢弃单色、灰度或素描等单色图像

        ClassFilterAction(["illustration", "bangumi"]),  # 丢弃漫画或3D图像
      #       RatingFilterAction(['safe', 'r15']),  # 可选，丢弃非全年龄或R15的图像
        # 人像处理
        #     FaceCountAction(1),  # 丢弃没有人脸或有多个人脸的图像
         #    PersonSplitAction(),  # 将多人图像中每个人物裁出
         #   FaceCountAction(1),  # 丢弃裁出内容中没有人脸或有多个人脸的图像
        # CCIP，丢弃内容为非指定角色的图像
   CCIPAction(),
        # 将短边大于800像素的图像等比例调整至短边为800像素
        AlignMinSizeAction(1024),
        # 使用wd14 v2进行标注，如果不需要角色标注，将character_threshold设置为1.01
        #  MirrorAction(),  # 可选，镜像处理图像进行数据增强
        FilterSimilarAction(),
        RandomFilenameAction(),  # 随机重命名图像
        #  ThreeStageSplitAction(),
        FirstNSelectAction(1000),  # 当已有10000张图像到达此步骤时，停止后继图像处理
         TagOverlapDropAction(),
        #   TaggingAction(force=True),
        FileExtAction(ext='.webp', quality=90)  # 按webp 90% 的质量保存
    ).export(
        # 保存到/data/surtr_dataset目录，可自行更改
         SaveExporter(save_path)
    ) 

    # 运行命令
    run(["python", r"E:\waifuc\xl_train_json2tag\json2tags.py", save_path, "--keep_characteristic"])
    run(["python", r"E:\waifuc\tag.py", save_path])
