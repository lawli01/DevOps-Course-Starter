import os
from flask import Flask, redirect, render_template, request
from dotenv import load_dotenv
from flask_login import LoginManager, login_required
from oauthlib.oauth2 import WebApplicationClient
from todo_app.data.item import ItemStatus
from todo_app.data.mongo_items import get_item, get_items, add_item, delete_item, save_item
from todo_app.data.itemsViewModel import ItemsViewModel
load_dotenv()


def create_app():
    """
    Create the todo app

    Returns:
        app: The flask application.
    """ 
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        client = WebApplicationClient(os.environ['OAUTH_CLIENT_ID'])
        oauth_get_uri = client.prepare_request_uri("https://github.com/login/oauth/authorize")
        return redirect(oauth_get_uri, code=302)
        
    @login_manager.user_loader
    def load_user(user_id):
        return None

    login_manager.init_app(app) 

    @app.route('/')
    @login_required
    def index():
        items = get_items()
        items_view_model = ItemsViewModel(items)
        return render_template('index.html', view_model=items_view_model)

    @app.route('/todos', methods=['POST'])
    def add_todo():
        title = request.form.get('title')
        add_item(title)
        return redirect('/')

    @app.route('/todos/<id>', methods=['POST'])
    def update_todo(id):
        status = request.form.get('status')
        item = get_item(id)
        item.status = ItemStatus.COMPLETE if status == 'COMPLETE' else ItemStatus.NOT_STARTED
        save_item(item)
        return redirect('/')

    @app.route('/todos/<id>/delete', methods=['POST'])
    def remove_todo(id):
        delete_item(id)
        return redirect('/')

    return app

if __name__ == '__main__':
    create_app().run()
