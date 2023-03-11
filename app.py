from flask import Flask, render_template
from flask import Flask, redirect, url_for, render_template
#from flask_sqlalchemy import SQLAlchemy
from dash import Dash, html, dcc, no_update
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output#, State, MATCH, ALL, no_update
#from dash.dependencies import no_update
import csv
import pandas as pd
import plotly.express as px
from sklearn.manifold import MDS
from extra import key
from data import *
#from extra import projected_features, urls, titles, channels, views
server = Flask(__name__);
#server.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(server)

API_KEY = key()
video_data = get_data(API_KEY,15,"US")
urls, titles, channels, views = parse_variables(video_data)
folder_thumbnails(urls)
images = [preprocess_image(f"thumbnails/image_{i}.jpg") for i in range(len(urls))]
images = np.array(images)
features = extract_features(images)
mds = MDS(n_components=2)
projected_features = mds.fit_transform(features)

with open("data.csv","a") as file:
    writer = csv.writer(file)
    for i in range(len(urls)):
        writer.writerow(tuple(video_data[i]))
with open("xy.csv", "a") as file:
    writer = csv.writer(file)
    for i in range(len(urls)):
        writer.writerow((projected_features[:, 0],projected_features[:, 1]))

#class Youtube(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
app = Dash(__name__, server=server, url_base_pathname='/Dashapp/')

colors = {
    'background': '#FFFFFF',
    'text': '#0008CF'
}
size = views
fig = go.Figure(data=[go.Scatter(
    x=projected_features[:, 0],
    y=projected_features[:, 1],
    #z=projected_features[:, 2],
    #color =views,
    mode='markers+text',
    marker=dict(
        color ="#BD00CC",
        size=views,
        sizemode='area',
        sizeref=2.*max(size)/(40.**2),
        sizemin=4
    ),
    text=titles
)])
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
navbar = html.Nav(
    children=[
        html.A("Home", href="/home"),
        html.A("Scene", href="/scene"),
        html.A("DashApp", href="/Dashapp"),
    ],
    className="navbar navbar-expand-lg navbar-dark bg-dark",
)
app.layout = html.Div(style={'backgroundColor': '#000000'}, children=[
    navbar,
    html.H1(
        children='Moodboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Multidimensional scaling of top youtube thumbnails', style={
        'textAlign': 'center',
        'color': '#000000'
    }),
    html.Div(className="container", children=[

    dcc.Graph(
        id='example-graph-2',
        figure=fig, clear_on_unhover=True
    ),
    dcc.Tooltip(
        id="graph-tooltip-5",
        direction="bottom"
              )
    ])
])

@app.callback(
    Output("graph-tooltip-5", "show"),
    Output("graph-tooltip-5", "bbox"),
    Output("graph-tooltip-5", "children"),
    Input("example-graph-2","hoverData"))
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    hover_data = hoverData["points"][0]
    bbox = hover_data["bbox"]
    num = hover_data["pointNumber"]
    img_src = urls[num]
    children = [
        html.Div([
            #html.H1(f"{num}",style={"color": "darkblue", "overflow-wrap": "break-word"}),
            html.Img(src=img_src, style={"width": "100%"}),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]
    
    return True, bbox, children



@server.route("/")
@server.route("/home")
def home():
    return render_template("index.html")

@server.route("/scene")
def threes():
    return render_template("scene.html")

if __name__ == '__main__':
    server.run(debug=True, port=5000)
