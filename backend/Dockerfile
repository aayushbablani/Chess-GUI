FROM python:latest
LABEL authors="Max Esser"

ENV DB_SCHEMA=backend
ENV DB_USER=root
ENV DB_PASS=real_good_password
ENV DB_HOST=localhost
ENV DB_PORT=33060

EXPOSE 80/tcp

WORKDIR /backend

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]