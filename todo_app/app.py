from todo_app.data.itemsViewModel import ItemsViewModel
from todo_app.data.item import ItemStatus
from todo_app.data.trello_items import get_items, add_item, delete_item, get_item, save_item
from flask import Flask, redirect, render_template, request
from todo_app.flask_config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    @app.route('/')
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
