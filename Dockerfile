FROM openvino/ubuntu18_dev:latest
USER root
RUN apt-get update
RUN pip3 install --upgrade pip \
  && pip3 install opencv-python
RUN pip3 install flask
RUN pip3 install influxdb
RUN cd 
WORKDIR ./
COPY run.py .
ENTRYPOINT python3 run.py
