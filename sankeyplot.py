from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import json, urllib
from sankeydata import calc_data

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Dice Outcomes'),
    dcc.Graph(id="graph"),
    html.P("dice_start"),
    dcc.Slider(id='dice_start', min=0, max=6, 
               value=1, step=1),
    html.P("dice stop"),
    dcc.Slider(id='dice_stop', min=0, max=6, 
               value=6, step=1),
    html.P("n dice"),
    dcc.Slider(id='n_dice', min=1, max=8, 
               value=2, step=1)
])

@app.callback(
    Output("graph", "figure"), 
    Input("dice_start", "value"),
    Input("dice_stop", "value"),
    Input("n_dice", "value"))
def display_sankey(dice_start,dice_stop,n_dice):
    
    feed = calc_data(6, dice_start,dice_stop,n_dice)
    links_dict = feed['links']

    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = feed['labels'],
      color = "blue"
    ),
    link = dict(
      source = links_dict["source"],
      target = links_dict["target"],
      value = links_dict["value"]
  ))])
    fig.update_layout(title_text="dice outcomes", font_size=10)
    fig.update_layout(height = 750)
    return fig
    # fig.show()
    
    
    
    # url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    # response = urllib.request.urlopen(url)
    # data = json.loads(response.read()) # replace with your own data source

    # node = data['data'][0]['node']
    # node['color'] = [
    #     f'rgba(255,0,255,{opacity})' 
    #     if c == "magenta" else c.replace('0.8', str(opacity)) 
    #     for c in node['color']]

    # link = data['data'][0]['link']
    # link['color'] = [
    #     node['color'][src] for src in link['source']]

    # fig = go.Figure(go.Sankey(link=link, node=node))
    # fig.update_layout(font_size=10)
    # return fig

app.run_server(debug=True)