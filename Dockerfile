FROM python:3.9

RUN mkdir /lab1918
WORKDIR /lab1918

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ /lab1918

CMD celery -A lab1918_agent.deployer worker --pool=prefork --concurrency=4 --loglevel=info -E
