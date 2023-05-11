# dash-dynamic-images

A library that helps with embedding dynamic and generative images into Plotly Dash applications.

# Setting up

**1. Install the `dash-dynamic-images` python package**

```
pip install dash-dynamic-images
```

**2. Add an `html.Img` element to your page's layout**

This step does not differ in any way from the regular process of writing layouts for Dash applications.

```python
import dash_html_components as html

...

app.layout = html.Div(children=[
    html.Img(id='image'),
    ...
    dcc.Input(id='x', type='number', value=10),
    dcc.Input(id='y', type='number', value=10)
])
```

**3. Create an `image_callback` that serves your dynamic image**

You can use `image_callback` decorator to create callbacks that return dynamic images. It works similarly to the standard Dash `callback` decorator, but with few notable differences:

- The first argument of the decorator should be an instance of the `Dash` object.
- The callback should have only one output, pointing at the `src` property of an `Img` layout element.
- The decorated function should return a `PIL.Image.Image` object (from the `Pillow` python library).

```python
from dash_dynamic_images import image_callback
from PIL import Image, ImageDraw

...

@image_callback(
    app,
    dash.Output('image', 'src'),
    dash.Input('x', 'value'),
    dash.Input('y', 'value'))
def generate_image(x, y):
    image = Image.new('RGB', (200, 200), color=(0, 0, 200))
    ImageDraw.Draw(image).line([(0, 0), (x, y)], width=5)
    return image
```

As long as the returned object is a Pillow image, it does not matter on how was it create. You can generate it from scratch or obtain it from an external provider.

```python
import requests

...

@image_callback(
    app,
    dash.Output('image', 'src'),
    dash.Input('button', 'n_clicks'))
def generate_image(_):
    response = requests.get('https://your_service.example/api/images/get')

    return Image.open(BytesIO(response.content))
```

Please consult the `Pillow` documentation for more details.

**4. Enjoy the working application**

A complete example of an application:

```python
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_dynamic_images import image_callback
from PIL import Image, ImageDraw


app = dash.Dash()
app.layout = html.Div(children=[
    html.Img(id='image'),
    dcc.Input(id='x', type='number', value=10),
    dcc.Input(id='y', type='number', value=10)
])


@image_callback(
    app,
    dash.Output('image', 'src'),
    dash.Input('x', 'value'),
    dash.Input('y', 'value'))
def generate_image(x, y):
    image = Image.new('RGB', (200, 200), color=(0, 0, 200))
    ImageDraw.Draw(image).line([(0, 0), (x, y)], width=5)
    return image


if __name__ == '__main__':
    app.run_server(debug=True)
```

# How it works

Whenever an `image_callback` is registered, the library performs two operations:

- It registers a `flask` route with a path of `/image_generator/{unique_guid}.png` that generates and serves images whenever invoked.
- It registers a standard `Dash` callback that produces and returns a parametrized (through the query string) image url based on the `image_callback` input values.

In practice, whenever one of the `image_callback` input parameters change, a new url is generated and inserted into the `src` property of the `Img` element, which in orders triggers a process of requesting and producing a new image.

The generated images are not persisted in the file system.

The library is aligned with the stateless nature of the Dash framework and therefor is compatible with its horizontal scaling capabilities (where a single application can be served by multiple processes and/or machines).

# Motivation

This library aims at simplifying the process described in the previous section so that it can be achieved through a single line of a python code.