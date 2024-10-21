# Steps for project

- Create a new project directory and navigate to it
- Create a new virtual environment and activate it 
- Install FastAPI and Uvicorn: ```pip install fastapi uvicorn```
- Create a new directory named `app` and navigate to it
- Create a new file named main.py and write the following code:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}
```
- Create an init file with ```touch __init__.py``` into the app directory
- Create a Dockerfile with the following content:
```Dockerfile
FROM python:3.12-slim

WORKDIR /fastapi

COPY ./requirements.txt /fastapi/requirements.txt

COPY ./app /fastapi/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5700"]
```
- If you like can you create a requirements.txt file with the following content:
```txt
fastapi
uvicorn
```
or you can install the packages directly in the Dockerfile.
Alternative type the following command in the terminal:
```bash
pip freeze > requirements.txt
```
All packages will be saved in the requirements.txt file with a version number.

- Build the Docker image with the following command:
```bash
docker build -t fastapi_docker .
```

- Run the Docker container with the following command,
- with the `-d` flag to run the container in detached mode
- with `-p` flag to map the host port to the container port:
```bash
docker run -d --name fastapi_docker -p 5700:5700 fastapi_docker
```

 or 
```bash
docker run -p 5700:5700 fastapi_docker
```

- Open your browser and navigate to `http://localhost:5700` to see the message `Hello World!`

- To stop the container, type the following command:
```bash
docker stop fastapi_docker
```

- To remove the container, type the following command:
```bash
docker rm fastapi_docker
```

- To remove the image, type the following command:
```bash
docker rmi fastapi_docker
```
