import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()


def get_setting(
    key: str,
    default=None
):
    """
    Read configuration from Streamlit Secrets
    or local environment variables.
    """

    try:
        if key in st.secrets:
            return st.secrets[key]
    except st.errors.StreamlitSecretNotFoundError:
        # Running locally without .streamlit/secrets.toml
        pass

    return os.getenv(
        key,
        default
    )


AWS_REGION = get_setting(
    "AWS_REGION",
    "ap-southeast-2"
)

AWS_ACCESS_KEY_ID = get_setting(
    "AWS_ACCESS_KEY_ID"
)

AWS_SECRET_ACCESS_KEY = get_setting(
    "AWS_SECRET_ACCESS_KEY"
)

BEDROCK_MODEL_ID = get_setting(
    "BEDROCK_MODEL_ID"
)

MAX_TOKENS = int(
    get_setting(
        "MAX_TOKENS",
        "500"
    )
)

TEMPERATURE = float(
    get_setting(
        "TEMPERATURE",
        "0.7"
    )
)


def validate_settings():
    """Validate required settings."""

    if not BEDROCK_MODEL_ID:
        raise ValueError(
            "BEDROCK_MODEL_ID is missing. "
            "Add it to Streamlit Secrets "
            "or your local .env file."
        )