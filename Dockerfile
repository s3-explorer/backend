FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY s3-explorer.conf /etc/nginx/conf.d/s3-explorer.conf

RUN apt update && apt upgrade -y
RUN apt install python3 -y
RUN apt install python3-pip -y

WORKDIR /app
COPY start-service.sh .
COPY . .
RUN pip3 install -r requirements.txt
RUN chmod +x start-service.sh

EXPOSE 80
EXPOSE 5000

CMD ["./start-service.sh"]
