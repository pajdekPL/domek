import os
import asyncio
from websockets.asyncio.client import connect
import json
import logging
from sensor_data_parser import (is_magnetic_sensor_event, create_magnetic_sensor_data, parse_data_to_dict,
                                MagenticSensorData)
from aiomqtt import Client, MqttCodeError
from dotenv import load_dotenv


load_dotenv()

WS_URL = os.environ.get("WS_URL")
LOG_DIR = os.environ.get("LOG_DIR")
TOPIC = "sensors/magnet"
MQTT_PORT = os.environ.get("MQTT_PORT")
HOST = os.environ.get("HOST")
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")


logger = logging.getLogger("MQTT_SENSOR_PUB")
logging.basicConfig(filename=LOG_DIR, encoding='utf-8', level=logging.DEBUG)


async def publish_magnetic_sensor_event_to_mqtt(mqtt_client, data: MagenticSensorData):
    logging.info(f"publishing {data} to topic: {TOPIC}")
    try:
        await mqtt_client.publish(TOPIC, json.dumps(data))
    except MqttCodeError as error:
        logging.error(f"MQTT There was a problem with publish {data} to {TOPIC}, error: {error}")
    logging.info(f"data successfully published")


def on_ws_message_with_mqtt_client(mqtt_client):
    mqtt_client = mqtt_client
    def on_ws_message(ws, message):
        message_data = parse_data_to_dict(message)
        if is_magnetic_sensor_event(message_data):
            publish_magnetic_sensor_event_to_mqtt(mqtt_client, create_magnetic_sensor_data(message_data))
    return on_ws_message


async def handle_ws_messages(mqtt_client, uri):
    async with connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            message_data = parse_data_to_dict(message)
            if is_magnetic_sensor_event(message_data):
                await publish_magnetic_sensor_event_to_mqtt(mqtt_client, create_magnetic_sensor_data(message_data))


async def main():
    async with Client(
            hostname=HOST,  # The only non-optional parameter
            port=int(MQTT_PORT),
            username=MQTT_USER,
            password=MQTT_PASSWORD,
    ) as mqtt_client:
        await handle_ws_messages(mqtt_client, f"ws://{WS_URL}")

if __name__ == "__main__":
    asyncio.run(main())
