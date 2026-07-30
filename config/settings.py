import os

from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-southeast-2"
)

ACCESS_KEY_ID = os.getenv(
    "AWS_ACCESS_KEY_ID"
)

SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY"
)

BEDROCK_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID"
)

MAX_TOKENS = int(
    os.getenv("MAX_TOKENS", "500")
)

TEMPERATURE = float(
    os.getenv("TEMPERATURE", "0.7")
)




def validate_settings():
    """Validate required application settings."""

    if not BEDROCK_MODEL_ID:
        raise ValueError(
            "BEDROCK_MODEL_ID is missing. "
            "Add it to the .env file."
        )