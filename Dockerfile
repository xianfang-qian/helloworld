FROM openvino/ubuntu18_dev:latest

CMD ["/bin/bash"]

#COPY app /app
#COPY intel /intel
USER root
#RUN apt-get update && apt-get install -y wget libcanberra-gtk-module libcanberra-gtk3-module git
RUN pip3 install --upgrade pip \
  && pip3 install opencv-python
#WORKDIR /app
WORKDIR /
COPY run.sh /
COPY server.py /
COPY requirements.txt /
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENTRYPOINT source run.sh

