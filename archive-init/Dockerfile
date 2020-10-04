FROM python:alpine3.12

RUN pip install pymongo

COPY ./data/ /data
COPY ./init_db.py .

CMD python init_db.py
