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

    def chat(
        self,
        conversation_history: list
    ) -> str:
        """
        Send the complete conversation
        history to Claude.
        """

        bedrock_messages = []

        for message in conversation_history:

            bedrock_messages.append(
                {
                    "role": message["role"],
                    "content": [
                        {
                            "text": message["content"]
                        }
                    ]
                }
            )

        response = self.client.converse(
            modelId=BEDROCK_MODEL_ID,

            system=[
                {
                    "text": SYSTEM_PROMPT
                }
            ],

            messages=bedrock_messages,

            inferenceConfig={
                "maxTokens": MAX_TOKENS,
                "temperature": TEMPERATURE
            }
        )

        return (
            response["output"]
            ["message"]
            ["content"][0]
            ["text"]
        )