FROM python:3.9
ARG VERSION
RUN pip install api-reflector==$VERSION

WORKDIR /app
ADD wsgi.py .

CMD [ "gunicorn", "--workers=2", "--threads=2", "--error-logfile=-", \
    "--access-logfile=-", "--bind=0.0.0.0:6502", "wsgi" ]
