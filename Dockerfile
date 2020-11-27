FROM python:3.9.0

COPY labo_negaposi /negaposi/labo_negaposi

RUN pip install -r /negaposi/labo_negaposi/setup/requirements.txt

RUN python /negaposi/labo_negaposi/app.py
