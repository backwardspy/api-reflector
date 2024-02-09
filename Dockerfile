FROM ghcr.io/binkhq/python:3.11
ARG APP_VERSION
WORKDIR /app
ADD wsgi.py .
RUN pip install --no-cache api-reflector==$(echo ${APP_VERSION} | cut -c 2-)

ENTRYPOINT [ "gunicorn" ]
CMD [ "--error-logfile=-", "--access-logfile=-", "--bind=0.0.0.0:6502", "wsgi" ]
