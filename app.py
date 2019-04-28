from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

from flask_caching import Cache

import layout


dash_app = Dash(__name__)
dash_app.server.name = 'IndPenSim'
dash_app.config['supress_callback_exceptions'] = True
# dash_app.index_string = '''
#     <!DOCTYPE html>
#     <html>
#         <head>
#             {%meta%}
#             <link rel="shortcut icon" type="image/png" href"assets/icon.png"/>
#             {%css%}
#         </head>
#         <body>
#             {%app_entry%}
#             <footer>
#                 {%config%}
#                 {%scripts%}
#             </footer>
#         </body
#     </html>
# '''
dash_app.layout = html.Div([
    dcc.Location(
        id='url',
        refresh=False
    ),
    html.Div(id='page-content')
])

@dash_app.callback(
    Output('button', 'value'), [
        Input('dropdown', 'value')
    ]
)
def pass_batch_id_to_button(batch_id):
    return batch_id


@dash_app.callback(
    Output('url', 'pathname'), [
        Input('button', 'n_clicks')
    ], [
        State('button', 'value')
    ]
)
def refresh_page(n_clicks, batch_id):
    return '/' + batch_id


def display_page(url, cache):
    page = cache.get(url)

    if page is None:
        return html.Div([
            html.P('404 page not found')
        ])

    return page


if __name__ == '__main__':
    data = pd.read_csv('data/sample.csv')

    cache = Cache(
        dash_app.server,
        config=dict(
            CACHE_TYPE='filesystem',
            CACHE_DIR='.cache',
            CACHE_THRESHOLD=1e3
        )
    )

    cache.clear()
    batch_ids = set(['batch_{}'.format(batch_id) for batch_id in data['Batch ID']])
    cache.set('batch_ids', batch_ids, timeout=0)

    for batch_id in batch_ids:
        cache.set('/' + batch_id, layout.make(cache, batch_id))

    dash_app.callback(
        output=Output('page-content', 'children'),
        inputs=[Input('url', 'pathname')]
    )(lambda url: display_page(url, cache))

    dash_app.run_server(
        host='0.0.0.0',
        threaded=True,
        debug=False,
        use_reloader=False
    )