# Start your image with a node base image
FROM python:3.12

RUN pip install poetry

COPY . /src

WORKDIR /src

RUN poetry install --only main --no-root

# Start the app using serve command
CMD ["poetry", "run", "python", "-u", "src/main.py"]