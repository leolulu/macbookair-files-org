import os
import dash_html_components as html
import dash_core_components as dcc
import dash
import os
from PIL import Image
import random
from typing import List

app = dash.Dash(__name__)

pic_max_height = 475

img_path_list = []
browserd_img_list = []


def get_img_path_list(img_path_list: List):
    temp_img_list = []
    for root, dirs_, files_ in os.walk('./static/img'):
        for file_ in files_:
            temp_img_list.append(os.path.join(root, file_))
    temp_img_list.sort()
    for temp_img in temp_img_list:
        if temp_img not in img_path_list and temp_img not in browserd_img_list:
            img_path_list.append(temp_img)
    return img_path_list


img_path_list = get_img_path_list(img_path_list)

pic_resolutions_sum = []
sample_num = int(len(img_path_list)/10)
for pic in random.sample(img_path_list, sample_num):
    try:
        pic_resolutions_sum.append(sum(Image.open(pic).size))
    except:
        pass
try:
    if len(pic_resolutions_sum) < sample_num*0.5:
        raise UserWarning()
    avg_pic_resolution_sum = sum(pic_resolutions_sum) / len(pic_resolutions_sum)
    page_capacity = int(100_000 / avg_pic_resolution_sum)
    print('平均分辨率和为{}，计算得出每页{}张图...'.format(avg_pic_resolution_sum, page_capacity))
except:
    page_capacity = 10

# img_path_list = [os.path.join('/static/img', i) for i in os.listdir('./static/img')]
# print(img_path_list)

# app.layout = html.Div([
#     html.Div(
#         [html.A(html.Img(src=img_path, style={'max-width': '25%', 'max-height': '600px', 'float': 'left'}), href=img_path, target='_blank') for img_path in img_path_list]
#     )
# ])

app.layout = html.Div([
    html.Div(style={'display': 'flex', 'flex-wrap': 'wrap',
                    'justify-content': 'left'}, id='container'),
    html.Div([
        html.Div(html.A(html.Button([
            html.Div(id='button_text'),
            html.Div(id='remain_count')
        ], id='get_pics'), href='#container')),
        html.Div(
            html.Div([
                dcc.Slider(min=10, max=300, step=10, value=page_capacity, updatemode='drag', id='slider1'),
                dcc.Slider(min=100, max=1500, step=1, value=pic_max_height, updatemode='drag', id='slider2')
            ], style={'display': 'flex', 'flex-direction': 'column'})
        )
    ], id='button_container', style={'float': 'right'})
])


@app.callback(
    [
        dash.dependencies.Output('container', 'children'),
        dash.dependencies.Output('remain_count', 'children')
    ],
    [
        dash.dependencies.Input('get_pics', 'n_clicks')
    ]
)
def popup_100_pics(n_clicks):
    global img_path_list
    return_list = []
    for idx in range(page_capacity):
        try:
            img_path = img_path_list.pop(0)
        except IndexError:
            break
        return_list.append(
            html.Video(
                src=img_path,
                muted=True, autoPlay=True, controls=True, loop=True,
                style={'max-height': '380px', 'vertical-align': 'middle'},
                id={'type': 'pics', 'index': idx}
            )
            if os.path.splitext(img_path)[-1].lower() in ['.mp4', '.mov', '.avi', '.flv', '.mkv', '.ts'] else
            html.A(html.Img(
                src=img_path,
                style={'max-height': '380px', 'vertical-align': 'middle'},
                id={'type': 'pics', 'index': idx}
            ), href=img_path, target='_blank')
        )
        browserd_img_list.append(img_path)
    if len(img_path_list) == 0:
        img_path_list = get_img_path_list(img_path_list)
    remain_count = '还剩{}张'.format(len(img_path_list))
    return return_list, remain_count


@app.callback(
    dash.dependencies.Output('button_text', 'children'),
    [
        dash.dependencies.Input('slider1', 'value')
    ]
)
def set_page_capacity(s_value):
    global page_capacity
    page_capacity = s_value
    button_text = '再来{}张！'.format(page_capacity)
    return button_text


@app.callback(
    dash.dependencies.Output({'type': 'pics', 'index': dash.dependencies.ALL}, 'style'),
    [dash.dependencies.Input('slider2', 'value')],
    [dash.dependencies.State('container', 'children')]
)
def det_pic_height(s_value, pics):
    global pic_max_height
    pic_max_height = s_value
    return [{'max-height': f'{pic_max_height}px', 'vertical-align': 'middle'} for i in range(len(pics))]


if __name__ == "__main__":
    app.run_server(debug=False)
