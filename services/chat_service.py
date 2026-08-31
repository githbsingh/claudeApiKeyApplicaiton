from services.bedrock_client import get_bedrock_client

from config.settings import (
    BEDROCK_MODEL_ID,
    MAX_TOKENS,
    TEMPERATURE,
)

from tools.registry import (
    TOOLS,
    execute_tool,
)


class ChatService:

    def __init__(self):

        self.client = get_bedrock_client()

    # ========================================================
    # NORMAL CHAT
    # ========================================================

    def chat(self, conversation_history):

        messages = self._build_messages(
            conversation_history
        )

        return self._run_agent(
            messages
        )

    # ========================================================
    # AGENT LOOP
    # ========================================================

    def _run_agent(self, messages):

        while True:

            response = self.client.converse(

                modelId=BEDROCK_MODEL_ID,

                messages=messages,

                toolConfig={
                    "tools": TOOLS
                },

                inferenceConfig={
                    "maxTokens": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                },
            )

            output = response["output"]["message"]

            stop_reason = response.get(
                "stopReason"
            )

            # ------------------------------------------------
            # Claude wants to use a tool
            # ------------------------------------------------

            if stop_reason == "tool_use":

                messages.append(
                    output
                )

                tool_results = []

                for content_block in output["content"]:

                    if "toolUse" not in content_block:
                        continue

                    tool_use = content_block["toolUse"]

                    tool_name = tool_use["name"]

                    tool_input = tool_use["input"]

                    tool_use_id = tool_use["toolUseId"]

                    # Execute our Python function
                    result = execute_tool(
                        tool_name,
                        tool_input
                    )

                    tool_results.append(
                        {
                            "toolResult": {
                                "toolUseId": tool_use_id,
                                "content": [
                                    {
                                        "text": result
                                    }
                                ]
                            }
                        }
                    )

                # Send tool results back to Claude
                messages.append(
                    {
                        "role": "user",
                        "content": tool_results
                    }
                )

                # Claude now generates final answer
                continue

            # ------------------------------------------------
            # Normal final response
            # ------------------------------------------------

            return self._extract_text(
                output
            )

    # ========================================================
    # STREAMING AGENT
    # ========================================================

    def stream_chat(self, conversation_history):

        messages = self._build_messages(
            conversation_history
        )

        # For Phase 4, we initially use the
        # non-streaming Converse call for tool
        # orchestration.

        response = self._run_agent(
            messages
        )

        yield response

    # ========================================================
    # MESSAGE CONVERSION
    # ========================================================

    @staticmethod
    def _build_messages(
        conversation_history
    ):

        messages = []

        for message in conversation_history:

            messages.append(
                {
                    "role": message["role"],
                    "content": [
                        {
                            "text": message["content"]
                        }
                    ],
                }
            )

        return messages

    # ========================================================
    # RESPONSE EXTRACTION
    # ========================================================

    @staticmethod
    def _extract_text(message):

        text_parts = []

        for content in message.get(
            "content",
            []
        ):

            if "text" in content:

                text_parts.append(
                    content["text"]
                )

        return "".join(text_parts)