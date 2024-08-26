import os
import asyncio
from aiomqtt import Client
import logging
import requests
from sensors_lights_mapping import sensor_light_map
from dotenv import load_dotenv


load_dotenv()


# LOG_DIR = os.environ.get("LOG_DIR")
MQTT_PORT = os.environ.get("MQTT_PORT")
HOST = os.environ.get("HOST")
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
BASE_DECONZ_API_URL = os.environ.get("BASE_DECONZ_API_URL")
TOPIC = "sensors/magnet"

logger = logging.getLogger("MQTT_SENSOR_PUB")
logging.basicConfig(filename="logs.log", encoding='utf-8', level=logging.DEBUG)


def send_put_state_req_to_light(light_uuid, data):
    req = requests.put(f"{BASE_DECONZ_API_URL}lights/{light_uuid}/state", json=data)
    if req.status_code == 200:
        logging.info(f"Light turned on: {light_uuid}")
    else:
        logging.error(f"There was a problem with turning on the light: {light_uuid}, {req.text}")


def turn_on_light(light_uuid):
    logging.info(f"Turning on light: {light_uuid}")
    send_put_state_req_to_light(light_uuid,{"on": True} )


def turn_off_light(light_uuid):
    logging.info(f"Turning off light: {light_uuid}")
    send_put_state_req_to_light(light_uuid, {"on": False})


def handle_magnetic_sensor(data):
    light_uuid = sensor_light_map.get(data.get("uuid"), None)
    if not light_uuid:
        logging.warning(f"The magnetic sensor has not mapped light, sensor info: {data}")
        return

    if data.get("open") is True:
        turn_on_light(light_uuid)
    else:
        turn_off_light(light_uuid)



async def main():
    async with Client(
            hostname=HOST,
            port=int(MQTT_PORT),
            username=MQTT_USER,
            password=MQTT_PASSWORD,
    ) as client:
        await client.subscribe(TOPIC)
        async for message in client.messages:
            handle_magnetic_sensor(message)

if __name__ == "__main__":
    asyncio.run(main())
