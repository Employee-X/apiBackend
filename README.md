# Backend For API services

This is the backend for the Web API. It is built using FastApi and MongoDB.

## Installation

Install python3.8 and pip

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8 python3-pip
```

Install virtualenv

```bash
sudo apt install python3.8-venv
```

Create a virtual environment and activate it.

```bash
python3.8 -m venv venv
source venv/bin/activate
```

Install all the dependencies.
```bash
pip install -r requirements.txt
```
## Usage

```bash
python3 main.py
```

## Environment Variables

Create a ``.env.dev`` file in the root directory and add the following variables

```bash
DATABASE_URL=<mongodb_url>
secret_key=<secret_key>
```

## Contributing

Make changes to dev branch and create a pull request to merge with main.

Remember to do `pip freeze > requirements.txt` before pushing to dev.
