import dash_html_components as html
import dash_core_components as dcc
import dash
import re

app = dash.Dash(__name__)

pic_height = 100

with open('rarbg_chrome_console_crawl.js', 'r', encoding='utf-8') as f:
    img_url_page_url_list = f.read().split('\n')
img_url_page_url_list = [i.split(' ')[1:3] for i in list(filter(lambda x:re.match(r'VM\d{4}', x), img_url_page_url_list))]


container_content = []
for idx, img_url_page_url in enumerate(img_url_page_url_list):
    container_content.append(
        html.A(html.Img(
            src=img_url_page_url[0],
            style={'height': f'{pic_height}px', 'vertical-align': 'middle'},
            id={'type': 'pics', 'index': idx}
        ), href=img_url_page_url[1], target='_blank'))

app.layout = html.Div([
    html.Div(container_content, style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'left'}, id='container'),
    html.Div(
        dcc.Slider(min=100, max=1500, step=1, value=pic_height, updatemode='drag', id='slider2'), id='button_container', style={'float': 'right'}
    )
])


@app.callback(
    dash.dependencies.Output({'type': 'pics', 'index': dash.dependencies.ALL}, 'style'),
    [dash.dependencies.Input('slider2', 'value')],
    [dash.dependencies.State('container', 'children')]
)
def det_pic_height(s_value, pics):
    global pic_height
    pic_height = s_value
    return [{'height': f'{pic_height}px', 'vertical-align': 'middle'} for i in range(len(pics))]


if __name__ == "__main__":
    app.run_server(debug=False)
