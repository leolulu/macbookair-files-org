import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
from urllib.parse import urljoin

app = dash.Dash(__name__)

video_path_list = [
    '//i.4cdn.org/gif/1598624562511.webm',
    '//is2.4chan.org/gif/1598624595813.webm',
    '//i.4cdn.org/gif/1598624634224.webm',
    '//i.4cdn.org/gif/1598624704083.webm',
    '//i.4cdn.org/gif/1598639239772.webm',
    '//i.4cdn.org/gif/1598653536129.webm',
    '//i.4cdn.org/gif/1598656615398.webm',
    '//is2.4chan.org/gif/1598656677270.webm',
    '//is2.4chan.org/gif/1598656716639.webm',
    '//is2.4chan.org/gif/1598657183291.webm',
    '//i.4cdn.org/gif/1598657222676.webm',
    '//is2.4chan.org/gif/1598657274269.webm',
    '//i.4cdn.org/gif/1598657312691.webm',
    '//is2.4chan.org/gif/1598657348550.webm',
    '//is2.4chan.org/gif/1598657385586.webm',
    '//i.4cdn.org/gif/1598657421633.webm',
    '//is2.4chan.org/gif/1598657460219.webm',
    '//is2.4chan.org/gif/1598657518042.webm',
    '//i.4cdn.org/gif/1598677614721.webm',
    '//is2.4chan.org/gif/1598727850517.webm',
    '//i.4cdn.org/gif/1598754498189.webm',
    '//is2.4chan.org/gif/1598754538458.webm',
    '//is2.4chan.org/gif/1598754580070.webm',
    '//is2.4chan.org/gif/1598754639205.webm',
    '//i.4cdn.org/gif/1598754678914.webm',
    '//is2.4chan.org/gif/1598754739526.webm',
    '//is2.4chan.org/gif/1598754795521.webm'
]

video_path_list = [urljoin('https://boards.4chan.org/gif/thread/17797350', i) for i in video_path_list]
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
