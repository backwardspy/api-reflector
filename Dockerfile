FROM ghcr.io/binkhq/python:3.11-poetry as build

WORKDIR /src
ADD . .

RUN poetry build

FROM ghcr.io/binkhq/python:3.11

WORKDIR /app
COPY --from=build /src/dist/*.whl .
COPY --from=build /src/wsgi.py .
RUN pip install *.whl && rm *.whl

ENTRYPOINT [ "gunicorn" ]
CMD [ "--error-logfile=-", "--access-logfile=-", "--bind=0.0.0.0:6502", "wsgi" ]
