# lab1918-agent

## Setup

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

Alway format the code before push

```
$ black .
```

## Build

```
docker build -t agent .
```

## Test

```
tox
```

## Run
```
docker run -d -t -i            \
  -e BROKER=<>                 \
  -e BACKEND=<>                \
  -e AWS_REGION=<>             \
  -e AWS_ACCESS_KEY_ID=<>      \
  -e AWS_SECRET_ACCESS_KEY=<>  \
  agent
```