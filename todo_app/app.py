from functools import wraps
import json
import os
import requests
from flask import Flask, abort, redirect, render_template, request
from dotenv import load_dotenv
from flask_login import LoginManager, current_user, login_required, login_user
from oauthlib.oauth2 import WebApplicationClient
from todo_app.data.item import ItemStatus
from todo_app.data.mongo_items import get_item, get_items, add_item, delete_item, save_item
from todo_app.data.itemsViewModel import ItemsViewModel
from todo_app.data.user import User, Role, user_id_to_role
load_dotenv()

def authorised_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = getattr(current_user, "id", None)
            user_role = user_id_to_role.get(str(user_id), Role.READER)

            login_disabled = os.environ.get("LOGIN_DISABLED", False) 
            if (login_disabled == False and role == Role.WRITER and user_role != Role.WRITER):
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def create_app():
    """
    Create the todo app

    Returns:
        app: The flask application.
    """ 
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

    login_manager = LoginManager()
    oauth_client_id = os.environ['OAUTH_CLIENT_ID']
    oauth_client_secret = os.environ['OAUTH_CLIENT_SECRET']
    client = WebApplicationClient(oauth_client_id)

    @login_manager.unauthorized_handler
    def unauthenticated():
        oauth_get_uri = client.prepare_request_uri(uri="https://github.com/login/oauth/authorize", state="todoapp")
        return redirect(oauth_get_uri, code=302)
        
    @login_manager.user_loader
    def load_user(user_id):
        return User(id=user_id, role=user_id_to_role.get(str(user_id), Role.READER))

    login_manager.init_app(app) 

    @app.route('/')
    @authorised_role(role=Role.READER)
    @login_required
    def index():
        items = get_items()
        items_view_model = ItemsViewModel(items)
        print(current_user.__dict__)
        return render_template('index.html', view_model=items_view_model, user=current_user)

    @app.route('/login/callback')
    def login_callback():
        code = request.args.get("code")
        post_token_request = client.prepare_token_request("https://github.com/login/oauth/access_token", state="todoapp", client_id=oauth_client_id, client_secret=oauth_client_secret, code=code)
        (post_token_url, post_token_headers, post_token_body) = post_token_request
        post_token_headers["Accept"] = "application/json"
        token_response = requests.post(post_token_url, data=post_token_body, headers=post_token_headers)
        client.parse_request_body_response(token_response.text)
        (get_user_url, get_user_headers, _) = client.add_token("https://api.github.com/user")
        user_response = requests.get(get_user_url, headers=get_user_headers).json()
        user = User(id=user_response["id"])
        login_user(user)
        return redirect('/')

    @app.route('/todos', methods=['POST'])
    @authorised_role(role=Role.WRITER)
    @login_required
    def add_todo():
        title = request.form.get('title')
        add_item(title)
        return redirect('/')

    @app.route('/todos/<id>', methods=['POST'])
    @authorised_role(role=Role.WRITER)
    @login_required
    def update_todo(id):
        status = request.form.get('status')
        item = get_item(id)
        item.status = ItemStatus.COMPLETE if status == 'COMPLETE' else ItemStatus.NOT_STARTED
        save_item(item)
        return redirect('/')

    @app.route('/todos/<id>/delete', methods=['POST'])
    @authorised_role(role=Role.WRITER)
    @login_required
    def remove_todo(id):
        delete_item(id)
        return redirect('/')

    return app

if __name__ == '__main__':
    create_app().run()

