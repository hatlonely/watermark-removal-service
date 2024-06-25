FROM watermark-removal-service-base

COPY ./app /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD [ "gunicorn", "-c", "config.py", "main:app" ]
