import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go


def __make_header(batch_id, batch_ids):
    return html.Div([
        html.H2('Select batch'),

        dcc.Dropdown(
            id='dropdown',
            options=[
                { 'label': value.replace('_', ' ').title(), 'value': value } 
                for value in sorted(list(batch_ids))
            ],
            value=batch_id
        ),

        html.Button('Refresh', id='button', value=batch_id)
    ], className='row')


def decorate(make):
    def wrapper(cache, batch_id):
        batch_ids = cache.get('batch_ids')
        page = make(cache, batch_id)

        return html.Div([
            __make_header(batch_id, batch_ids),
            html.Br([]),
            page
        ], className='container') 

    return wrapper


@decorate
def make(cache, batch_id):
    data = cache.get('data')
    
    if data is None:
        return html.Div([])

    batch_data = data[data['Batch ID'] == int(batch_id.split('_')[-1])].sort_values('Time', ascending=False)
    variables = batch_data.columns[1:31]
    raman_spectra = batch_data.columns[34:]

    return html.Div([
        # Plot for variables
        html.Div([
            dcc.Graph(
                id='variable_plot',
                figure={
                    'data': [
                        go.Scatter(
                            x=batch_data['Time'],
                            y=batch_data[variable],
                            line={
                                'width': 1
                            },
                            mode='lines',
                            name=variable,
                            visible='legendonly'
                        ) for variable in variables
                    ],
                    'layout': go.Layout(
                        font={
                            'family': 'Arial',
                            'size': 9
                        },
                        showlegend=True,
                        titlefont={
                            'family': 'Arial',
                            'size': 9,
                        },
                        xaxis={
                            'title': 'Time',
                            'showline': True,
                            'zeroline': False
                        },
                        yaxis={
                            'title': 'Value',
                            'showline': True,
                            'zeroline': False
                        }
                    )
                },
                config={
                    'displayModeBar': False
                }
            )
        ], className='six columns'),

        # Plot for Raman spectra
        html.Div([
            dcc.Graph(
                id='raman_plot',
                figure={
                    'data': [
                        go.Scatter(
                            x=raman_spectra,
                            y=batch_data[x],
                            line={
                                'width': 1
                            },
                            mode='lines',
                            hoverinfo='none',
                            name=x,
                        ) for x in raman_spectra
                    ],
                    'layout': go.Layout(
                        hovermode=False,
                        font={
                            'family': 'Arial',
                            'size': 9
                        },
                        showlegend=False,
                        titlefont={
                            'family': 'Arial',
                            'size': 9,
                        },
                        xaxis={
                            'title': 'Wavelength',
                            'showline': True,
                            'zeroline': False
                        },
                        yaxis={
                            'title': 'Intensity',
                            'showline': True,
                            'zeroline': False
                        }
                    )
                },
                config={
                    'displayModeBar': False
                }
            )
        ], className='six columns')
    ], className='row')