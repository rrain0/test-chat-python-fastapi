from fastapi import FastAPI

# Create the FastAPI instance
app = FastAPI()

# Define a GET route at the root URL
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Define a dynamic route with a path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
