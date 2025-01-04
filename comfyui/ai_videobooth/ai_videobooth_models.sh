#!/bin/bash

# URLs, folder names, and custom file names
urls=(
  "https://huggingface.co/guoyww/animatediff/resolve/main/v3_sd15_mm.ckpt|animatediff_models|v3_sd15_mm.ckpt"
  "https://civitai.com/api/download/models/93208?type=Model&format=SafeTensor&size=pruned&fp=fp16|checkpoints|model_93208_fp16.safetensors"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p.pth|controlnet|control_v11e_sd15_ip2p.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p.yaml|controlnet|control_v11e_sd15_ip2p.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle.pth|controlnet|control_v11e_sd15_shuffle.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle.yaml|controlnet|control_v11e_sd15_shuffle.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile.pth|controlnet|control_v11f1e_sd15_tile.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile.yaml|controlnet|control_v11f1e_sd15_tile.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth|controlnet|control_v11f1p_sd15_depth.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.yaml|controlnet|control_v11f1p_sd15_depth.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.pth|controlnet|control_v11p_sd15_canny.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.yaml|controlnet|control_v11p_sd15_canny.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint.pth|controlnet|control_v11p_sd15_inpaint.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint.yaml|controlnet|control_v11p_sd15_inpaint.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart.pth|controlnet|control_v11p_sd15_lineart.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart.yaml|controlnet|control_v11p_sd15_lineart.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd.pth|controlnet|control_v11p_sd15_mlsd.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd.yaml|controlnet|control_v11p_sd15_mlsd.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae.pth|controlnet|control_v11p_sd15_normalbae.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae.yaml|controlnet|control_v11p_sd15_normalbae.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth|controlnet|control_v11p_sd15_openpose.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.yaml|controlnet|control_v11p_sd15_openpose.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble.pth|controlnet|control_v11p_sd15_scribble.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble.yaml|controlnet|control_v11p_sd15_scribble.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg.pth|controlnet|control_v11p_sd15_seg.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg.yaml|controlnet|control_v11p_sd15_seg.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge.pth|controlnet|control_v11p_sd15_softedge.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge.yaml|controlnet|control_v11p_sd15_softedge.yaml"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime.pth|controlnet|control_v11p_sd15s2_lineart_anime.pth"
  "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime.yaml|controlnet|control_v11p_sd15s2_lineart_anime.yaml"
  "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/blob/main/vae-ft-mse-840000-ema-pruned.safetensors|vae|vae-ft-mse-840000-ema-pruned.safetensors"
  "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.ckpt|vae|vae-ft-mse-840000-ema-pruned.ckpt"
)

# Download each file with its original name or specified custom name
for url in "${urls[@]}"
do
  IFS="|" read -r link folder name <<< "$url"
  # Prepend "models/" to the folder path
  target_folder="../../../models/$folder"
  # Ensure the target folder exists
  mkdir -p "$target_folder"
  # Download the file with the specified name
  wget -O "$target_folder/$name" "$link"
done
