FROM python:3.9

RUN mkdir -p /home/lab1918
WORKDIR /home/lab1918

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ /home/lab1918

CMD PYTHONPATH=. python3 lab1918_agent/main.py; celery -A lab1918_agent.deployer worker --pool=prefork --concurrency=4 --loglevel=info -E
