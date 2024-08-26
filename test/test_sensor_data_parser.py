import pytest
from publisher.sensor_data_parser import (parse_data_to_dict, is_sensor_event, is_magnetic_sensor_event,
                                          create_magnetic_sensor_data)

magnetic_sensor_raw_str = ('{"e":"changed","id":"24","r":"sensors",'
                           '"state":{"lastupdated":"2024-08-23T18:09:11.244","open":false}, '
                           '"t":"event","uniqueid":"00:15:8d:00:03:58:39:e5-01-0006"}')


@pytest.mark.parametrize(("data", "expected"), [
    (magnetic_sensor_raw_str,
     {'e': 'changed', 'id': '24', 'r': 'sensors', 'state':
        {'lastupdated': '2024-08-23T18:09:11.244', 'open': False}, 't': 'event',
      'uniqueid': '00:15:8d:00:03:58:39:e5-01-0006'}),
])
def test_parse_data_to_dict(data, expected):
    assert parse_data_to_dict(data) == expected


@pytest.mark.parametrize(("data", "expected"), [
    (magnetic_sensor_raw_str, True),
    ('{"attr":{"id":"1","lastannounced":null,"lastseen":"2024-08-23T18:09Z","manufacturername":"LUMI",'
     '"modelid":"lumi.ctrl_ln1.aq1","name":"pierdolnik","swversion":"06-25-2018",'
     '"type":"Smart plug","uniqueid":"00:15:8d:00:04:2b:ef:77-01"},'
     '"e":"changed","id":"1","r":"lights","t":"event","uniqueid":"00:15:8d:00:04:2b:ef:77-01"}',
     False),
])
def test_is_sensor_event(data, expected):
    assert is_sensor_event(parse_data_to_dict(data)) is expected


@pytest.mark.parametrize(("data", "expected"), [
    (magnetic_sensor_raw_str, True),
    ('{"e":"changed","id":"24","r":"sensors","state":{"lastupdated":"2024-08-23T18:09:11.244","value": "234"},'
     '"t":"event","uniqueid":"00:15:8d:00:03:58:39:e5-01-0006"}', False),
    ('{"attr":{"id":"1","lastannounced":null,"lastseen":"2024-08-23T18:09Z","manufacturername":"LUMI",'
     '"modelid":"lumi.ctrl_ln1.aq1","name":"pierdolnik","swversion":"06-25-2018",'
     '"type":"Smart plug","uniqueid":"00:15:8d:00:04:2b:ef:77-01"},'
     '"e":"changed","id":"1","r":"lights","t":"event","uniqueid":"00:15:8d:00:04:2b:ef:77-01"}',
     False),
])
def test_is_magnetic_sensor_event(data, expected):
    assert is_magnetic_sensor_event(parse_data_to_dict(data)) is expected


@pytest.mark.parametrize(("data", "expected"), [
    (magnetic_sensor_raw_str, {
            "uuid": '00:15:8d:00:03:58:39:e5-01-0006',
            "open": False,
            "last_updated": "2024-08-23T18:09:11.244"
        }),
])
def test_create_magnetic_sensor_raw_str(data, expected):
    assert create_magnetic_sensor_data(parse_data_to_dict(data)) == expected
