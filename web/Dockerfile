FROM nikolaik/python-nodejs:latest

COPY . /root/web
WORKDIR /root/web
RUN pip3 install -r requirements.txt && \
    npm install

WORKDIR /root/web
ENTRYPOINT ["/bin/sh" ,"./docker-entrypoint.sh"]
