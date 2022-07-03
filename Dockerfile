FROM python:3.9

RUN apt update
RUN mkdir /oldtimers

WORKDIR /oldtimers

COPY ./src ./src
COPY ./commands ./commands

COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt
RUN chmod -R 750 ./commands -R

CMD ["bash"]