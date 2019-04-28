import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go


def decorate(make):
    def wrapper(cache, batch_id):
        return html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=[
                    { 'label': value, 'value': value } 
                    for value in sorted(list(cache.get('batch_ids')))
                ],
                value=batch_id
            ),

            html.Br([]),

            html.Button('Refresh', id='button', value=batch_id),

            html.Br([]),

            # Actual page for a batch
            make(cache, batch_id)
        ]) 

    return wrapper


@decorate
def make(cache, batch_id):
    batch_cache = cache.get(batch_id)
    
    if batch_cache is None:
        return html.Div([])

    return html.Div([
        # Plot for variables


        # Plot for Raman spectra
    ])