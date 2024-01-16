FROM python:3.11

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py /home/app

CMD ["python3", "app.py"]
