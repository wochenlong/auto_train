#!/bin/bash

roles=("konpaku_youmu_(ghost)" "kaenbyou_rin" "yakumo_ran" "kawashiro_nitori" "moriya_suwako" "rumia" "chen" "kamishirasawa_keine" "hinanawi_tenshi" "tatara_kogasa" "inaba_tewi" "mystia_lorelei" "nazrin" "mizuhashi_parsee" "koakuma" "ibuki_suika" "houraisan_kaguya" "yagokoro_eirin" "daiyousei" "houjuu_nue")

failed_downloads=()

for role in "${roles[@]}"
do
    # 下载文件
    wget "https://huggingface.co/datasets/CyberHarem/${role}_touhou/resolve/main/dataset-1200.zip" -P "/root/autodl-tmp/dongfang2"

    # 检查下载是否成功
    if [ $? -ne 0 ]; then
        failed_downloads+=("${role}")
    else
        # 解压文件
        unzip "/root/autodl-tmp/dongfang2/dataset-1200.zip" -d "/root/autodl-tmp/dongfang2/${role}"

        # 删除压缩文件
        rm "/root/autodl-tmp/dongfang2/dataset-1200.zip"
    fi
done

# 检查无法下载的链接或文件
if [ ${#failed_downloads[@]} -gt 0 ]; then
    echo "以下链接或文件下载失败："
    for failed in "${failed_downloads[@]}"
    do
        echo "${failed}"
    done
else
    echo "所有文件下载完成！"
fi
