import json
from typing import TypedDict


class MagenticSensorData(TypedDict):
    uuid: str
    open: bool
    last_updated: str


def parse_data_to_dict(mqtt_data: str) -> dict:
    return json.loads(mqtt_data)


def is_sensor_event(mqtt_parsed_data: dict) -> bool:
    """
    DeConz sensor data format"
    '{"e": "changed", "id": "24", "r": "sensors", "state": {"lastupdated": "2024-08-23T18:09:11.244", "open": false},
    "t": "event", "uniqueid": "00:15:8d:00:03:58:39:e5-01-0006"}'
    :param mqtt_parsed_data:
    :return:
    """
    if mqtt_parsed_data.get("r", None) == "sensors" and mqtt_parsed_data.get("e", None) == "changed":
        return True
    return False


def is_magnetic_sensor_event(mqtt_parsed_data: dict) -> bool:
    """
    DeConz magnetic sensor data format"
    '{"e": "changed", "id": "24", "r": "sensors", "state": {"lastupdated": "2024-08-23T18:09:11.244", "open": false},
    "t": "event", "uniqueid": "00:15:8d:00:03:58:39:e5-01-0006"}'
    :param mqtt_parsed_data:
    :return:
    """
    if is_sensor_event(mqtt_parsed_data):
        if "state" in mqtt_parsed_data and "open" in mqtt_parsed_data["state"]:
            return True
    return False


def create_magnetic_sensor_data(mqtt_parsed_data: dict) -> MagenticSensorData:
    data: MagenticSensorData = {
            "uuid": mqtt_parsed_data.get("uniqueid", ""),
            "open": mqtt_parsed_data["state"]["open"],
            "last_updated": mqtt_parsed_data["state"]["lastupdated"]
        }
    return data


class MagenticSensorData(TypedDict):
    uuid: str
    open: bool
    last_updated: str
