from fastapi import APIRouter
from models import Item

router = APIRouter()

@router.get("/items")
def get_items():
    return [
        Item(id=1, name="Item One"),
        Item(id=2, name="Item Two")
    ]