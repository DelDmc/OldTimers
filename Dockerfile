FROM python:3.9

RUN apt update
RUN mkdir /oldtimers

WORKDIR /oldtimers

COPY ./src ./src
COPY ./commands ./commands

COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt
RUN chmod +x commands/start_server.sh


CMD ["commands/start_server.sh"]

#CMD ["python", "src/manage.py", "runserver", "0:8008"]