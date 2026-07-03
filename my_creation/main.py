from fastapi import HTTPException, FastAPI
from pydantic import BaseModel

app = FastAPI()

class AddRequest(BaseModel):
    number1: float
    number2: float
    operation: str  # 'add', 'subtract', 'multiply', 'divide'
    


@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/add")
async def add_numbers(request: AddRequest):
    try:
        result = request.number1 + request.number2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.post("/subtract")
async def subtract_numbers(request: AddRequest):
    try:
        result = request.number1 - request.number2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/multiply")
async def multiply_numbers(request: AddRequest):
    try:
        result = request.number1 * request.number2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@app.post("/divide")
async def divide_numbers(request: AddRequest):
    try:
        if request.number2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = request.number1 / request.number2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
