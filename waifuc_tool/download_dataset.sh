
#!/bin/bash

roles=("hakurei_reimu" "kirisame_marisa" "remilia_scarlet" "flandre_scarlet" "izayoi_sakuya" "konpaku_youmu" "patchouli_knowledge" "cirno" "alice_margatroid" "kochiya_sanae" "yakumo_yukari" "komeiji_koishi" "fujiwara_no_mokou" "reisen_udongein_inaba" "shameimaru_aya" "hong_meiling" "inubashiri_momiji" "komeiji_satori" "saigyouji_yuyuko" "kazami_yuuka" "reiuji_utsuho")

for role in "${roles[@]}"
do
    # 下载文件
    wget "https://huggingface.co/datasets/CyberHarem/${role}_touhou/resolve/main/dataset-1200.zip" -P "/root/autodl-tmp/dongfang"

    # 解压文件
    unzip "/root/autodl-tmp/dongfang/dataset-1200.zip" -d "/root/autodl-tmp/dongfang/${role}_marisa_touhou"

    # 删除压缩文件
    rm "/root/autodl-tmp/dongfang/dataset-1200.zip"
done
