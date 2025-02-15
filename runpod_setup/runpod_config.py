import runpod

runpod.api_key = "rpa_NTQ7XV4ZVZK69C0064IALRZ7BE8GONO1ZBWFMXZZ12lz7v"

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

