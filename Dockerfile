FROM python:3.9
ARG VERSION
RUN pip install api-reflector==$VERSION
