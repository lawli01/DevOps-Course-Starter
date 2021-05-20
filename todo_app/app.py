from flask.globals import request
from todo_app.data.session_items import add_item, get_items
from flask import Flask, redirect
from flask.templating import render_template
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html', items=get_items())

@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    add_item(title)
    return redirect('/')


if __name__ == '__main__':
    app.run()
