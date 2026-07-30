import boto3

from config.settings import AWS_REGION, ACCESS_KEY_ID, SECRET_ACCESS_KEY


def get_bedrock_client():
    """
    Create and return an Amazon Bedrock Runtime client.
    """

    return boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY
    )