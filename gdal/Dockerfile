FROM python:3.13.7

RUN apt-get update -y
RUN apt-get install -y gdal-bin libgdal-dev
RUN apt-get install -y python3-gdal
RUN apt-get install -y binutils libproj-dev

RUN pip install gunicorn==23.0.0
