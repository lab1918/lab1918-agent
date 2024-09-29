import logging
import os

from lab1918_agent.assume_role import assume_role
from lab1918_agent.utils import logger, get_celery_app


app = get_celery_app()


@app.task(bind=True)
def ping(self, *args, **kwargs) -> str:
    logger.info(
        f"Running task ping, id: {self.request.id}, args: {args}, kwargs: {kwargs}"
    )
    return "pong"


def setup_env():
    role = os.getenv("STS_ROLE_ARN")
    if role is None:
        logger.info(f"no role arn, skip setup env")
        return

    for k, v in assume_role().items():
        os.environ[k] = v
    logger.info(f"switch role to {role}")


if __name__ == "__main__":
    setup_env()
    worker = app.Worker(include=["lab1918_agent.deployer"])
    worker.setup_defaults(concurrency=4, loglevel=logging.INFO)
    worker.start()
