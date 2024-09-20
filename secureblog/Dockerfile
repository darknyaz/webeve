FROM ubuntu:24.10

RUN apt update && apt install -y python3 python3-pip

COPY src /app

WORKDIR /app

RUN pip3 install -r requirements.txt --break-system-packages

EXPOSE 5000

ENTRYPOINT ["flask", "--app", "app", "run", "--host", "0.0.0.0"]

