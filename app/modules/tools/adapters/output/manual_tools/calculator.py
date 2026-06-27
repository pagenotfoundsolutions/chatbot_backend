import numexpr
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(description="The mathematical expression to evaluate (e.g., '12 * (3 + 4)')")

class CalculatorOutput(BaseModel):
    result: str = Field(description="The evaluated result")
    error: str | None = Field(default=None, description="Error message if evaluation fails")

@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result in a structured JSON format."""
    try:
        # numexpr safely evaluates math expressions
        result = numexpr.evaluate(expression)
        val = str(result.item() if hasattr(result, "item") else result)
        return CalculatorOutput(result=val).model_dump_json()
    except Exception as e:
        return CalculatorOutput(result="", error=str(e)).model_dump_json()
