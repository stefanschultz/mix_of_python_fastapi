# mix_of_python_fastapi
Mix of different projects to test the tech stack of Python, FastAPI, Pydantic and more...

## First step create a virtual environment and install the dependencies

You need to have python 3.12 installed in your system. You can install it using the following commands for python, pip and venv.
Activate the virtual environment and install the dependencies using the requirements.txt file.

```bash
sudo apt-get install python3.12
sudo apt-get install python3.12-pip
sudo apt-get install python3.12-venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To deactivate the virtual environment use the following command:

```bash
deactivate
```

## Run the FastAPI server

To run the FastAPI server use the following command:

```bash
uvicorn main:app --reload
```

## Test the FastAPI server

To test the FastAPI server use the following command:

```bash
curl -X 'GET' \
  'http://
```

or type in your browser the url `http://127.0.0.1:8000/`

## FastAPI Swagger docs
You can open with your browser the following URL to see the FastAPI docs from Swagger:

```bash
http://127.0.0.1:8000/docs/
```
