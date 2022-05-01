FROM python:2.7-alpine

ARG version=dart
ENV POX_VERSION $version

RUN rm -Rf /temp && mkdir /temp && cd /temp && \
    pip install networkx && \
    wget https://github.com/noxrepo/pox/archive/$POX_VERSION.zip && \
    unzip -o $POX_VERSION.zip && \
    mkdir -p /usr/src/pox && \
    cp -r /temp/pox-$POX_VERSION/* /usr/src/pox && \
    rm -Rf /temp/pox-$POX_VERSION && rm $POX_VERSION.zip

WORKDIR "/usr/src/pox"

ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]
