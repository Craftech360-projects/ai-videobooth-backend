#!/bin/bash

# List of GitHub repositories to clone
repos=(
    "https://github.com/ltdrdata/ComfyUI-Impact-Pack.git"
    "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation.git"
    "https://github.com/jags111/efficiency-nodes-comfyui.git"
    "https://github.com/WASasquatch/was-node-suite-comfyui.git"
    "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes.git"
    "https://github.com/cubiq/ComfyUI_IPAdapter_plus.git"
    "https://github.com/jamesWalker55/comfyui-various.git"
    "https://github.com/rgthree/rgthree-comfy.git"
    "https://github.com/giriss/comfy-image-saver.git"
    "https://github.com/cubiq/ComfyUI_essentials.git"
    "https://github.com/crystian/ComfyUI-Crystools.git"
    "https://github.com/jakechai/ComfyUI-JakeUpgrade.git"
    "https://github.com/Fannovel16/comfyui_controlnet_aux.git"
    "https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet.git"
    "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git"
    "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git"
    "https://github.com/ai-shizuka/ComfyUI-tbox.git"
    "https://github.com/FizzleDorf/ComfyUI_FizzNodes.git"
    "https://github.com/Fannovel16/ComfyUI-MagickWand.git"
    "https://github.com/WASasquatch/FreeU_Advanced.git"
    "https://github.com/cubiq/ComfyUI_FaceAnalysis.git"
    "https://github.com/sipherxyz/comfyui-art-venture.git"
    "https://github.com/JPS-GER/ComfyUI_JPS-Nodes.git"
    "https://github.com/chrisgoringe/cg-use-everywhere.git"
    "https://github.com/kijai/ComfyUI-KJNodes.git"
    "https://github.com/chflame163/ComfyUI_LayerStyle.git"
    "https://github.com/taabata/LCM_Inpaint_Outpaint_Comfy.git"
    "https://github.com/palant/image-resize-comfyui.git"
    "https://github.com/PowerHouseMan/ComfyUI-AdvancedLivePortrait.git"
)

# Clone each repository
for repo in "${repos[@]}"
do
    echo "Cloning $repo..."
    git clone "$repo"
done
