from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from PIL import Image
import base64
import io

# Load the image
image_path = 'img/DoDFanChart.png'
img = Image.open(image_path)

# Convert the image to base64
buffered = io.BytesIO()
img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# Get image dimensions
img_width, img_height = img.size
aspect_ratio = img_height / img_width

# Define the size based on aspect ratio
fig_width = 10
fig_height = fig_width * aspect_ratio

# Create the initial figure with the image
fig = go.Figure()

fig.add_layout_image(
    dict(
        source='data:image/png;base64,{}'.format(img_str),
        xref="x",
        yref="y",
        x=0,
        y=fig_height,
        sizex=fig_width,
        sizey=fig_height,
        sizing="stretch",
        opacity=1,
        layer="below"
    )
)

fig.update_xaxes(
    visible=False,
    range=[0, fig_width]
)

fig.update_yaxes(
    visible=False,
    range=[0, fig_height],
    scaleanchor="x"
)

# Create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div([
    dcc.Graph(id='interactive-chart', figure=fig),
    html.Div(id='mouse-coordinates'),
    html.Div([
        dcc.Input(id='vendor-info', type='text', placeholder='Enter vendor info'),
        dbc.Button('Add Point', id='add-point-button', n_clicks=0, color='primary')
    ]),
    dcc.Store(id='click-location', data={'x': 0, 'y': 0}),
])


@app.callback(
    Output('mouse-coordinates', 'children'),
    Input('interactive-chart', 'hoverData')
)
def display_coordinates(hover_data):
    if hover_data and 'points' in hover_data:
        x = hover_data['points'][0]['x']
        y = hover_data['points'][0]['y']
        return f'Mouse coordinates: x={x}, y={y}'
    return 'Mouse coordinates:'


@app.callback(
    Output('click-location', 'data'),
    Input('interactive-chart', 'clickData')
)
def store_click_location(click_data):
    if click_data and 'points' in click_data:
        click_location = {'x': click_data['points'][0]['x'], 'y': click_data['points'][0]['y']}
        return click_location
    return {'x': 0, 'y': 0}


@app.callback(
    Output('interactive-chart', 'figure'),
    Input('add-point-button', 'n_clicks'),
    State('vendor-info', 'value'),
    State('click-location', 'data'),
    State('interactive-chart', 'figure')
)
def update_graph(n_clicks, vendor_info, click_location, figure):
    if n_clicks > 0 and vendor_info:
        x = click_location['x']
        y = click_location['y']

        # Append new point to a text file
        with open('points.txt', 'a') as f:
            f.write(f'x: {x}, y: {y}, vendor_info: {vendor_info}\n')

        return figure

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
