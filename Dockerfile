FROM python:3.9
ARG VERSION
RUN for _ in 1 2 3 4 5; do pip install api-reflector==$VERSION; if [ $? -eq 0 ]; then break; else sleep 60; fi; done

WORKDIR /app
ADD wsgi.py .

CMD [ "gunicorn", "--workers=2", "--threads=2", "--error-logfile=-", \
    "--access-logfile=-", "--bind=0.0.0.0:6502", "wsgi" ]
