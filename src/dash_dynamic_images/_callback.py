from typing import Callable, List
from dash import Dash, Input, Output
from flask import request, send_file
from dash_dynamic_images._utils import extract_input_names, extract_request_parameters, generate_unique_image_path, convert_image_into_byte_stream, generate_request_parameters, add_parameters_to_path
from PIL.Image import Image


def callback(app: Dash, *inputs_and_outputs: List[Input | Output]):
    input_names = extract_input_names(inputs_and_outputs)

    def decorator(image_generator: Callable[..., Image]):
        image_path = generate_unique_image_path()

        @app.server.route(image_path)
        def serve_image():
            parameters = extract_request_parameters(input_names, request.args)

            image = image_generator(*parameters)
            image_stream = convert_image_into_byte_stream(image)

            return send_file(image_stream, mimetype='image/png')

        @app.callback(*inputs_and_outputs)
        def generate_url(*args):
            parameters = generate_request_parameters(input_names, args)

            return add_parameters_to_path(image_path, parameters)

        return image_generator

    return decorator
