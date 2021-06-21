import os
from typing import List

import requests
from flask import session
from flask.globals import request

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]

query_params = {
    'token': os.environ['TRELLO_API_TOKEN'],
    'key': os.environ['TRELLO_API_KEY']
}

base_uri = "https://api.trello.com/1"

def get_todo_board_id():
    configured_todo_board_name = os.environ['TRELLO_API_TODO_BOARD_NAME']
    response = requests.get(f'{base_uri}/members/me/boards', params=query_params).json()
    boards_filtered_by_name = [x for x in response if x['name'] == configured_todo_board_name]
    todo_board = next(iter(boards_filtered_by_name), None)

    if (todo_board is None):
        raise ValueError(f"Could not find configured to do board: {configured_todo_board_name}")

    return todo_board['id']

def get_lists():
    todo_board_id = get_todo_board_id()
    return requests.get(f'{base_uri}/boards/{todo_board_id}/lists', params=query_params).json()

def get_list_id_or_throw(lists: List[dict], list_name: str):
    list = next(iter([x for x in lists if x['name'] == list_name]), None)
    if (list is None):
        raise ValueError(f"Could not find list '{list_name}'. Make sure you have this configured on your trello board")
    return list['id']

def get_items_from_list(list_id: str, status: str):
    cards = requests.get(f'{base_uri}/lists/{list_id}/cards', params=query_params).json()
    return [{
        'id': card['id'],
        'status': status,
        'title': card['name']
    } for card in cards]

def create_todo_item(item: dict):
    lists = get_lists()
    to_do_list_id = get_list_id_or_throw(lists, "To Do")
    response = requests.post(f'{base_uri}/cards', params={**query_params, 'name': item['title'], 'idList': to_do_list_id})

    if response.status_code != 200:
        raise ValueError(f"Failed to create todo item for '{item['title']}'. Received status code {response.status_code}")


def get_items():
    """
    Fetches all saved items from trello.

    Returns:
        list: The list of saved items.
    """
    lists = get_lists()
    to_do_list_id = get_list_id_or_throw(lists, "To Do")
    doing_list_id = get_list_id_or_throw(lists, "Doing")
    done_list_id = get_list_id_or_throw(lists, "Done")

    to_do_items = get_items_from_list(to_do_list_id, 'Not Started')
    in_progress_items = get_items_from_list(doing_list_id, 'In Progress')
    complete_items = get_items_from_list(done_list_id, 'Complete')

    return to_do_items + in_progress_items + complete_items

def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the todo list.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    
    item = { 'title': title, 'status': 'Not Started' }

    # Add the item to the list
    create_todo_item(item)

    return item


def delete_item(id):
    """
    Deletes the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    existing_items = get_items()
    item = next((item for item in existing_items if item['id'] == int(id)), None)
    if (item != None):
        existing_items.remove(item)
        session['items'] = existing_items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item

