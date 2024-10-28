from urllib import request
from os import path
from filelock import FileLock

from lab1918_agent.logger import logger


class UnsupportedScheme(Exception):
    pass


class Getter:
    def __init__(self, file_url, file_name, overwrite=False) -> None:
        self.file_url = file_url
        self.file_name = file_name
        self.overwrite = overwrite
        self._cache_dir = "/tmp/cache/"

    def get(self):
        file_path = f"{self._cache_dir}/{self.file_name}"
        # lock the file to avoid concurrent write
        lock = FileLock(f"{file_path}.lock", timeout=300)
        with lock:
            if (
                not self.overwrite
                and self.path.exists(file_path)
                and path.getsize(file_path)
            ):
                logger.info(f"file {file_path} already downloaded")
                return file_path
            else:
                with open(
                    file_path,
                    "wb",
                ) as F:
                    request.urlretrieve(self.file_url, F)
        return file_path
