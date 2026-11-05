import math
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Calculator API")


# ---------- Calculator functions ----------

def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(a: float, b: float) -> float:
    return a ** b


def modulo(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot take modulo by zero")
    return a % b


class Operation(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"
    power = "power"
    modulo = "modulo"


OPERATIONS = {
    Operation.add: add,
    Operation.subtract: subtract,
    Operation.multiply: multiply,
    Operation.divide: divide,
    Operation.power: power,
    Operation.modulo: modulo,
}


def calculate(a: float, b: float, operation: Operation) -> dict:
    try:
        result = OPERATIONS[operation](a, b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except OverflowError:
        raise HTTPException(status_code=400, detail="Result is too large")
    if isinstance(result, complex):
        raise HTTPException(status_code=400, detail="Result is not a real number")
    if not math.isfinite(result):
        raise HTTPException(status_code=400, detail="Result is too large")
    return {"a": a, "b": b, "operation": operation, "result": result}


# ---------- API endpoints ----------

@app.get("/")
async def read_root():
    return {"message": "Calculator API", "operations": [op.value for op in Operation]}


@app.get("/add")
async def add_numbers(a: float, b: float):
    return calculate(a, b, Operation.add)


@app.get("/subtract")
async def subtract_numbers(a: float, b: float):
    return calculate(a, b, Operation.subtract)


@app.get("/multiply")
async def multiply_numbers(a: float, b: float):
    return calculate(a, b, Operation.multiply)


@app.get("/divide")
async def divide_numbers(a: float, b: float):
    return calculate(a, b, Operation.divide)


@app.get("/power")
async def power_numbers(a: float, b: float):
    return calculate(a, b, Operation.power)


@app.get("/modulo")
async def modulo_numbers(a: float, b: float):
    return calculate(a, b, Operation.modulo)


class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: Operation


@app.post("/calculate")
async def calculate_numbers(request: CalculationRequest):
    return calculate(request.a, request.b, request.operation)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("calculatorapi:app", host="127.0.0.1", port=8000, reload=True)
