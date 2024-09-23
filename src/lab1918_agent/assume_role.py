import boto3

from os import getenv


def assume_role() -> dict:
    sts_role_arn = getenv("STS_ROLE_ARN")
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=sts_role_arn,
        RoleSessionName="SwitchRole",
    )
    credentials = assumed_role_object["Credentials"]
    return {
        "AWS_ACCESS_KEY_ID": credentials["AccessKeyId"],
        "AWS_SECRET_ACCESS_KEY": credentials["SecretAccessKey"],
        "AWS_SESSION_TOKEN": credentials["SessionToken"],
    }


if __name__ == "__main__":
    print(assume_role())
