FROM --platform=linux/amd64 ubuntu:22.04
LABEL authors="Max Esser"

ENV DB_SCHEMA=backend
ENV DB_USER=root
ENV DB_PASS=real_good_password
ENV DB_HOST=localhost
ENV DB_PORT=3306

EXPOSE 105/tcp

WORKDIR /backend
COPY . .

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3.11 python3-pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "flask-api.py"]