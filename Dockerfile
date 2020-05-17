FROM python:3.6

WORKDIR /app

COPY src /app

RUN pip install -r requirements.txt

RUN mkdir -p /app/config

ENTRYPOINT ["python"]
CMD ["cpa.py"]