from langchain_core.tools import tool

@tool
def plus(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide a by b. Returns error message if b is 0."""
    if b == 0:
        return "Error: Division by zero"
    return a / b
