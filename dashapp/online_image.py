import os
import dash_html_components as html
import dash_core_components as dcc
import dash
from dash.dependencies import Input,Output,State
import requests
from lxml import etree

app = dash.Dash(__name__)



app.layout = html.Div([
    html.Div(html.Span("//ul[@id='post-list-posts']/li/a/@href")),
    dcc.Textarea(style={'width':'75%','height':'300px'},id='input1'),
    html.Button('显示',id='b1'),
    html.Div(id='pic_list_container')
])

@app.callback(
    Output('pic_list_container','children'),
    [Input('b1','n_clicks')],
    [State('input1','value')]
)
def get_large_image_url(n_clicks,url_value):
    url_list = [i.strip() for i in url_value.split('\n')]
    return [html.A(html.Img(src=img_path,style={'max-width':'100%','max-height':'680px','float':'left'}),href=img_path,target='_self') for img_path in url_list]


if __name__ == "__main__":
    app.run_server()