import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
import re

app = dash.Dash(__name__)

str1 = requests.get('https://boards.4chan.org/gif/thread/16376642').text
webm_url_list = list(set(['https:'+i for i in re.findall(r'href="(\S+?webm)',str1)]))

app.layout = html.Div([
    html.H1('hello dash!'),
    html.Div(
        [html.Iframe(src=url,style={'width':'90%','height':'650px'}) for url in webm_url_list[:5]]
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)