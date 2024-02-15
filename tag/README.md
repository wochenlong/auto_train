[I don't understand Chinese, show me in English](#README)
# 说明文档

根据 civitai 的 Chenkin（风吟）要求编写，用于处理标签。

目前通过处理 waifuc 的 json 来实现。代码将去除角色特征，画师名后创建标签。

如果需要使用由 wd14 创建的内容，而不是使用 danbooru 的提示，请使用 tags2json 先将 txt 转换为 json，然后再使用 json2tags。这样使用将只能去除'角色特征'而无法处理艺术家名以及角色、系列名。

tags2json 后续会增加根据路径来增加艺术家名以及角色、系列名等的逻辑。

json2tag 的生成格式为：special_tag（如 1girl）+ character_tag（角色名）+ series_tag（系列名）+ artist_tag（作者名）+ generate_tag（常规）。  
其中 'special_tag' 默认保留，'艺术家名' 默认删除，'角色特征' 默认删除。  
可以通过使用 --del_special、--keep_artist、--keep_characteristic 来修改。

waifuc 使用示例：
```bash
# 查看帮助
python json2tags.py -h

# 常规使用
python json2tags.py your/path/to/jsons

# 保留艺术家名与角色特征
python json2tags.py your/path/to/jsons --keep_artist --keep_characteristic
```

非 waifuc 使用示例：
```bash
# 代码会删除原有 prompt 的 txt，请在小数据集上尝试后再在大数据集上尝试
python tags2json.py your/path/to/txts
python json2tags.py your/path/to/txts --no_waifuc
```

> 角色特征的删除依赖tags与words。  
> tags为完全相同匹配，words为末尾相同匹配。  
> 角色特征的tags与words并不完全完整，如果你发现其他的可以加入的tags或words，请提issue。

---
# README

Written at the request of Chenkin from civitai for tag processing purposes.

Currently achieved through processing waifuc's JSON. The code will remove character features and create tags after the artist's name.

If you need to use content created by wd14 instead of using prompts from danbooru, use tags2json to convert txt to json first before using json2tags. This way, only 'character features' can be removed, and it cannot handle artist names as well as character and series names.

Tags2json will later add logic to add artist names, character names, series names, etc., based on the path.

The generated format of json2tag is: special_tag (such as 1girl) + character_tag (character name) + series_tag (series name) + artist_tag (artist name) + generate_tag (general).  
Where 'special_tag' is kept by default, 'artist name' is deleted by default, and 'character features' are deleted by default.  
Modifications can be made using --del_special, --keep_artist, --keep_characteristic.

Usage example for waifuc:
```bash
# Get help
python json2tags.py -h

# Regular usage
python json2tags.py your/path/to/jsons

# Keep artist name and character features
python json2tags.py your/path/to/jsons --keep_artist --keep_characteristic
```

No-waifuc usage example:
```bash
# The code will delete the original prompt txt, please try on a small dataset first before trying on a large dataset
python tags2json.py your/path/to/txts
python json2tags.py your/path/to/txts --no_waifuc
```

> Deletion of character features depends on tags and words.
> Tags are for exact match, while words are for matching the end.  
> The tags and words for character features are not completely exhaustive. If you find any other tags or words that can be added, please raise an issue.
