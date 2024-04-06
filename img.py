import sys
import uuid
from PIL import Image, PngImagePlugin
# 导入webuiapi模块
import webuiapi
# 初始化WebUIApi对象，指定服务器地址、端口、采样器和步数
api = webuiapi.WebUIApi(use_https=True,host='u59632-8216-74ceddf4.westb.seetacloud.com', port=8443, sampler="Euler a", steps=28)
提示词列表 = ["ganyu", "miku"]
lora = ",<lora:Sakimichan:1>"
for 提示词 in 提示词列表:
    # 调用api的txt2img方法
    result = api.txt2img(
        prompt="1girl, souryuu asuka langley, neon genesis evangelion"+lora,
        negative_prompt="wings, nsfw, low quality, worst quality, normal quality,",
        seed=-1,
        cfg_scale=7,
        width=1024,
        height=1024,
    )

   # 生成随机文件名
random_filename = f"image_{uuid.uuid4()}.png"
# 首先，复制图像，以避免在原始图像上进行更改
img_copy = result.image.copy()
# 创建一个新的meta对象，将参数作为文本添加到meta中
meta = PngImagePlugin.PngInfo()
parameters = f"{result.info['infotexts'][0]}"
meta.add_text("parameters", parameters)

# 将图像保存为PNG格式，并将信息作为文本区块添加
img_copy.save(random_filename, format="PNG", pnginfo=meta)
print(f"Image saved as {random_filename}")
