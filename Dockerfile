FROM python:3.9

RUN apt update
RUN mkdir /oldtimers

WORKDIR /oldtimers

COPY ./src ./src
COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

CMD ["python", "src/manage.py", "runserver", "0:8008"]