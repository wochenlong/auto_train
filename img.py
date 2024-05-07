import os
import json
import re
from PIL import Image, PngImagePlugin
from tqdm import tqdm
import webuiapi

def safetensors_metadata_parser(file_path):
    header_size = 8
    meta_data = {}
    if os.stat(file_path).st_size > header_size:
        with open(file_path, "rb") as f:
            b8 = f.read(header_size)
            if len(b8) == header_size:
                header_len = int.from_bytes(b8, 'little', signed=False)
                headers = f.read(header_len)
                if len(headers) == header_len:
                    meta_data = sorted(json.loads(headers.decode("utf-8")).get("__metadata__", meta_data).items())
    return meta_data

blacklist = ["solo", "2girls", "twitter_username", "artist_name", "signature","official_art","looking_at_viewer", "male_focus", "full_body",
             "blush", "simple_background", "white_background", "smile", "open_mouth", "highres", "commentary_request",
             "absurdres", "closed_mouth", "cowboy_shot", "upper_body", "sitting", "standing", "commentary", "hand_up",
             "outdoors","indoors,","food","day","nipples","ass","legs"，"armpits"]  # 黑名单列表

def filter_keywords(keywords_list):
    filtered_list = []
    for keyword in keywords_list:
        keyword = keyword.strip()
        if any(keyword.startswith(prefix) for prefix in ["holding", "eat", "from","looking","vision"]) or \
                any(keyword.endswith(suffix) for suffix in ["background","nude", "up", "id","commentary","text","ing","cross","work","field","sky","frame"]):
            continue
        filtered_list.append(keyword)
    return filtered_list

def get_keywords(safetensors_file, top_20=True):
    metadatas = safetensors_metadata_parser(safetensors_file)
    _dict = {}
    for a, b in metadatas:
        if a == "ss_tag_frequency":
            tags = b
            try:
                json_obj = json.loads(tags)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                return
            for key, value in json_obj.items():
                key = re.search(r"_(.*)", key).group(1)
                max_value = max(value.values())
                value_white = {zi: zi_value for zi, zi_value in value.items() if zi not in blacklist}
                filtered_keywords = filter_keywords(value_white.keys())
                keywords = []
                if top_20:
                    keywords = filtered_keywords[:20]
                else:
                    for zi in filtered_keywords:
                        zi_value = value_white[zi]
                        if zi_value / max_value > 0.5:
                            keywords.append(zi)
                _dict[key] = keywords
            return _dict

def main(lora_file):
    api = webuiapi.WebUIApi(host="127.0.0.1", port=6006, sampler="Euler a", steps=20)
    output_folder = "/root/autodl-tmp/current/pony114514"
    os.makedirs(output_folder, exist_ok=True)  # 创建输出目录
    keywords = get_keywords(lora_file)
    progress_bar = tqdm(total=len(keywords), desc="Generating Images")
    for character, keywords_list in keywords.items():
        prompt = ", ".join(keywords_list)
        lora_name = os.path.basename(lora_file)
        lora_name = os.path.splitext(lora_name)[0]
        lora = f", <lora:{lora_name}:1>"
        result = api.txt2img(
            prompt="score_9,score_8_up,score_7_up," + prompt + lora,
            negative_prompt="score_4,score_5,score_6,lowres,nsfw, low quality, worst quality, normal quality,",
            seed=-1,
            cfg_scale=7,
            width=768,
            height=1216,
        )
        output_path = os.path.join(output_folder, f"{character}.png")
        img_copy = result.image.copy()
        meta = PngImagePlugin.PngInfo()
        parameters = f"{result.info['infotexts'][0]}"
        meta.add_text("parameters", parameters)
        img_copy.save(output_path, format="PNG", pnginfo=meta)
        progress_bar.update(1)
    progress_bar.close()
    print(f"Generation completed. Images saved in {output_folder}")

lora_file = r"/root/autodl-tmp/stable-diffusion-webui/models/Lora/genshin_pony_v3.safetensors"
main(lora_file)
