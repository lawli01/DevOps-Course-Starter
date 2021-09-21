FROM python:3-buster
WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/usr/src/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install gunicorn
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
COPY ./todo_app ./todo_app
COPY ./poetry.toml ./poetry.toml
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
RUN /root/.poetry/bin/poetry config virtualenvs.create false \
  && /root/.poetry/bin/poetry install
EXPOSE 5000
CMD ["gunicorn", "--workers=2", "app:create_app()", "--bind", ":5000", "--chdir", "/usr/src/app/todo_app"]  
