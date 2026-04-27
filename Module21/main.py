from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{"Message": "Hello World"}

@app.get("/items/")
def read_items():
    return{"items": ["item1", "item2", "item3"]}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return{"user_id": user_id, "name": "Gerti"}

@app.get("/items/{item_id}")
def get_items(skip: int = 0 , limit: int = 10):
    return{"skip": skip, "limit": limit}

@app.get("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    return{"item_id": item_id, "item_name": name, "item_price": price}

@app.post("/items/")
def create_item(name: str, price: float):
    return{"item_name": name, "item_price": price}