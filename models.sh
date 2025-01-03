#!/bin/bash

# Base directory for COMFY UI models
BASE_DIR="./models"

# Declare an associative array with folder names and their corresponding download URLs
declare -A files=(
    ["checkpoints/photon_v1.safetensors"]="https://huggingface.co/sam749/Photon-v1/resolve/main/photon_v1.safetensors"
    ["controlnet/control_v1p_sd15_qrcode_monster.safetensors"]="https://huggingface.co/monster-labs/control_v1p_sd15_qrcode_monster/resolve/main/control_v1p_sd15_qrcode_monster.safetensors"
    ["controlnet/control_depth-fp16.safetensors"]="https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_depth-fp16.safetensors"
    ["controlnet/control_v1p_sd15_qrcode.safetensors"]="https://huggingface.co/DionTimmer/controlnet_qrcode/resolve/main/control_v1p_sd15_qrcode.safetensors"
    ["controlnet/controlnet_checkpoint.ckpt"]="https://huggingface.co/crishhh/animatediff_controlnet/resolve/main/controlnet_checkpoint.ckpt"
    ["loras/AnimateLCM_sd15_t2v_lora.safetensors"]="https://huggingface.co/wangfuyun/AnimateLCM/resolve/main/AnimateLCM_sd15_t2v_lora.safetensors"
    ["loras/v3_sd15_adapter.ckpt"]="https://huggingface.co/guoyww/animatediff/resolve/main/v3_sd15_adapter.ckpt"
    ["upscale_models/4x_NMKD-Siax_200k.pth"]="https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth"
    ["vae/vae-ft-mse-840000-ema-pruned.safetensors"]="https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors"
    ["animatediff_models/AnimateLCM_sd15_t2v.ckpt"]="https://huggingface.co/wangfuyun/AnimateLCM/resolve/main/AnimateLCM_sd15_t2v.ckpt"
)

# Loop through the array and download files
for path in "${!files[@]}"; do
    file_url="${files[$path]}"
    full_path="$BASE_DIR/$path"
    
    # Download the file
    echo "Downloading $file_url to $full_path"
    curl -L -o "$full_path" "$file_url"
done

echo "All files have been downloaded to their respective folders."
