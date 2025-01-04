#!/bin/bash

# Navigate to the ai-videobooth-backend/comfyui/ai_videobooth/ folder
cd "$(dirname "$0")/comfyui/ai_videobooth/"

# Run the ai_videobooth_models.sh script
bash ai_videobooth_models.sh

bash custom_node.sh
