# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition

FROM server_base
COPY . /root/facial_features

WORKDIR /root/facial_features

ENTRYPOINT ["/bin/sh" ,"./docker-entrypoint.sh"]