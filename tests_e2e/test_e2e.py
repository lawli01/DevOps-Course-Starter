import os

from dotenv.main import find_dotenv, load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from todo_app.app import create_app
import pytest
import pymongo
from selenium import webdriver
from threading import Thread
from todo_app.data.mongo_items import MONGO_CLIENT


@pytest.fixture(scope='module')
def app_with_temp_db():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True, verbose=True)
     # Update the mongo db name environment variable
    test_db = "Todo_e2e_tests"
    os.environ['MONGO_DATABASE_NAME'] = test_db
    # construct the new application
    application = create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()

    yield application

    # Tear Down
    thread.join(1)
    mongoClient = pymongo.MongoClient(f'{os.environ["MONGO_CONNECTION_STRING"]}')
    mongoClient.drop_database(test_db)


@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.headless = True
    with webdriver.Firefox(options=opts) as driver:
        yield driver


def add_todo(driver: WebDriver, todo_name: str):
    todo_input = driver.find_element_by_css_selector('[aria-label="todo input box"]')
    todo_input.send_keys(todo_name)
    add_todo_button = driver.find_element_by_css_selector('[aria-label="add todo"]')
    add_todo_button.click()


def click_todo_checkbox(driver: WebDriver, todo_name: str):
    driver.find_element_by_css_selector(f'[aria-label="todo {todo_name} checkbox"]').click()


def test_add_todo(driver: WebDriver, app_with_temp_db):
    driver.get('http://localhost:5000/')
    add_todo(driver, todo_name="test")

    new_todo = driver.find_element_by_css_selector('[aria-label="todo test label"]')
    assert new_todo.text == 'test'
    assert driver.title == 'To-Do App'


def test_can_mark_todo_as_complete(driver: WebDriver, app_with_temp_db):
    driver.get('http://localhost:5000/')
    click_todo_checkbox(driver, todo_name="test")

    is_checked = driver.find_element_by_css_selector(f'[aria-label="todo test checkbox"]').is_selected()

    assert is_checked == True


def test_can_mark_todo_as_not_complete(driver: WebDriver, app_with_temp_db):
    driver.get('http://localhost:5000/')
    click_todo_checkbox(driver, todo_name="test")

    is_checked = driver.find_element_by_css_selector(f'[aria-label="todo test checkbox"]').is_selected()

    assert is_checked == False