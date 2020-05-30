import os
import dash_html_components as html
import dash_core_components as dcc
import dash
import os

app = dash.Dash(__name__)

img_path_list = []
for root, dirs_, files_ in os.walk('./static/img'):
    for file_ in files_:
        img_path_list.append(os.path.join(root, file_))


# img_path_list = [os.path.join('/static/img', i) for i in os.listdir('./static/img')]
print(img_path_list)

app.layout = html.Div([
    html.Div(
        [html.A(html.Img(src=img_path, style={'max-width': '25%', 'max-height': '340px', 'float': 'left'}), href=img_path, target='_self') for img_path in img_path_list]
    )
])

if __name__ == "__main__":
    app.run_server()
