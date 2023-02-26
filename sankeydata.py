from dice import diceroll as dr
import plotly.graph_objects as go
import pandas as pd
import nbformat

def calc_data(dice_shape, dice_start, dice_stop, n):
    # url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    # response = urllib.request.urlopen(url)
    # data = json.loads(response.read()) # replace with your own data source
    outcome = dr.dice(sides = dice_shape,values= list(range(dice_start, dice_stop + 1)), max_n= n)
    rolls = outcome.melted.loc[outcome.melted['n'] == n,:]

    link_1_group = rolls.groupby(['n','die'])['value'].count().reset_index()
    link_2_group = rolls.groupby(['die','result'])['n'].count().reset_index()
    # link_1_group['value'] = link_1_group['value']/link_1_group['value'].sum()
    # link_2_group['value'] = link_2_group['value']/link_2_group['value'].sum()
    dice_source_map = {d : f'{d} Dice' for i, d in enumerate(link_1_group['n'])}
    result_source_map = {d: f'{d} roll' for d in link_2_group['result']}
    link_1_group['n'] = link_1_group['n'].map(dice_source_map)
    link_2_group['result'] = link_2_group['result'].map(result_source_map)
    link_1_group.columns = ['source','target','value']

    link_2_group.columns = ['source','target','value']

    # link_1_group['value'] = link_1_group['value']/link_1_group['value'].sum()
    # link_2_group['value'] = link_2_group['value']/link_2_group['value'].sum()


    links = pd.concat([link_1_group, link_2_group], axis=0)
    unique_source_target = list(pd.unique(links[['source', 'target']].values.ravel('C')))
    mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
    links['source'] = links['source'].map(mapping_dict)
    links['target'] = links['target'].map(mapping_dict)
    links_dict = links.to_dict(orient='list')

    data = {'links' : links_dict, 'labels' : unique_source_target}

    return data


def test():
    a = calc_data(6, 1, 6, 2)
    print()

if __name__ == "__main__":
    test()