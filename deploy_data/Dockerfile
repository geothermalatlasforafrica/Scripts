FROM thinkwhere/gdal-python

ENV GEOSERVER_URL=https://gaa-proxy.azurewebsites.net/geoserver
ENV API_URL=http://host.docker.internal:3001

RUN pip install geoserver-rest pyyaml validators openpyxl dataclasses
