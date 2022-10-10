FROM ghcr.io/binkhq/python:3.10-poetry as build

WORKDIR /src
ADD . .

RUN poetry build

FROM ghcr.io/binkhq/python:3.10

WORKDIR /app
COPY --from=build /src/dist/*.whl .
COPY --from=build /src/wsgi.py .
RUN pip install *.whl && rm *.whl

ENTRYPOINT [ "gunicorn" ]

CMD [ "--workers=2", "--threads=2", "--error-logfile=-", \
    "--access-logfile=-", "--bind=0.0.0.0:6502", "wsgi" ]
