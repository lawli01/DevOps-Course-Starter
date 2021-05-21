from flask.globals import request
from todo_app.data.session_items import add_item, get_item, get_items, save_item
from flask import Flask, redirect
from flask.templating import render_template
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = get_items()
    print(items)
    return render_template('index.html', items=items)

@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    add_item(title)
    return redirect('/')

@app.route('/todos/<id>', methods=['POST'])
def update_todo(id):
    status = request.form.get('status')
    item = get_item(id)
    item['status'] = 'Complete' if status == 'Complete' else 'Not Started'
    save_item(item)
    return redirect('/')


if __name__ == '__main__':
    app.run()
