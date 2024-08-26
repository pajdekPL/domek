FROM python:3-alpine3.13

ADD magnetic_sensor_handler.py .
ADD sensor_data_parser.py .
ADD requirements.txt .

RUN pip install -r requirements.txt


CMD ["python", "./magnetic_sensor_handler.py"]