import numexpr
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(description="The mathematical expression to evaluate (e.g., '12 * (3 + 4)')")

@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result. Use this for math, arithmetic, or calculations."""
    try:
        # numexpr safely evaluates math expressions
        result = numexpr.evaluate(expression)
        return str(result.item() if hasattr(result, "item") else result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"
