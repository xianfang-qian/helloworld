FROM openvino/ubuntu18_dev:latest

CMD ["/bin/bash"]

WORKDIR /
COPY run.sh /
COPY server.py /
ENTRYPOINT source run.sh

