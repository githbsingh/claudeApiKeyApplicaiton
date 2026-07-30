from config.prompts import SYSTEM_PROMPT
from config.settings import (
    BEDROCK_MODEL_ID,
    MAX_TOKENS,
    TEMPERATURE
)
from services.bedrock_client import get_bedrock_client


class ChatService:

    def __init__(self):
        self.client = get_bedrock_client()

    def chat(self, user_message: str) -> str:
        """
        Send a user message to Claude
        and return the generated response.
        """

        response = self.client.converse(
            modelId=BEDROCK_MODEL_ID,

            system=[
                {
                    "text": SYSTEM_PROMPT
                }
            ],

            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": user_message
                        }
                    ]
                }
            ],

            inferenceConfig={
                "maxTokens": MAX_TOKENS,
                "temperature": TEMPERATURE
            }
        )

        return response[
            "output"
        ]["message"]["content"][0]["text"]