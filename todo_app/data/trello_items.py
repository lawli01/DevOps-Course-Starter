import os
from typing import List

import requests

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
        raise ValueError(f'Could not find configured to do board: {configured_todo_board_name}')

    return todo_board['id']

def get_lists():
    todo_board_id = get_todo_board_id()
    return requests.get(f'{base_uri}/boards/{todo_board_id}/lists', params=query_params).json()

def get_list_id_or_throw(lists: List[dict], list_name: str):
    list = next(iter([x for x in lists if x['name'] == list_name]), None)
    if (list is None):
        raise ValueError(f'Could not find list "{list_name}". Make sure you have this configured on your trello board')
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
        raise ValueError(f'Failed to create todo item for "{item["title"]}". Received status code {response.status_code}')

def remove_item(id: str):
    response = requests.delete(f'{base_uri}/cards/{id}', params=query_params)
    if response.status_code != 200:
        raise ValueError(f'Failed to delete todo item with id "{id}"". Received status code {response.status_code}')

def update_item(item: dict):
    lists = get_lists()
    to_do_list_id = get_list_id_or_throw(lists, "To Do")
    doing_list_id = get_list_id_or_throw(lists, "Doing")
    done_list_id = get_list_id_or_throw(lists, "Done")
    
    list_id_to_move_to = None
    if item['status'] == 'Not Started': list_id_to_move_to = to_do_list_id
    elif item['status'] == "In Progress": list_id_to_move_to = doing_list_id
    elif item['status'] == "Complete": list_id_to_move_to = done_list_id

    response = requests.put(f'{base_uri}/cards/{item["id"]}', params={**query_params, 'idList': list_id_to_move_to})#

    if response.status_code != 200:
        raise ValueError(f'Failed to update todo item with id "{item["id"]}". Received status code {response.status_code}')


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

def get_item(id: str):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == id), None)


def add_item(title: str):
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


def delete_item(id: str):
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


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    update_item(item)

    return item

