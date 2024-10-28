from lab1918_agent.utils import get_celery_app
from lab1918_agent.logger import logger
from lab1918_agent.docker_client import ContainerClient
from lab1918_agent.file_getter import Getter


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
    client.create_network(networks[0])
    container = client.create_container(image_name, container_name, networks[0])
    for each in networks[1:]:
        network = client.create_network(each)
        network.connect(container)
    container.start()
    logger.info(f"created container {container_name}")
    return True


@app.task(bind=True)
def delete_container(self, container_name) -> bool:
    logger.info(
        f"Running task delete_container, id: {self.request.id}, container_name: {container_name}"
    )
    client = ContainerClient()
    client.delete_container(container_name)
    logger.info(f"deleted container {container_name}")
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


@app.task(bind=True)
def delete_network(self, network_name) -> bool:
    logger.info(
        f"Running task delete_network, id: {self.request.id}, network_name: {network_name}"
    )
    client = ContainerClient()
    client.delete_network(network_name)
    logger.info(f"deleted network {network_name}")
    return True


@app.task(bind=True)
def load_image(self, url) -> bool:
    logger.info(f"Running task load_image, id: {self.request.id}, url: {url}")
    client = ContainerClient()
    client.load_image(url)
    logger.info(f"image {url} loaded")
    return True


@app.task(bind=True)
def pull_image(self, image_name) -> bool:
    logger.info(
        f"Running task pull_image, id: {self.request.id}, image_name: {image_name}"
    )
    client = ContainerClient()
    client.pull_image(image_name)
    logger.info(f"image {image_name} loaded")
    return True


@app.task(bind=True)
def get_file(self, file_url, file_name, overwrite=False):
    logger.info(
        f"start processing {file_name} with overwrite {overwrite}, id: {self.request.id}"
    )
    getter = Getter(file_url, file_name, overwrite=overwrite)
    cached_file = getter.get()
    return cached_file
