from dash_dynamic_images._utils import generate_unique_endpoint_id, generate_unique_image_path, add_parameters_to_path, extract_input_names, extract_request_parameters, generate_request_parameters, convert_image_into_byte_stream
from dash import Input, Output
from PIL import Image


def test_generate_unique_endpoint_id():
    endpoint_id_1 = generate_unique_endpoint_id()
    endpoint_id_2 = generate_unique_endpoint_id()

    assert endpoint_id_1 != endpoint_id_2


def test_generate_unique_image_path():
    image_path_1 = generate_unique_image_path()
    image_path_2 = generate_unique_image_path()

    assert image_path_1 != image_path_2


def test_add_parameters_to_path():
    path = '/image_path'
    parameters = {'a': '1', 'b': '2'}

    path_with_parameters = add_parameters_to_path(path, parameters)

    assert path_with_parameters == '/image_path?a=1&b=2'


def test_extract_input_names():
    inputs_and_outputs = [
        Input('component_id_1', 'component_property_1'),
        Input('component_id_2', 'component_property_2'),
        Output('component_id_3', 'component_property_3')
    ]

    input_names = extract_input_names(inputs_and_outputs)

    assert input_names == [
        'component_id_1.component_property_1',
        'component_id_2.component_property_2',
    ]


def test_extract_request_parameters():
    input_names = [
        'component_id_1.component_property_1',
        'component_id_2.component_property_2',
    ]
    args = {
        'component_id_1.component_property_1': '{"a": 1}',
        'component_id_2.component_property_2': '{"b": 2}',
    }

    request_parameters = extract_request_parameters(input_names, args)

    assert request_parameters == [
        {'a': 1},
        {'b': 2},
    ]


def test_generate_request_parameters():
    input_names = [
        'component_id_1.component_property_1',
        'component_id_2.component_property_2',
    ]
    values = [
        {'a': 1},
        {'b': 2},
    ]

    request_parameters = generate_request_parameters(input_names, values)

    assert request_parameters == {
        'component_id_1.component_property_1': '{"a": 1}',
        'component_id_2.component_property_2': '{"b": 2}',
    }


def test_convert_image_into_byte_stream():
    image = Image.new('RGB', (1, 1), (255, 0, 0))

    image_stream = convert_image_into_byte_stream(image)

    assert image_stream.read(
    ) == b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00\xc9\xfe\x92\xef\x00\x00\x00\x00IEND\xaeB`\x82'
