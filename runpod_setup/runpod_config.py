import runpod

runpod.api_key = "rpa_C59F7NHVAK5UO3DG170WWMA8CM8GP8JNWPS4PIFQzh77bb"

# pods = runpod.get_pods()

# print(pods)

# create pod for AI Video booth
pod = runpod.create_pod(
    name="ComfyUI AI VideoBooth",
    image_name="registry.hf.space/camenduru-comfyui-temp:latest",
    gpu_type_id="NVIDIA GeForce RTX 4090",
    gpu_count=1,
    ports="7860/tcp"
)

print(pod)

