FROM python:3-alpine3.13

ADD sensor_mqtt_publisher.py .
ADD sensor_data_parser.py .
ADD requirements.txt .

RUN pip install -r requirements.txt


CMD ["python", "./sensor_mqtt_publisher.py"]