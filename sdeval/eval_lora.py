# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 05:11:31 2024

@author: rezer
"""
import os
from collections import Counter
from tags import gen_tag, gen_test_image
import webuiapi
from tqdm import tqdm
import pandas as pd
from sdeval.fidelity import CCIPMetrics
from sdeval.controllability import BikiniPlusMetrics
from sdeval.corrupt import AICorruptMetrics
import os

os.environ["onnx_mode"] = "cpu"
#os.environ["https_proxy"] = "http://192.168.1.100:7890"


class eval_lora:
    def __init__(self, lora_name_list: list, lora_train_dir: str, trigger_dir: str):
        self.lora_name_list = lora_name_list  # 测试lora名字列表
        self.lora_train_dir = lora_train_dir  # 测试lora训练集地址
        self.trigger_dir = trigger_dir  # 测试文件存放目录
        self.get_core_tag()

    def get_core_tag(
        self,
    ):  # 获取一个列表，其中self.trigger_word被赋值为一个列表，为核心触发词
        self.lora_test_tags = []  # 一个列表，每个子项都是一个txt caption文件的全部内容
        for root, dirs, files in os.walk(self.lora_train_dir):
            for filename in files:
                if filename.endswith(".txt"):
                    file_path = os.path.join(root, filename)
                    with open(file_path, "r", encoding="utf-8") as file:
                        self.lora_test_tags.append(file.read().replace("\\", ""))
        self.text_file_count = len(self.lora_test_tags)
        all_txt_contents_list = [
            x.strip() for x in ",".join(self.lora_test_tags).split(",")
        ]  # 所有词组成一个清单
        self.lora_tags_count = Counter(all_txt_contents_list)  # 词频统计字典
        self.trigger_word = []  # 触发词组成的列表。
        for key in self.lora_tags_count.keys():
            if self.lora_tags_count[key] >= 0.9 * self.text_file_count:
                self.trigger_word.append(key)
        print("核心关键字为：", self.trigger_word)

    def set_api(self, api):
        self.api = api

    def test_a_lora(self, lora_name):
        print(f"正在测试{lora_name}")
        except_save_image_dir = os.path.join(self.trigger_dir, lora_name)
        if not os.path.exists(except_save_image_dir):
            os.makedirs(except_save_image_dir)
            print(f"测试目录已生成{except_save_image_dir}")
        run_lora_list = gen_tag(
            lora_name=lora_name, core_tag=",".join(self.trigger_word)
        )
        print("核心tag获取，准备开始出图")
        for run in tqdm(run_lora_list):
            if not os.path.exists(
                os.path.join(except_save_image_dir, run["filename"] + ".png")
            ):
                gen_test_image(
                    api=self.api,
                    prompt=run["prompt"],
                    seed=run["seed"],
                    save_file_path=os.path.join(
                        except_save_image_dir, run["filename"] + ".png"
                    ),
                )
            else:
                print("检测到图片存在，跳过")

    def test_all_lora(self):
        for lora_name in self.lora_name_list:
            self.test_a_lora(lora_name=lora_name)

    def get_test_report(
        self,
    ):

        report_name = self.lora_name_list[0]
        print(f"准备生成{report_name}测试报告，初始化CCIP参数")
        ccip = CCIPMetrics(images=self.lora_train_dir)  #
        bp = BikiniPlusMetrics(
            tag_blacklist=[
                "bangs",
                "long_hair",
                "blue_eyes",
                "animal_ears",
                "sleeveless",
                "breasts",
                "grey_hair",
                "medium_breasts",
            ]
        )
        metrics = AICorruptMetrics()
        print("参数初始化完成")
        test_list = []

        for lora_name in self.lora_name_list:
            print(f"评估模型{lora_name}")
            lora_sample_dir = os.path.join(self.trigger_dir, lora_name)
            ccip_score = ccip.score(lora_sample_dir)
            metrics_score = metrics.score(lora_sample_dir)
            bp_score = bp.score(lora_sample_dir)

            lora_report = [lora_name, ccip_score, metrics_score, bp_score]
            test_list.append(lora_report)
        df = pd.DataFrame(test_list)
        df.columns = ["lora_name", "ccip", "ai-c", "bp-score"]
        df.to_excel(f"{report_name}.xlsx")


# api = webuiapi.WebUIApi(host='10.0.0.223', port=7860) #webuiapi
api = webuiapi.WebUIApi(host="127.0.0.1", port=7860)  # webuiapi
profile = (
    {
        "sd_model_checkpoint": r"animagine-xl-3.0.safetensors [1449e5b0b9]",
        "sd_vae": "none",
    },
)
api.set_options(profile)

# a=eval_lora(lora_name_list=[
#     "shiro_(no_game_no_life)",
#                             "shiro_(no_game_no_life)-000022",
#                             "shiro_(no_game_no_life)-000020",
#                             "shiro_(no_game_no_life)-000018",
#                             "shiro_(no_game_no_life)-000016",
#                             "shiro_(no_game_no_life)-000014",
#                             "shiro_(no_game_no_life)-000012",
#                             "shiro_(no_game_no_life)-000010",
#                             "shiro_(no_game_no_life)-000008",
#                             "shiro_(no_game_no_life)-000006",
#                             "shiro_(no_game_no_life)-000004",
#                             "shiro_(no_game_no_life)-000002",],
#             lora_train_dir=r"G:\lora_train\train\shiro_(no_game_no_life)\1_1girl",
#             trigger_dir=r"G:\lora_train\sample\shiro_(no_game_no_life)"
#             )
# a.set_api(api=api)
# a.test_all_lora()
# a.get_test_report()

# a=eval_lora(lora_name_list=[
#                             "diana",
#                             "diana-000022",
#                             "diana-000020",
#                             "diana-000018",
#                             "diana-000016",
#                             "diana-000014",
#                             "diana-000012",
#                             "diana-000010",
#                             "diana-000008",
#                             "diana-000006",
#                             "diana-000004",
#                             "diana-000002",],
#             lora_train_dir=r"H:\lora_train\diana\train\diana\1_girl",
#             trigger_dir=r"G:\lora_train\sample\diana"
#             )
# a.set_api(api=api)
# a.test_all_lora()
# a.get_test_report()

a = eval_lora(
    lora_name_list=[
        "kafka_1k.safetensors",
        "kafka_1k-000010.safetensors",
   
    ],
    lora_train_dir=r"/root/data/new/1111/star_rail/kafka_1k",  # 测试路径
    trigger_dir=r"/root/windsing/output/kafuka",  # 输出测试文件目录
)
a.set_api(api=api)
a.test_all_lora()
a.get_test_report()
