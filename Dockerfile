FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY app /app
COPY chat.py /
COPY requirements.txt /
WORKDIR /
RUN pip3 install -r /requirements.txt
ENTRYPOINT ["python3"]
CMD ["chat.py"]
