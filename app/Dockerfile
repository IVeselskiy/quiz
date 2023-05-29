FROM python:3-alpine

WORKDIR /app

COPY . /app

RUN python -m pip install -r /app/requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]