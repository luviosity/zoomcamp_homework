FROM python:3.9

WORKDIR /app

COPY requirements.txt trip_data_ingest.py zones_data_ingest.py entrypoint.sh /app/

RUN apt-get install wget && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod +x entrypoint.sh

ENTRYPOINT ["bash"]