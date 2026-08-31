import json

from tools.calculator import calculate
from tools.trip_info import get_trip_info


TOOLS = [
    {
        "toolSpec": {
            "name": "calculator",
            "description": (
                "Perform mathematical calculations. "
                "Use this tool whenever the user asks "
                "for arithmetic or numerical calculations."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": (
                                "Mathematical expression "
                                "to calculate."
                            ),
                        }
                    },
                    "required": ["expression"],
                }
            },
        }
    },

    {
        "toolSpec": {
            "name": "get_trip_info",
            "description": (
                "Retrieve information about the "
                "Kudremukha trip, including dates, "
                "destination, departure time and itinerary."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": (
                                "The trip information "
                                "the user wants."
                            ),
                        }
                    },
                    "required": ["topic"],
                }
            },
        }
    },
]


def execute_tool(tool_name, tool_input):
    """
    Execute the requested tool.
    """

    if tool_name == "calculator":

        return calculate(
            tool_input["expression"]
        )

    if tool_name == "get_trip_info":

        return get_trip_info(
            tool_input["topic"]
        )

    return (
        f"Unknown tool: {tool_name}"
    )