FROM ghcr.io/binkhq/python:3.11
ARG APP_VERSION
WORKDIR /app
RUN pip install --no-cache api-reflector==$(echo ${APP_VERSION} | cut -c 2-)

ENTRYPOINT [ "gunicorn" ]
CMD [ "--error-logfile=-", "--access-logfile=-", "--bind=0.0.0.0:6502", "api_reflector.api:create_app" ]
