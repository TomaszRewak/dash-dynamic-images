from io import BytesIO
import json
from typing import Any, Dict, List
from urllib.parse import urlencode
import uuid
from dash import Input, Output
from werkzeug.datastructures import MultiDict
from PIL.Image import Image


def generate_unique_endpoint_id() -> str:
    return str(uuid.uuid4())


def generate_unique_image_path() -> str:
    return f'/image_generator/{generate_unique_endpoint_id()}.png'


def add_parameters_to_path(path: str, parameters: Dict[str, str]) -> str:
    encoded_parameters = urlencode(parameters, doseq=True)
    return f'{path}?{encoded_parameters}'


def extract_input_names(inputs_and_outputs: List[Input | Output]) -> List[str]:
    return [
        f'{arg.component_id}.{arg.component_property}'
        for arg in inputs_and_outputs
        if isinstance(arg, Input)
    ]


def extract_request_parameters(input_names: List[str], args: MultiDict[str, str]) -> List[Any]:
    return [
        json.loads(args.get(input_name))
        for input_name in input_names
    ]


def generate_request_parameters(input_names: List[str], values: List[Any]) -> Dict[str, str]:
    assert len(input_names) == len(values)

    encoded_values = [
        json.dumps(value)
        for value in values
    ]

    return dict(zip(input_names, encoded_values))

def convert_image_into_byte_stream(image: Image) -> BytesIO:
    image_io = BytesIO()
    image.save(image_io, 'PNG')
    image_io.seek(0)

    return image_io
