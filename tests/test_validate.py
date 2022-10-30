import json
import os

import pytest
from jsonschema import Draft202012Validator

from quranbot_schema_registry.validate_schema import _get_definition_file_path, validate_schema, BASE_DIR


def test_get_definition_file_path():
    got = _get_definition_file_path('Task.Added', 1)

    assert got == 'schemas/task/added/1.json'


@pytest.mark.parametrize('event_name,event_version,event_data', [
    ('Mailing.Created', 1, {'text': 'mailing text'}),
    ('File.SendTriggered', 1, {'file_id': 123}),
    ('Messages.Created', 1, {'messages': [{'message_json': {}, 'is_unknown': False, 'trigger_message_id': None}]}),
    ('Button.Pushed', 1, {'json': {}, 'timestamp': '843795'}),
    ('User.Subscribed', 1, {'user_id': 843795, 'referrer_id': None, 'date_time': '893475'}),
    ('Prayers.Sended', 1, {}),
])
def test_validate_schema(event_name, event_version, event_data):
    validate_schema(
        {
            "event_id": "some_id",
            "event_version": 1,
            "event_name": "event_name",
            "event_time": "392409283",
            "producer": "some producer",
            "data": event_data,
        },
        event_name=event_name,
        version=event_version,
    )


@pytest.mark.parametrize('file_path', [
    f'{x[0]}/{x[2][0]}'
    for x in os.walk(BASE_DIR / 'schemas')
    if len(x[2]) > 0
])
def test_schemas(file_path):
    with open(file_path, 'r') as schema_file:
        Draft202012Validator(schema=json.load(schema_file))
