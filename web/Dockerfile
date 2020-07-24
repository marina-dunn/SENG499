FROM nikolaik/python-nodejs:latest

COPY . /root/web
WORKDIR /root/web
RUN pip3 install -r requirements.txt && \
    npm install

ENTRYPOINT ["/bin/sh" ,"./docker-entrypoint.sh"]

# CMD ["gen_test_data.py"]
