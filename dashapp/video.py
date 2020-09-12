import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
from lxml import etree
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

video_url_list = []


app.layout = html.Div([
    dcc.Input(placeholder='请输入url...', type='input', id='url_input', style={'width': '50%'}),
    html.Button('提取url结果', 'b2'),
    dcc.Textarea(style={'width': '100%', 'height': '200px'}, id='textarea1'),
    html.Div(id='wapy1'),
    html.Button('切换', id='b1'),
    html.P(id='p1', style={'display': 'inline', 'paddingBottom': '500px'})
])


@app.callback(
    Output('textarea1', 'value'),
    [Input('b2', 'n_clicks')],
    [State('url_input', 'value')]
)
def func2(nclicks, start_url):
    global video_url_list

    print(start_url)
    url_prefix = 'https://pyone.dd111.xyz'
    while start_url:
        html1 = etree.HTML(requests.get(start_url).content)
        start_url_find_list = html1.xpath(r"//a[contains(text(),'»')]/@href")
        if len(start_url_find_list) > 0:
            start_url = url_prefix + start_url_find_list[0]
        else:
            start_url = None
        print(start_url)
        video_url_list.extend(
            [url_prefix+i for i in html1.xpath(r"//li/a/@href") if len(i) > 50 and i.find('page') == -1])
        print(len(video_url_list))
    return '\n\n'.join(video_url_list)


@app.callback(
    [Output('wapy1', 'children'), Output('p1', 'children')],
    [Input('b1', 'n_clicks')]
)
def fun1(ncliks):
    return [html.Video(src=url, style={'max-width': '50%', 'height': 'auto', 'verticalAlign': 'top'}, controls=True, autoPlay=True, loop=True) for url in gen_video_url_list(video_url_list)], '     剩余{}条'.format(len(video_url_list))


def gen_video_url_list(video_url_list):
    temp_list = []
    try:
        for _ in range(10):
            temp_list.append(video_url_list.pop())
    except:
        pass
    return temp_list


if __name__ == "__main__":
    app.run_server()
