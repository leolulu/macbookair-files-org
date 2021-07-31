import dash_html_components as html
import dash_core_components as dcc
import dash
import re

app = dash.Dash(__name__)

pic_height = 200

with open('rarbg_data.data', 'r', encoding='utf-8') as f:
    img_url_page_url_list = f.read().split('\n')
img_url_page_url_list = [re.sub(r"VM\d+:\d+", '', i).replace("\u200b", "").strip().split(",") for i in list(filter(lambda x:re.search(r'http.*?rarbg', x), img_url_page_url_list))]
img_url_page_url_list = [(i[0].split('.')[0], i[1], i[2]) for i in img_url_page_url_list]
img_url_page_url_list.sort(key=lambda x: x[0])
for i in img_url_page_url_list[::-1]:
    with open('rarbg.history', 'r', encoding='utf-8') as f:
        his = f.read().split('\n')
    if str(i) not in his:
        print(i)
        with open('rarbg.history', 'a', encoding='utf-8') as f:
            f.write('\n'+str(i))
    else:
        img_url_page_url_list.remove(i)
# print(img_url_page_url_list)


container_content = []
previous_brand = ''
batch_img_content = []
for idx, img_url_page_url in enumerate(img_url_page_url_list):
    brand = img_url_page_url[0]
    if brand != previous_brand:
        container_content.extend(batch_img_content)
        batch_img_content = []
        container_content.append(html.H1(brand, style={"width": "100%"}))
    previous_brand = brand
    batch_img_content.append(
        html.A(html.Img(
            src=img_url_page_url[1],
            style={'height': f'{pic_height}px', 'verticalAlign': 'middle'},
            id={'type': 'pics', 'index': idx}
        ), href=img_url_page_url[2], target='_blank'))
if batch_img_content:
    container_content.extend(batch_img_content)

app.layout = html.Div([
    html.Div(container_content, style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'left'}, id='container'),
    html.Div(
        dcc.Slider(min=100, max=1500, step=1, value=pic_height, updatemode='drag', id='slider2'), id='button_container', style={'float': 'right'}
    )
])


@app.callback(
    dash.dependencies.Output({'type': 'pics', 'index': dash.dependencies.ALL}, 'style'),
    [dash.dependencies.Input('slider2', 'value')],
    dash.dependencies.State({'type': 'pics', 'index': dash.dependencies.ALL}, 'children')
)
def det_pic_height(s_value, pics):
    global pic_height
    pic_height = s_value
    return [{'height': f'{pic_height}px', 'verticalAlign': 'middle'} for i in range(len(pics))]


if __name__ == "__main__":
    app.run_server(debug=False)
