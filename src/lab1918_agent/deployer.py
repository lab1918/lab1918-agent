from lab1918_agent.utils import logger
from lab1918_agent.celery import get_celery_app


app = get_celery_app()


@app.task(bind=True)
def ping(self, *args, **kwargs) -> str:
    logger.info(
        f"Running task ping, id: {self.request.id}, args: {args}, kwargs: {kwargs}"
    )
    return "pong"
