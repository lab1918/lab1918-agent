FROM python:3.9

RUN mkdir -p /home/lab1918
WORKDIR /home/lab1918

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ /home/lab1918

CMD PYTHONPATH=. python3 lab1918_agent/deployer.py
