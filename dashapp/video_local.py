import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os

app = dash.Dash(__name__)

video_path_list = []
for root, dirs_, files_ in os.walk('./static/img'):
    for file_ in files_:
        video_path_list.append(os.path.join(root, file_))
video_path_list.sort()


app.layout = html.Div([
    html.Div(
        [
            html.Video(src=url, style={'max-width': '50%', 'max-height': '900px', 'verticalAlign': 'top'}, controls=True, autoPlay=False, muted=False, loop=False)
            for url in video_path_list
        ]
    )
])


if __name__ == "__main__":
    app.run_server()
