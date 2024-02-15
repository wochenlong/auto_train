import os,re,json
import argparse
from tqdm import tqdm

# 确保json文件存在对应图片
def find_matching_image(json_file, waifuc):
    dirname = os.path.dirname(json_file)
    basename = os.path.basename(json_file)
    filename, ext = os.path.splitext(basename)
    if waifuc:
        filename = (filename.split("_meta")[0]).split(".")[1]
    image_extensions = (".webp", ".jpg", ".jpeg", ".png", ".gif")

    for ext in image_extensions:
        image_file = os.path.join(dirname, filename + ext)
        if os.path.exists(image_file):
            return True  # 如果找到匹配的图像文件，立即返回True

    return False  # 如果循环结束后没有找到匹配的图像文件，返回False

def get_txt_path(json_file, waifuc):
    dirname = os.path.dirname(json_file)
    basename = os.path.basename(json_file)
    filename, ext = os.path.splitext(basename)
    if waifuc:
        filename = (filename.split("_meta")[0]).split(".")[1]
    txt_file = os.path.join(dirname, filename + ".txt")
    return txt_file

def find_matching_txt(json_file, waifuc):
    txt_file = get_txt_path(json_file, waifuc)
    return os.path.exists(txt_file)

def split_tags(tags,waifuc,split=","):
    if waifuc:
        split=" "
    tags_set = set()
    tags = tags.split(split)

    for tag in tags:
        tag = tag.strip()  # 去除首尾空格
        if tag:
            tags_set.add(tag)

    return tags_set

def compare_and_update_sets(general_set, special_tags_ex):
    special_set = set()
    common_tags = general_set.intersection(special_tags_ex)
    special_set.update(common_tags)
    general_set.difference_update(common_tags)

def process_prompt(json_file, waifuc, del_characteristic=True, del_artist=True, del_special=False):
    with open(json_file, 'r', encoding='utf-8') as f: 
        data = json.load(f)
    if waifuc:
        # 获取tag信息
        tag_general = data['danbooru']['tag_string_general']
        tag_character = data['danbooru']['tag_string_character']
        tag_copyright = data['danbooru']['tag_string_copyright']
        tag_artist = data['danbooru']['tag_string_artist']

    else:
        tag_general = ", ".join(data['general_tags'])
        tag_character = ", ".join(data['character_tags'])
        tag_copyright = ", ".join(data['series_tags'])
        tag_artist = ", ".join(data['artist_tags'])
    general_set = split_tags(tag_general,waifuc)
    character_set = split_tags(tag_character,waifuc)
    series_set = split_tags(tag_copyright,waifuc)
    artist_set = split_tags(tag_artist,waifuc)
    special_tags_ex = {"1girl", "2girls", "3girls", "4girls", "5girls", "6+girls", "multiple girls", "multiple_girls",
                "1boy", "2boys", "3boys", "4boys", "5boys", "6+boys", "multiple boys", "male focus","multiple_boys", "male_focus"}
    special_set = set()
    special_tags = general_set.intersection(special_tags_ex)
    special_set.update(special_tags)
    general_set.difference_update(special_tags)

    if del_characteristic:
        general_set = process_general(general_set)

    if del_special:
        special_set.clear()

    if del_artist:
        artist_set.clear()

    all_tags = list(special_set) + list(character_set) + list(series_set) + list(artist_set) + list(general_set)
    tags_str = ", ".join(all_tags)
    txt_path = get_txt_path(json_file, waifuc)
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(tags_str)

def get_filter_tags(filter_tags_file):
    # 读取文件内容
    with open(filter_tags_file, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # 去除分隔符并组成合集
    result_set = set()
    for line in lines:
        line = line.strip()
        if line != '——————' and line != '————————————————————':
            result_set.add(line)
    return result_set

def generate_patterns(words_set):
    patterns = []

    for word in words_set:
        pattern = r'^.*(\b|_)' + re.escape(word) + r'$'
        patterns.append(pattern)

    return patterns

def process_general(general_set):
    # 删除以 words 为结尾的内容
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    words = get_filter_tags(os.path.join(script_dir,"words.txt"))
    regs = generate_patterns(words)
    filter_tags = get_filter_tags(os.path.join(script_dir,"tags.txt"))
    filtered_set = general_set.copy()
    to_be_removed = []  # 用于存储待删除的元素
    for item in general_set:
        for pattern in regs:
            if re.match(pattern, item):
                to_be_removed.append(item)
                break
            if item in filter_tags:
                to_be_removed.append(item)
                break
    for item in to_be_removed:
        filtered_set.remove(item)  # 删除待删除元素
    return filtered_set

def main(root_dir, waifuc=True, del_characteristic=True, del_artist=True, del_special=False):
    for folder_name, subfolders, filenames in tqdm(os.walk(root_dir), desc="Processing"):
        for filename in filenames:
            if filename.endswith(".json"):
                json_file = os.path.join(folder_name, filename)
                matching_image = find_matching_image(json_file, waifuc)
                matching_txt = find_matching_txt(json_file, waifuc)
                if matching_image and not matching_txt:
                    process_prompt(json_file, waifuc, del_characteristic, del_artist, del_special)
                else:
                    print(f"{filename}无需处理")
                    continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从json文件中获取prompt.")
    parser.add_argument("root_dir", type=str, help="处理路径")
    parser.add_argument("--no_waifuc", action="store_true", help="非waifuc情况下使用,需配合另一个代码（暂未实现）")
    parser.add_argument("--keep_characteristic", action="store_true", help="保留角色特征")
    parser.add_argument("--keep_artist", action="store_true", help="保留艺术家名")
    parser.add_argument("--del_special", action="store_true", help="删除特殊项，ex:1girl")

    args = parser.parse_args()

    waifuc = not args.no_waifuc
    del_characteristic = not args.keep_characteristic
    del_artist = not args.keep_artist
    del_special = args.del_special

    main(args.root_dir, waifuc=waifuc, del_characteristic=del_characteristic, del_artist=del_artist, del_special=del_special)
