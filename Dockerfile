FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./project ./project
COPY ./tests ./tests
COPY run.py .
ENV FLASK_APP=run

CMD flask run -h 0.0.0.0 -p 80