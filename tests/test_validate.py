from pathlib import Path
import uuid
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
    ('File.SendTriggered', 1, {'file_id': str(uuid.uuid4()), 'source': 'disk'}),
    ('Messages.Created', 1, {'messages': [{'message_json': {}, 'is_unknown': False, 'trigger_message_id': None, 'trigger_callback_id': None, 'mailing_id': None}]}),
    ('Button.Pushed', 1, {'json': {}, 'timestamp': '843795'}),
    ('User.Subscribed', 1, {'user_id': 843795, 'referrer_id': None, 'date_time': '893475'}),
    ('Ayat.Changed', 1, {
        'public_id': '0acec6b6-4b3c-4ce9-8d11-3985f52a1c03',
        'day': 2,
        'audio_id': 'a2ed8d0e-ce4b-4994-9a12-e36482263cb7',
        'ayat_number': '1-3',
        'content': 'Updated content',
        'arab_text': 'Updated arab text',
        'transliteration': 'Updated arab transliteration',
    }),
    ('DailyContent.Created', 1, {'day': 2, 'ayat_ids': [1, 2, 3]}),
    ('Prayers.Created', 1, {'prayers': [{
        'name': 'fajr',
        'time': '5:36',
        'city_id': '4075504b-4b6f-4978-bf9c-8ecd5ecf9192',
        'day': '2023-01-02',
    }]}),
    ('Mailing.DailyAyats', 1, {}),
    ('Mailing.DailyPrayers', 1, {}),
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
    Draft202012Validator(schema=json.loads(Path(file_path).read_text()))


@pytest.mark.parametrize('file_path', [
    f'{x[0]}/{x[2][0]}'
    for x in os.walk(BASE_DIR / 'schemas')
    if len(x[2]) > 0
])
def test_formats(file_path):
    file_content = Path(file_path).read_text().strip()

    assert file_content == json.dumps(json.loads(file_content), indent=2)
