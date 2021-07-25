import os

from dotenv.main import find_dotenv, load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
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
    os.environ['TRELLO_API_TODO_BOARD_ID'] = board_id
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


def add_todo(driver: WebDriver, todo_name: str):
    todo_input = driver.find_element_by_css_selector('[aria-label="todo input box"]')
    todo_input.send_keys(todo_name)
    add_todo_button = driver.find_element_by_css_selector('[aria-label="add todo"]')
    add_todo_button.click()


def click_todo_checkbox(driver: WebDriver, todo_name: str):
    driver.find_element_by_css_selector(f'[aria-label="todo {todo_name} checkbox"]').click()


def test_add_todo(driver: WebDriver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    add_todo(driver, todo_name="test")

    new_todo = driver.find_element_by_css_selector('[aria-label="todo test label"]')
    assert new_todo.text == 'test'
    assert driver.title == 'To-Do App'


def test_can_mark_todo_as_complete(driver: WebDriver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    click_todo_checkbox(driver, todo_name="test")

    is_checked = driver.find_element_by_css_selector(f'[aria-label="todo test checkbox"]').is_selected()

    assert is_checked == True


def test_can_mark_todo_as_not_complete(driver: WebDriver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    click_todo_checkbox(driver, todo_name="test")

    is_checked = driver.find_element_by_css_selector(f'[aria-label="todo test checkbox"]').is_selected()

    assert is_checked == False