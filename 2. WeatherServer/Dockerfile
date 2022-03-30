FROM python:3.7-alpine

LABEL maintainer="Soroush Mehraban <smehraban2013@gmail.com>"

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./

CMD python main.py
