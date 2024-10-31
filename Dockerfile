FROM python:3.8
ENV HOME /root
WORKDIR /root
COPY . .
# Download dependancies
RUN pip3 install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
# RUN python3 -m pip install ffmpeg-python
EXPOSE 8000
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
CMD /wait && python -u server.py