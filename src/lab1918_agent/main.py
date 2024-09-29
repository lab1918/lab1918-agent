import logging
import os

from pathlib import Path
from lab1918_agent.assume_role import assume_role
from lab1918_agent.utils import logger, get_celery_app


def switch_role():
    role = os.getenv("STS_ROLE_ARN")
    if role is None:
        logger.info(f"no role arn, skip switch role")
        return

    filepath = Path.home() / ".aws" / "credentials"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with filepath.open("w", encoding="utf-8") as f:
        f.write("[default]\n")
        for k, v in assume_role().items():
            f.write(f"{k}={v}\n")
    logger.info(f"switched role to {role}")


if __name__ == "__main__":
    switch_role()
    app = get_celery_app()
    worker = app.Worker(include=["lab1918_agent.deployer"])
    worker.setup_defaults(concurrency=4, loglevel=logging.INFO)
    worker.start()
