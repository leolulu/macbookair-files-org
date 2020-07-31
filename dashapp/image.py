import os
import dash_html_components as html
import dash_core_components as dcc
import dash
import os

app = dash.Dash(__name__)

page_capacity = 50
img_path_list = []
for root, dirs_, files_ in os.walk('./static/img'):
    for file_ in files_:
        img_path_list.append(os.path.join(root, file_))
img_path_list.sort()


# img_path_list = [os.path.join('/static/img', i) for i in os.listdir('./static/img')]
# print(img_path_list)

# app.layout = html.Div([
#     html.Div(
#         [html.A(html.Img(src=img_path, style={'max-width': '25%', 'max-height': '600px', 'float': 'left'}), href=img_path, target='_blank') for img_path in img_path_list]
#     )
# ])

app.layout = html.Div([
    html.Div(style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'left'}, id='container'),
    html.Div([
        html.Div(html.A(html.Button([html.Div(id='button_text'), html.Div(id='remain_count')], id='get_pics'), href='#container')),
        html.Div(dcc.Slider(min=10, max=500, step=10, value=page_capacity, updatemode='drag', id='slider1'))
    ], id='button_container'
    )
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
    return_list = []
    for _ in range(page_capacity):
        try:
            img_path = img_path_list.pop(0)
        except IndexError:
            break
        return_list.append(
            html.A(html.Img(src=img_path, style={'max-height': '380px', 'vertical-align': 'middle'}), href=img_path, target='_blank')
        )
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


if __name__ == "__main__":
    app.run_server()
