

# Import FastAPI and Pydantic for data validation
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Create FastAPI application instance
app = FastAPI()

# Define the data model for our to-do items
class Todo(BaseModel):
    # Each todo item will have an ID (unique identifier)
    id: Optional[int] = None
    # Title of the todo item
    title: str
    # Description (optional)
    description: Optional[str] = None
    # Status to track if task is completed
    completed: bool = False

# In-memory database (for simplicity, using a list)
# In real applications, we use a proper database like PostgreSQL or MongoDB
todos_db = [
    Todo(id=1, title="Learn FastAPI", description="Study FastAPI basics", completed=False),
    Todo(id=2, title="Build CRUD App", description="Create a complete CRUD application", completed=False)
]

# AUTO-INCREMENT for new IDs
next_id = 3

# CREATE operation - Add a new todo item
# POST: /todos
@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    # Get the next available ID
    global next_id

    # Create new todo with the next ID
    todo_dict = todo.dict()
    todo_dict['id'] = next_id
    new_todo = Todo(**todo_dict)

    # Add to our "database"
    todos_db.append(new_todo)
    # Increment next_id for future items
    next_id += 1
    # Return the created todo item
    return new_todo

# READ operation - Get all todo items
# GET: /todos
@app.get("/todos", response_model=List[Todo])
async def get_all_todos():
    # Return all todos from our "database"
    return todos_db

# READ operation - Get a specific todo by ID
# GET: /todos/{todo_id}
@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo_by_id(todo_id: int):
    # Find the todo with the matching ID
    for todo in todos_db:
        if todo.id == todo_id:
            # Return the found todo
            return todo
    # If not found, raise an error
    raise HTTPException(status_code=404, detail="Todo not found")

# UPDATE operation - Update an existing todo
# PUT: /todos/{todo_id}
@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated_todo: Todo):
    # Find the index of the todo to update
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            # Update the todo with new data
            todos_db[index] = updated_todo
            # Return the updated todo
            return updated_todo
    # If not found, raise an error
    raise HTTPException(status_code=404, detail="Todo not found")

# DELETE operation - Remove a todo item
# DELETE: /todos/{todo_id}
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    # Find the index of the todo to delete
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            # Remove the todo from our "database"
            deleted_todo = todos_db.pop(index)
            # Return confirmation message
            return {"message": f"Todo '{deleted_todo.title}' deleted successfully"}
    # If not found, raise an error
    raise HTTPException(status_code=404, detail="Todo not found")

# Health check endpoint to verify the server is running
# GET: /health
@app.get("/health")
async def health_check():
    return {"status": "healthy", "todos_count": len(todos_db)}

# Print message when server starts
print("🚀 FastAPI Todo App server started on http://localhost:8000")

