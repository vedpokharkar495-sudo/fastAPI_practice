
# Import FastAPI library for creating the API
from fastapi import FastAPI
from pydantic import BaseModel

# Create an instance of FastAPI application
app = FastAPI()

# Define a data model for calculator requests using Pydantic
# This will validate incoming data
class CalculatorRequest(BaseModel):
    # First number input with type hint as float
    number1: float
    # Second number input with type hint as float
    number2: float
    # Operation type with predefined values
    operation: str  # 'add', 'subtract', 'multiply', 'divide'

# This endpoint accepts GET requests at /
@app.get("/")
async def health_check():
    # Return a simple health status message
    return {"status": "FastAPI server started on http://localhost:8000"}

# Define endpoint for addition operation
# This endpoint accepts POST requests at /add
@app.post("/add")
async def add(request: CalculatorRequest):
    # Perform addition of two numbers from the request
    result = request.number1 + request.number2
    # Return the result as a dictionary
    return {"result": result}

# Define endpoint for subtraction operation
# This endpoint accepts POST requests at /subtract
@app.post("/subtract")
async def subtract(request: CalculatorRequest):
    # Perform subtraction of two numbers from the request
    result = request.number1 - request.number2
    # Return the result as a dictionary
    return {"result": result}

# Define endpoint for multiplication operation
# This endpoint accepts POST requests at /multiply
@app.post("/multiply")
async def multiply(request: CalculatorRequest):
    # Perform multiplication of two numbers from the request
    result = request.number1 * request.number2
    # Return the result as a dictionary
    return {"result": result}

# Define endpoint for division operation
# This endpoint accepts POST requests at /divide
@app.post("/divide")
async def divide(request: CalculatorRequest):
    # Check if the second number is zero to avoid division by zero
    if request.number2 == 0:
        # Return error message if division by zero is attempted
        return {"error": "Cannot divide by zero"}
    # Perform division of two numbers from the request
    result = request.number1 / request.number2
    # Return the result as a dictionary
    return {"result": result}

