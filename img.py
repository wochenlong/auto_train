import os,json,re
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

blacklist = ["solo", "looking_at_viewer", "blush", "simple_background", "white_background", "smile", "open_mouth","highres","commentary_request","absurdres","closed_mouth","cowboy_shot","upper_body",'artist_name']  # 黑名单列表

def get_keywords(safetensors_file,top_20=True):
    metadatas = safetensors_metadata_parser(safetensors_file)
    _dict = {}
    for a,b in metadatas:
        if a == "ss_tag_frequency":
            tags = b
            #转化为json
            try:
                json_obj = json.loads(tags)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                return
            for key, value in json_obj.items():
                #key等于第一个_之后的内容，通过re获得
                key = re.search(r"_(.*)", key).group(1)
                max_value = max(value.values())
                value_white = {zi: zi_value for zi, zi_value in value.items() if zi not in blacklist}
                for zi, zi_value in value_white.items():
                    keywords = []
                    if top_20:
                        # 获取最高value的前20个结果
                        keywords = [zi for zi, zi_value in sorted(value_white.items(), key=lambda item: item[1], reverse=True)[:20]]
                    else:
                        if zi_value / max_value > 0.5:
                            keywords.append(zi)
                _dict[key] = keywords
            return _dict

def main(lora_file):
    # 初始化WebUIApi对象，指定服务器地址、端口、采样器和步数
    api = webuiapi.WebUIApi(host="127.0.0.1", port=6006, sampler="DPM++ 2M Karras", steps=20)
    # 指定路径和文件名
    output_folder = "/root/autodl-tmp/current/img2"
    keywords=get_keywords(lora_file)
    # 显示进度条
    progress_bar = tqdm(total=len(keywords), desc="Generating Images")
    for character, keywords_list in keywords.items():
        # 提取关键词作为 prompt,使用“, ”隔开列表
        prompt = ", ".join(keywords_list)
        lora_name = os.path.basename(lora_file)
        lora_name = os.path.splitext(lora_name)[0]  # 去掉后缀名
        lora = f", <lora:{lora_name}:1>"
        # 调用api的txt2img方法
        result = api.txt2img(
            prompt="score_9,,"+prompt + lora,
            negative_prompt=" nsfw, low quality, worst quality, normal quality,",
            seed=-1,
            cfg_scale=7,
            width=1024,
            height=1024,
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

lora_file = r"/root/autodl-tmp/stable-diffusion-webui/models/Lora/genshin_pony_v2/genshin_pony_v2.safetensors"
main(lora_file)
