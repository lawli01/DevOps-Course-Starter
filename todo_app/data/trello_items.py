import os
from todo_app.data.item import Item, ItemStatus
from typing import List, Optional

import requests

def get_query_params(): 
    return {
        'token': os.environ['TRELLO_API_TOKEN'],
        'key': os.environ['TRELLO_API_KEY']
    }

base_uri = "https://api.trello.com/1"

def get_lists() -> List[dict]:
    todo_board_id = os.environ['TRELLO_API_TODO_BOARD_ID']
    return requests.get(f'{base_uri}/boards/{todo_board_id}/lists', params=get_query_params()).json()

def get_list_id_or_throw(lists: List[dict], list_name: str) -> str:
    list = next(iter([x for x in lists if x['name'] == list_name]), None)
    if (list is None):
        raise ValueError(f'Could not find list "{list_name}". Make sure you have this configured on your trello board')
    return list['id']

def get_items_from_list(list_id: str, status: ItemStatus) -> List[Item]:
    cards = requests.get(f'{base_uri}/lists/{list_id}/cards', params=get_query_params()).json()
    return [Item(id=card['id'], title=card['name'], status=status) for card in cards]

def create_todo_item(title: str):
    lists = get_lists()
    to_do_list_id = get_list_id_or_throw(lists, "To Do")
    response = requests.post(f'{base_uri}/cards', params={**get_query_params(), 'name': title, 'idList': to_do_list_id})

    if response.status_code != 200:
        raise ValueError(f'Failed to create todo item for "{title}". Received status code {response.status_code}')
    
    response_body = response.json()
    return Item(id=response_body['id'], title=title, status=ItemStatus.NOT_STARTED)

def remove_item(id: str):
    response = requests.delete(f'{base_uri}/cards/{id}', params=get_query_params())
    if response.status_code != 200:
        raise ValueError(f'Failed to delete todo item with id "{id}"". Received status code {response.status_code}')

def update_item(item: Item):
    lists = get_lists()
    to_do_list_id = get_list_id_or_throw(lists, "To Do")
    doing_list_id = get_list_id_or_throw(lists, "Doing")
    done_list_id = get_list_id_or_throw(lists, "Done")
    
    list_id_to_move_to = None
    if item.status == ItemStatus.NOT_STARTED: list_id_to_move_to = to_do_list_id
    elif item.status == ItemStatus.IN_PROGRESS: list_id_to_move_to = doing_list_id
    elif item.status == ItemStatus.COMPLETE: list_id_to_move_to = done_list_id

    response = requests.put(f'{base_uri}/cards/{item.id}', params={**get_query_params(), 'idList': list_id_to_move_to})#

    if response.status_code != 200:
        raise ValueError(f'Failed to update todo item with id "{item.id}". Received status code {response.status_code}')


def get_items() -> List[Item]:
    """
    Fetches all saved items from trello.

    Returns:
        list: The list of saved items.
    """
    lists = get_lists()
    to_do_list_id = get_list_id_or_throw(lists, "To Do")
    doing_list_id = get_list_id_or_throw(lists, "Doing")
    done_list_id = get_list_id_or_throw(lists, "Done")

    to_do_items = get_items_from_list(to_do_list_id, ItemStatus.NOT_STARTED)
    in_progress_items = get_items_from_list(doing_list_id, ItemStatus.IN_PROGRESS)
    complete_items = get_items_from_list(done_list_id, ItemStatus.COMPLETE)

    return to_do_items + in_progress_items + complete_items

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
    item = create_todo_item(title)

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
    remove_item(id)
    return item


def save_item(item: Item) -> Item:
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    update_item(item)

    return item

