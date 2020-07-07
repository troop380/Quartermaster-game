FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY app /app
WORKDIR /app
RUN pip3 install -r /app/requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
