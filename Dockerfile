FROM python:3.9

RUN mkdir -p /home/lab1918
WORKDIR /home/lab1918

RUN apt-get update && apt-get install -y jq less awscli

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ /home/lab1918

CMD celery -A lab1918_agent.deployer worker --pool=prefork --concurrency=4 --loglevel=info -E
