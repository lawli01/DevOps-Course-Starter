import pytest
import mongomock
import pymongo
from dotenv.main import find_dotenv, load_dotenv
from todo_app.app import create_app

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True, verbose=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)): 
        test_app = create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    mockData = [
        {
            "title": "foo",
            "status": "Not Started"
        },
        {
            "title": "bar",
            "status": "In Progress"
        },
        {
            "title": "blah",
            "status": "Complete"
        }
    ]
    mongoClient = pymongo.MongoClient('mongodb://fakemongo.com')['Todo']
    mongoClient.items.insert_many(mockData)

    response = client.get('/')
    responseBody = response.data.decode("utf-8")

    assert response.status_code is 200
    assert "foo" in responseBody
    assert "bar" in responseBody
    assert "blah" in responseBody
