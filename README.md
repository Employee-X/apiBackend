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
python3.8 -m venv env_employeex
source env_employeex/bin/activate
```

Install all the dependencies.
```bash
pip install -r requirements.txt
```
## Usage

```bash
python main.py
```

## Environment Variables

Create a ``.env.dev`` file in the root directory and add the following variables

```bash
DATABASE_URL=<mongodb_url>
secret_key=<secret_key>

AWS_ACCESS_KEY_ID=<aws_access_key_id>
AWS_SECRET_ACCESS_KEY=<aws_secret_access_key>
AWS_REGION=<aws_region>
S3_BUCKET=<s3_bucket_name>
S3_KEY=<s3_key>
```

## Contributing

Make changes to dev branch and create a pull request to merge with main.

Remember to do `pip freeze > requirements.txt` before pushing to dev.
