FROM python:3.8
WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install --upgrade -r requirements.txt

# Get env file using curl
RUN curl -o .env.dev https://employeex.s3.ap-south-1.amazonaws.com/.env.dev

EXPOSE 8080

COPY ./ /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
