FROM nikolaik/python-nodejs:latest

COPY . /root/web
RUN cd /root/web && \
    pip3 install -r requirements.txt && \
    npm install

# CMD ["gen_test_data.py"]
