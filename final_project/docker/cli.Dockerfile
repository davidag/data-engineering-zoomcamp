FROM prefecthq/prefect:2.9-python3.9

# Required for Python mysqlclient package
RUN apt-get update && \
    apt-get install --no-install-recommends -y default-libmysqlclient-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY cli.requirements.txt requirements.txt

RUN python3 -m pip install -U -r requirements.txt

RUN python3 -c 'import nltk; nltk.download("punkt")'

CMD ["/bin/bash", "-c"]
