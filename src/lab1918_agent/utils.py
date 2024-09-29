import logging

from os import getenv
from celery import Celery

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_celery_app():
    results = getenv("BACKEND", default="celery")
    transport = getenv("BROKER", default="celery")
    region = getenv("AWS_REGION", default="us-east-1")
    broker_url = f"sqs://sqs.{region}.amazonaws.com"
    task_default_queue = transport
    result_backend = f"dynamodb://{region}/{results}"
    deployer = "lab1918_agent.deployer"
    broker_transport_options = {
        "visibility_timeout": 180,
        "polling_interval": 1,
        "is_secure": True,
        "sqs-creation-attributes": {
            "KmsMasterKeyId": "alias/aws/sqs",
            "MessageRetentionPeriod": "600",
        },
    }
    if account := getenv("AWS_ACCOUNT"):
        broker_transport_options["predefined_queues"] = {
            transport: {
                "url": f"https://sqs.{region}.amazonaws.com/{account}/{transport}"
            }
        }

    app = Celery(
        main=deployer,
        broker_url=broker_url,
        task_default_queue=task_default_queue,
        result_backend=result_backend,
        broker_transport_options=broker_transport_options,
        enable_utc=True,
        task_track_started=True,
        broker_connection_retry_on_startup=True,
    )

    return app
