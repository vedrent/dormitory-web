FROM python:3.11.4

WORKDIR /fastapi

RUN apt-get update && apt install -y netcat-traditional

RUN pip install --no-cache --upgrade pip setuptools
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .
CMD ["tail", "-f", "/dev/null"]
# ENTRYPOINT ["/fastapi/entrypoint.sh"]