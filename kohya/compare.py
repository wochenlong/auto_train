#!/bin/bash

train_data_dirs=(
"/root/data/ka"
"/root/data/ka2"
)

output_dirs=(
"/root/stable-diffusion-webui/models/Lora/tianqi"
"/root/stable-diffusion-webui/models/Lora/tianqi2"
)

output_names=(
"tianqi"
"tianqi2"
)

network_dims=(
4
8
)

network_alphas=(
2
4
)

for ((i=0; i<${#train_data_dirs[@]}; i++))
do
    accelerate launch --num_cpu_threads_per_process=2 "./sdxl_train_network.py" \
    --pretrained_model_name_or_path="/root/stable-diffusion-webui/models/Stable-diffusion/animagine-xl-3.0.safetensors" \
    --train_data_dir="${train_data_dirs[i]}" \
    --resolution="1024,1024" \
    --output_dir="${output_dirs[i]}" \
    --logging_dir="/root/windsing/logs" \
    --network_alpha=${network_alphas[i]} \  # 在这里设置network_alpha的值
    --training_comment="by chenkin" \
    --save_model_as=safetensors \
    --network_module=networks.lora \
    --text_encoder_lr=0.0002 \
    --unet_lr=0.0002 \
    --network_dim=${network_dims[i]} \
    --output_name="${output_names[i]}" \
    --lr_scheduler_num_cycles="10" \
    --no_half_vae \
    --learning_rate="0.0002" \
    --lr_scheduler="constant" \
    --train_batch_size="10" \
    --save_every_n_epochs="1" \
    --mixed_precision="fp16" \
    --save_precision="fp16" \
    --seed="12345" \
    --caption_extension=".txt" \
    --cache_latents \
    --optimizer_type="AdamW8bit" \
    --max_train_epochs=10 \
    --max_data_loader_n_workers="0" \
    --clip_skip=2 \
    --bucket_reso_steps=32 \
    --save_last_n_steps_state="1" \
    --gradient_checkpointing \
    --xformers \
    --noise_offset=0.0357 \
    --sample_sampler=euler_a \
    --sample_prompts="/root/kohya_ss/sample_prompts.txt" \
    --sample_every_n_epochs="1" \
    --save_state \
    --cache_latents_to_disk
done
