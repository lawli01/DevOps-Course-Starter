FROM python:3-buster as base
WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/usr/src/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install gunicorn

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY ./poetry.toml ./poetry.toml
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
RUN /root/.local/bin/poetry config virtualenvs.create false \
  && /root/.local/bin/poetry install
COPY ./todo_app ./todo_app

# production build stage
FROM base as production
EXPOSE 5000
CMD ["gunicorn", "--workers=2", "app:create_app()", "--bind", ":5000", "--chdir", "/usr/src/app/todo_app"]  

# local development stage
FROM base as development
EXPOSE 5000
CMD ["/root/.local/bin/poetry", "run", "flask", "run", "--host", "0.0.0.0"]

FROM base as test
COPY ./tests ./tests
COPY ./tests_e2e ./tests_e2e
ENV GECKODRIVER_VER v0.29.1
# Install the long-term support version of Firefox (and curl if 
# you don't have it already)
RUN apt-get update && apt-get install -y firefox-esr curl
 
# Download geckodriver and put it in the usr/bin folder
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
 && tar zxf geckodriver-*.tar.gz \
 && mv geckodriver /usr/bin/ \
 && rm geckodriver-*.tar.gz
ENTRYPOINT ["/root/.local/bin/poetry", "run", "pytest"]