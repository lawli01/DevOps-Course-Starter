# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

In the .env file you will need to add a configuration with your own mongo connection details:
```
# Example connection string: mongodb+srv://{USER}:{PASSWORD}@{HOST}
MONGO_CONNECTION_STRING=[YOUR CONNECTION STRING]
# This is the database where all the todo items will be stored
MONGO_DATABASE_NAME=[YOUR MONGO DATABASE NAME]
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

To edit and delete todo items you need to add your github user id to the user id to role map in users.py

## Running the integration and unit tests

In visual studio code:
 - Hit ctrl+shift+p and search for "Python: Discover Tests"
 - Configure pytest as the test runner pointing to the ./tests folder
 - Ensure you have the "Python Test Explorer for Visual Studio Code" extension installed
 - You should be able to run the tests now using the test explorer in visual studio code

 Alternatively you can just run the `pytest tests` command once you have activated the python venv

## Running the e2e tests

 Prequisites:
  - Download and install firefox
  - Download geckodriver and place it in the project root

run `pytest tests_e2e`

## Running the tests in docker

Run the following to build the test image:
 - docker build --target test --tag my-test-image .

Run the following to run the unit/integration tests:
 - docker run --env-file .env.test my-test-image tests

Run the following to run the e2e tests:
 - docker run --env-file .env my-test-image tests_e2e

## Building and running the Docker container

Run:
 - To build and run development image:
   - docker build --target development --tag todo-app:dev .
   - docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/usr/src/app/todo_app todo-app:dev
 - To build and run production image:
   - docker build --target production --tag todo-app:prod .
   - docker run -p 5000:5000 --env-file ./.env todo-app:prod