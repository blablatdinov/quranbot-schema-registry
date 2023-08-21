import json
from pathlib import Path

from jsonschema import validate, ValidationError


BASE_DIR = Path(__file__).parent


def validate_schema(event: dict, event_name: str, version: int):
    definition_file_path = BASE_DIR / _get_definition_file_path(event_name, version)
    try:
        schema = json.loads(definition_file_path.read_text())
    except FileNotFoundError:
        raise TypeError(f'Schema file for event {event_name} version: {version} not found')
    try:
        validate(instance=event, schema=schema)
    except ValidationError as e:
        raise TypeError('Schema file: {}. Error: {}'.format(definition_file_path, str(e)))


def _get_definition_file_path(event_name: str, version: int) -> str:
    return 'schemas/{}/{}.json'.format(
        event_name.lower().replace('.', '/'),
        version,
    )
