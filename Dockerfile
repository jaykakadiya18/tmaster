#FROM python:3-alpine3.15
FROM python:3.8-slim
WORKDIR /
COPY . /
RUN pip3 install -r requirements.txt
EXPOSE 5000
#CMD python3 ./main.py
CMD ["python3", "app.py"]

