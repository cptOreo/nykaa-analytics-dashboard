import re

with open('app.py', 'r') as f:
    app_text = f.read()

old_scenarios = """def build_page_scenarios(year):
    return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.methodology_badge('07', txt.BADGE_MODEL),
            html.Div(className='hairline-top', style={'backgroundColor': 'var(--bg-color)', 'padding': '24px 0'}, children=[
                html.Div("MODEL INPUTS", className='giant-label', style={'marginBottom': '24px'}),
                html.Div([html.Label("ADJUST CONTRIBUTION MARGIN (%)"), dcc.Slider(id='scen-cm', min=0, max=10, step=0.5, value=0, marks={i:f"+{i}%" for i in range(0,11,2)})], style={'marginBottom': '32px'}),
                html.Div([html.Label("REDUCE COMMERCIAL SPEND (AS % OF NSV)"), dcc.Slider(id='scen-mkt', min=0, max=10, step=0.5, value=0, marks={i:f"-{i}%" for i in range(0,11,2)})], style={'marginBottom': '32px'}),
                html.Div([html.Label("REDUCE FULFILMENT SPEND (AS % OF NSV)"), dcc.Slider(id='scen-ful', min=0, max=5, step=0.5, value=0, marks={i:f"-{i}%" for i in range(0,6)})], style={'marginBottom': '32px'}),
                html.Div([html.Label("INCREASE ORDERS PER CUSTOMER (%)"), dcc.Slider(id='scen-ord', min=0, max=50, step=5, value=0, marks={i:f"+{i}%" for i in range(0,51,10)})], style={'marginBottom': '32px'}),
                html.Div([html.Label("INCREASE AVERAGE ORDER VALUE (%)"), dcc.Slider(id='scen-aov', min=0, max=30, step=2, value=0, marks={i:f"+{i}%" for i in range(0,31,10)})]),
            ]),
            html.Div(id='scenario-annotation')
        ]),
        html.Div(className='main-column', children=[
            html.Div("Orders required to break even", className='editorial-statement'),
            html.Div("Required volume shifts alongside contribution per order.", className='editorial-substatement'),
            html.Div(id='scenario-results', style={'marginTop': '16px'})
        ])
    ])"""

new_scenarios = """def build_page_scenarios(year):
    lbl_style = {'fontSize': '10px', 'fontWeight': '800', 'display': 'block', 'marginBottom': '4px', 'lineHeight': '1.1', 'letterSpacing': '0.5px'}
    row_style = {'marginBottom': '16px'}
    
    return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.methodology_badge('07', txt.BADGE_MODEL),
            html.Div(className='hairline-top', style={'backgroundColor': 'var(--bg-color)', 'padding': '16px 0'}, children=[
                html.Div("MODEL INPUTS", className='giant-label', style={'marginBottom': '16px'}),
                html.Div([html.Label("ADJUST CONTRIBUTION MARGIN (%)", style=lbl_style), dcc.Slider(id='scen-cm', min=0, max=10, step=0.5, value=0, marks={i:f"+{i}%" for i in range(0,11,2)})], style=row_style),
                html.Div([html.Label("REDUCE COMMERCIAL SPEND (AS % OF NSV)", style=lbl_style), dcc.Slider(id='scen-mkt', min=0, max=10, step=0.5, value=0, marks={i:f"-{i}%" for i in range(0,11,2)})], style=row_style),
                html.Div([html.Label("REDUCE FULFILMENT SPEND (AS % OF NSV)", style=lbl_style), dcc.Slider(id='scen-ful', min=0, max=5, step=0.5, value=0, marks={i:f"-{i}%" for i in range(0,6)})], style=row_style),
                html.Div([html.Label("INCREASE ORDERS PER CUSTOMER (%)", style=lbl_style), dcc.Slider(id='scen-ord', min=0, max=50, step=5, value=0, marks={i:f"+{i}%" for i in range(0,51,10)})], style=row_style),
                html.Div([html.Label("INCREASE AVERAGE ORDER VALUE (%)", style=lbl_style), dcc.Slider(id='scen-aov', min=0, max=30, step=2, value=0, marks={i:f"+{i}%" for i in range(0,31,10)})], style={'marginBottom': '8px'}),
            ]),
            html.Div(id='scenario-annotation')
        ]),
        html.Div(className='main-column', children=[
            html.Div("Orders required to break even", className='editorial-statement'),
            html.Div("Required volume shifts alongside contribution per order.", className='editorial-substatement'),
            html.Div(id='scenario-results', style={'marginTop': '16px'})
        ])
    ])"""

app_text = app_text.replace(old_scenarios, new_scenarios)

with open('app.py', 'w') as f:
    f.write(app_text)
