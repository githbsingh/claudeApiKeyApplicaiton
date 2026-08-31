def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Examples:
        10 + 20
        100 / 4
        25 * 8
    """

    try:
        # Restrict the available namespace.
        result = eval(
            expression,
            {
                "__builtins__": {}
            },
            {}
        )

        return str(result)

    except Exception as e:
        return f"Unable to calculate expression: {str(e)}"