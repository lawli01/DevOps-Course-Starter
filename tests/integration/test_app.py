import os
from todo_app.app import create_app
from unittest.mock import Mock, patch
import pytest
import dotenv
import json

from pathlib import Path

THIS_DIR = Path(__file__).parent

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


@patch('requests.get')
def test_index_page(mock_get_requests, client):
    with open(THIS_DIR/'trello_responses/get_boards_lists.json') as jsonFile:
        testLists = json.load(jsonFile)
        jsonFile.close()
    to_do_list_id = next(x for x in testLists if x['name'] == "To Do")["id"]
    doing_list_id = next(x for x in testLists if x['name'] == "Doing")["id"]
    done_list_id = next(x for x in testLists if x['name'] == "Done")["id"]
    def mock_get_lists(url, params):
        response = Mock()
        if url == f'https://api.trello.com/1/boards/{os.environ["TRELLO_API_TODO_BOARD_ID"]}/lists':
            response.json.return_value = testLists
            return response
        elif url == f'https://api.trello.com/1/lists/{to_do_list_id}/cards':
            response.json.return_value = []
            return response
        elif url == f'https://api.trello.com/1/lists/{doing_list_id}/cards':
            response.json.return_value = []
            return response
        elif url == f'https://api.trello.com/1/lists/{done_list_id}/cards':
            response.json.return_value = []
            return response
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')
    return None