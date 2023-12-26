import os.path

from waifuc.action import ThreeStageSplitAction, FilterSimilarAction, TaggingAction
from waifuc.export import TextualInversionExporter
from waifuc.source import LocalSource

# 定义源目录列表
src_dirs = [
   "/root/windsing/data/星穹铁道/青雀/5_青雀",
     "/root/windsing/data/星穹铁道/藿藿/10_藿藿",
        "/root/windsing/data/星穹铁道/seele/5_seele",
        "/root/windsing/data/星穹铁道/lade/2_lade",
]

# 定义目标数据集的根目录
dst_root_dir = 'test_datasets'

# 遍历每个源目录
for src_dir in src_dirs:
    # 创建目标目录路径，通过将根目录和源目录的基本名称进行拼接
    dst_dir = os.path.join(dst_root_dir, os.path.basename(src_dir))
    
    # 创建当前源目录的 LocalSource 对象
    source = LocalSource(src_dir)
    
    # 将所需的操作附加到源上
    source.attach(
        ThreeStageSplitAction(),
        FilterSimilarAction(),
        TaggingAction(
            force=True,
            character_threshold=1.01,  # 如果不需要字符标记，请移除此行
        )
    ).export(TextualInversionExporter(dst_dir))
