import os
import pymongo
from typing import Dict, List, Optional
from bson.objectid import ObjectId
from todo_app.data.item import Item, ItemStatus

MONGO_CLIENT = None

def __get_items_collection():
    global MONGO_CLIENT
    if (MONGO_CLIENT is None):
        MONGO_CLIENT = pymongo.MongoClient(f'{os.environ["MONGO_CONNECTION_STRING"]}/?retryWrites=true&w=majority')
    return MONGO_CLIENT[os.environ['MONGO_DATABASE_NAME']].items

def __create_todo_item(title: str):
    id = __get_items_collection().insert_one({
        "title": title,
        "status": ItemStatus.NOT_STARTED.value
    })
    return Item(id=id, title=title, status=ItemStatus.NOT_STARTED)


def __remove_item(id: str):
    __get_items_collection().delete_one({"_id": ObjectId(id)})


def __update_item(item: Item):
    """
    Updates the item in mongo
    """

    __get_items_collection().update_one({"_id": ObjectId(item.id)}, {
        "$set": {
            "title": item.title,
            "status": item.status.value
        }
    })


def map_doc_to_item(doc: Dict) -> Item:
    return Item(id=str(doc["_id"]), title=doc["title"], status=ItemStatus.from_str(doc["status"]))


def get_items() -> List[Item]:
    """
    Fetches all saved items from mongo.

    Returns:
        list: The list of saved items.
    """
    return list(map(map_doc_to_item, __get_items_collection().find()))


def get_item(id: str) -> Optional[Item]:
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """

    items = get_items()
    return next((item for item in items if item.id == id), None)


def add_item(title: str) -> Item:
    """
    Adds a new item with the specified title to the todo list.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    # Add the item to the list
    item = __create_todo_item(title)

    return item


def delete_item(id: str) -> Item:
    """
    Deletes the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """

    item = get_item(id)
    __remove_item(id)
    return item


def save_item(item: Item) -> Item:
    """
    Updates an existing item in the session. 
    If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """

    __update_item(item)

    return item
