from todo_app.data.item import ItemStatus
from todo_app.data.trello_items import get_items, add_item, delete_item, get_item, save_item
from flask import Flask, redirect, render_template, request
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = get_items()
    sorted_by_status = sorted(items, key=lambda item: item.status, reverse=True)
    return render_template('index.html', items=sorted_by_status)

@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    add_item(title)
    return redirect('/')

@app.route('/todos/<id>', methods=['POST'])
def update_todo(id):
    status = request.form.get('status')
    item = get_item(id)
    item.status = ItemStatus.COMPLETE if status == 'Complete' else ItemStatus.NOT_STARTED
    save_item(item)
    return redirect('/')

@app.route('/todos/<id>/delete', methods=['POST'])
def remove_todo(id):
    delete_item(id)
    return redirect('/')


if __name__ == '__main__':
    app.run()
