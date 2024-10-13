import docker
import docker.constants

from typing import Optional

from lab1918_agent.logger import logger
from docker.models.networks import Network
from docker.models.containers import Container


class ContainerClient:
    def __init__(self):
        self.client = docker.from_env()

    def is_network_exist(self, name) -> Optional[Network]:
        networks = self.client.networks.list()
        for network in networks:
            if network.name == name:
                return network

    def create_network(self, name, driver="bridge") -> Network:
        logger.info(f"creating network {name}")
        network = self.is_network_exist(name)
        if network:
            logger.info(f"network {name} already exist")
            return network
        network = self.client.networks.create(name, driver=driver)
        logger.info(f"created network {name}")
        return network

    def delete_network(self, name) -> bool:
        logger.info(f"deleting network {name}")
        if not self.is_network_exist(name):
            logger.info(f"network {name} does not exist")
            return
        networks = self.client.networks.prune()["NetworksDeleted"]
        logger.info(f"deleted network {networks}")
        return name in networks

    def pull_image(self, name):
        logger.info(f"pull image {name}")
        self.client.images.pull(name)

    def create_container(self, image_name, container_name, mgmt_network) -> Container:
        logger.info(f"create container {container_name} from {image_name}")
        return self.client.containers.create(
            image=image_name,
            hostname=container_name,
            network=mgmt_network,
            detach=True,
            privileged=True,
            tty=True,
        )
