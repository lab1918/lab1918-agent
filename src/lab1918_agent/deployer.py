from lab1918_agent.utils import get_celery_app
from lab1918_agent.logger import logger
from lab1918_agent.docker_client import ContainerClient


app = get_celery_app()


@app.task(bind=True)
def ping(self, *args, **kwargs) -> str:
    logger.info(
        f"Running task ping, id: {self.request.id}, args: {args}, kwargs: {kwargs}"
    )
    return "pong"


@app.task(bind=True)
def create_container(self, container_name, image_name, networks) -> bool:
    logger.info(
        f"Running task create_container, id: {self.request.id}, container_name: {container_name}, image_name: {image_name}, networks: {networks}"
    )
    client = ContainerClient()
    client.pull_image(image_name)
    client.create_network(networks[0])
    container = client.create_container(image_name, container_name, networks[0])
    for each in networks[1:]:
        network = client.create_network(each)
        network.connect(container)
    container.start()
    logger.info(f"created container {container_name}")
    return True


@app.task(bind=True)
def create_network(self, network_name, network_driver) -> bool:
    logger.info(
        f"Running task create_network, id: {self.request.id}, network_name: {network_name}, network_driver: {network_driver}"
    )
    client = ContainerClient()
    client.create_network(network_name, network_driver)
    logger.info(f"created network {network_name}")
    return True
