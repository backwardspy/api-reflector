FROM ghcr.io/binkhq/python:3.11-poetry as build

ENV VENV /app/venv

WORKDIR /src
ADD . .

RUN python -m venv $VENV
ENV VIRTUAL_ENV=$VENV
ENV PATH=$VENV/bin:$PATH

COPY pyproject.toml poetry.lock .
RUN poetry install --without=dev --no-root
COPY . .
RUN poetry build && pip install --no-deps dist/*.whl

FROM ghcr.io/binkhq/python:3.11

WORKDIR /app

ENV VENV /app/venv
ENV PATH="$VENV/bin:$PATH"

COPY --from=build /src/wsgi.py .
COPY --from=build $VENV $VENV

ENTRYPOINT [ "gunicorn" ]
CMD [ "--error-logfile=-", "--access-logfile=-", "--bind=0.0.0.0:6502", "wsgi" ]
