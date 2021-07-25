import os

from dotenv.main import find_dotenv, load_dotenv
from todo_app.app import create_app
import pytest
from selenium import webdriver
from threading import Thread
from todo_app.data.trello_items import create_board, delete_board


@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True, verbose=True)
     # Create the new board & update the board id environment variable
    board_id = create_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    # construct the new application
    application = create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()

    yield application

    # Tear Down
    thread.join(1)
    delete_board(board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'