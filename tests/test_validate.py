import json
import os

import pytest
from jsonschema import validate, Draft202012Validator

from quranbot_schema_registry.validate_schema import _get_definition_file_path, validate_schema, BASE_DIR


def test_get_definition_file_path():
    got = _get_definition_file_path('Task.Added', 1)

    assert got == 'schemas/task/added/1.json'


def test_validate_schema():
    got = validate_schema(
        {
            "event_id": "some_id",
            "event_version": 1,
            "event_name": "event_name",
            "event_time": "392409283",
            "producer": "some producer",
            "data": {
                "text": "mailing text",
            },
        },
        event_name='Mailing.created',
        version=1,
    )


@pytest.mark.parametrize('file_path', [
    f'{x[0]}/{x[2][0]}'
    for x in os.walk(BASE_DIR / 'schemas')
    if len(x[2]) > 0
])
def test_schemas(file_path):
    with open(file_path, 'r') as schema_file:
        schema = Draft202012Validator(schema=json.load(schema_file))
