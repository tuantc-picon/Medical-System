from fastapi import APIRouter

# Create the router instance
router = APIRouter()

# Define your routes
@router.get("/example")
def get_example():
    return {"message": "This is an example endpoint"}

# Add more route handlers as needed
@router.post("/items")
def create_item():
    return {"message": "Item created"}

# You can organize routes by category
@router.get("/users")
def get_users():
    return {"users": ["user1", "user2"]}
