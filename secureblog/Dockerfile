FROM ubuntu:noble

RUN apt update && apt install -y python3 python3-pip libssl-dev wkhtmltopdf iproute2 iputils-ping dnsutils

COPY src /app

WORKDIR /app

RUN pip3 install -r requirements.txt --break-system-packages
RUN chmod +x run.sh

ENTRYPOINT ["./run.sh"]

