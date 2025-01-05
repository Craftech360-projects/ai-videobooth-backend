raw_response = run_graphql_query(
        pod_mutations.generate_pod_deployment_mutation(
            name,
            image_name,
            gpu_type_id,
            cloud_type,
            support_public_ip,
            start_ssh,
            data_center_id,
            country_code,
            gpu_count,
            volume_in_gb,
            container_disk_in_gb,
            min_vcpu_count,
            min_memory_in_gb,
            docker_args,
            ports,
            volume_mount_path,
            env,
            template_id,
            network_volume_id,
            allowed_cuda_versions,
            min_download,
            min_upload,
        )
    )


    def create_pod(
    name: str,
    image_name: str,
    gpu_type_id: str,
    cloud_type: str = "ALL",
    support_public_ip: bool = True,
    start_ssh: bool = True,
    data_center_id: Optional[str] = None,
    country_code: Optional[str] = None,
    gpu_count: int = 1,
    volume_in_gb: int = 0,
    container_disk_in_gb: Optional[int] = None,
    min_vcpu_count: int = 1,
    min_memory_in_gb: int = 1,
    docker_args: str = "",
    ports: Optional[str] = None,
    volume_mount_path: str = "/runpod-volume",
    env: Optional[dict] = None,
    template_id: Optional[str] = None,
    network_volume_id: Optional[str] = None,
    allowed_cuda_versions: Optional[list] = None,
    min_download = None,
    min_upload = None,
) -> dict:
    """
    Create a pod

    :param name: the name of the pod
    :param image_name: the name of the docker image to be used by the pod
    :param gpu_type_id: the gpu type wanted by the pod (retrievable by get_gpus)
    :param cloud_type: if secure cloud, community cloud or all is wanted
    :param data_center_id: the id of the data center
    :param country_code: the code for country to start the pod in
    :param gpu_count: how many gpus should be attached to the pod
    :param volume_in_gb: how big should the pod volume be
    :param ports: the ports to open in the pod, example format - "8888/http,666/tcp"
    :param volume_mount_path: where to mount the volume?
    :param env: the environment variables to inject into the pod,
                for example {EXAMPLE_VAR:"example_value", EXAMPLE_VAR2:"example_value 2"}, will
                inject EXAMPLE_VAR and EXAMPLE_VAR2 into the pod with the mentioned values
    :param template_id: the id of the template to use for the pod
    :param min_download: minimum download speed in Mbps
    :param min_upload: minimum upload speed in Mbps
    :example:

    >>> pod_id = runpod.create_pod("test", "runpod/stack", "NVIDIA GeForce RTX 3070")