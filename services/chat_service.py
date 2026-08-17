from services.bedrock_client import get_bedrock_client

from config.settings import (
    BEDROCK_MODEL_ID,
    MAX_TOKENS,
    TEMPERATURE,
)


class ChatService:

    def __init__(self):
        self.client = get_bedrock_client()

    def chat(self, conversation_history):
        """
        Normal non-streaming response.
        """

        messages = self._build_messages(
            conversation_history
        )

        response = self.client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages,
            inferenceConfig={
                "maxTokens": MAX_TOKENS,
                "temperature": TEMPERATURE,
            },
        )

        return response["output"]["message"]["content"][0]["text"]

    def stream_chat(self, conversation_history):
        """
        Stream Claude's response from Amazon Bedrock.
        """

        messages = self._build_messages(
            conversation_history
        )

        response = self.client.converse_stream(
            modelId=BEDROCK_MODEL_ID,
            messages=messages,
            inferenceConfig={
                "maxTokens": MAX_TOKENS,
                "temperature": TEMPERATURE,
            },
        )

        for event in response["stream"]:

            # Claude text delta
            if "contentBlockDelta" in event:

                delta = event["contentBlockDelta"]

                if "delta" in delta:
                    text = delta["delta"].get("text")

                    if text:
                        yield text

    @staticmethod
    def _build_messages(conversation_history):
        """
        Convert our conversation memory format
        into Amazon Bedrock Converse format.
        """

        messages = []

        for message in conversation_history:

            role = message["role"]
            content = message["content"]

            messages.append(
                {
                    "role": role,
                    "content": [
                        {
                            "text": content
                        }
                    ],
                }
            )

        return messages