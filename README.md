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
  -e AWS_ACCOUNT=<>            \
  -e STS_ROLE_ARN=<>           \
  agent
```

## test on ubuntu

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

```bash
git clone https://github.com/lab1918/lab1918-agent.git
pushd lab1918-agent
sudo docker build -t agent .
popd
sudo docker images
```