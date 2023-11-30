FROM python:3.11-bullseye

RUN apt-get update \
    && apt-get install -y build-essential \
    # opencsv dependencie
    libgl1 \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt