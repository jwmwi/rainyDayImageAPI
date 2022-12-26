FROM python:3.8-slim-buster

WORKDIR /api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

## don't be this sloppy later
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
