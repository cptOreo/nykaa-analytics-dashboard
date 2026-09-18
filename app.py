"""
Nykaa Editorial Dashboard - app.py
"""

from dash import Dash, html, dcc, callback, Input, Output, State
import dash
import pandas as pd
import numpy as np
from urllib.parse import parse_qs, urlencode

from data_loader import load_financial_data, load_customer_data, FINANCIAL_DATA, get_years
from kpi_calculations import compute_all_financial_kpis, calculate_return_rate_survey, calculate_purchase_frequency, calculate_aov_proxy, calculate_repeat_purchase_rate
import components as c

app = Dash(__name__, suppress_callback_exceptions=True, title="Nykaa Analytics — Data Story")

# ─── Data Loading ───────────────────────────────────────────────────
YEARS = get_years()
df_fin = load_financial_data()
try:
    df_cust = load_customer_data()
except Exception as e:
    df_cust = pd.DataFrame()
    print("Warning: Could not load customer CSV.", e)

def _get(data, segment, metric, year):
    return data.get(segment, {}).get(metric, {}).get(year)

def _kpis(year, segment):
    return compute_all_financial_kpis(FINANCIAL_DATA, year, segment)

def _safe(val, default=None):
    if val is None or (isinstance(val, float) and np.isnan(val)): return default
    return val

# ─── Navigation ─────────────────────────────────────────────────────
NAV_ITEMS = [
    ('/', '01', 'THE GAP'),
    ('/where-money-goes', '02', 'PROFITABILITY'),
    ('/growth', '03', 'GROWTH'),
    ('/customer', '04', 'THE CUSTOMER'),
    ('/returns', '05', 'RETURNS'),
    ('/acquisition', '06', 'ACQUISITION'),
    ('/scenarios', '07', 'SCENARIOS'),
    ('/propositions', '08', 'PROPOSITIONS'),
]

def make_sidebar():
    nav_links = []
    for href, num, label in NAV_ITEMS:
        nav_links.append(
            dcc.Link([
                html.Span(num, className='nav-num'),
                label
            ], href=href, id=f'nav-{href.strip("/") or "home"}', className='nav-link')
        )
    
    return html.Div(className='sidebar', children=[
        html.Div(className='sidebar-brand', children=[
            html.H2("NYKAA"),
            html.P("FASHION × BEAUTY")
        ]),
        html.Div(className='sidebar-nav', children=nav_links),
        html.Div(className='sidebar-filters', children=[
            html.Label("FINANCIAL YEAR"),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': y, 'value': y} for y in YEARS],
                value='FY26',
                clearable=False,
                searchable=False
            )
        ]),
        html.Div("DATA STORY / FY23–FY26", className='sidebar-footer')
    ])


# ─── PAGE 1: THE GAP ──────────────────────────────────────────────
def build_page_gap(year):
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')
    f_eb = _safe(fk.get('EBITDA Margin %'), 0)
    b_eb = _safe(bk.get('EBITDA Margin %'), 0)
    gap = abs(f_eb - b_eb)
    
    return html.Div(className='page-wrapper', children=[
        c.methodology_badge('P1', 'Nykaa reported financials'),
        html.Div(className='editorial-statement', children=[
            "FASHION IS GROWING.",
            html.Br(),
            "BUT THE ECONOMICS ARE DIFFERENT."
        ]),
        html.Div(className='editorial-substatement', children=[
            "Nykaa hasn’t been able to match Beauty’s EBITDA margins in Fashion, despite running a similar business model, and operating in the market for eight years."
        ]),
        html.Div(className='flex-row', children=[
            html.Div([
                html.Div("FASHION EBITDA", className='giant-label'),
                html.Div(f"{f_eb:.1f}%", className='giant-number fashion')
            ]),
            html.Div([
                html.Div("BEAUTY EBITDA", className='giant-label'),
                html.Div(f"{b_eb:.1f}%", className='giant-number beauty')
            ])
        ]),
        c.annotation_box(f"That's a {gap:.1f} percentage-point gap. Where does the money go?", 'fashion'),
        
        # Mini KPI Strip
        html.Div(className='kpi-strip', children=[
            c.kpi_card('EBITDA MARGIN', f_eb, b_eb),
            c.kpi_card('CONTRIBUTION', _safe(fk.get('Contribution Margin %')), _safe(bk.get('Contribution Margin %'))),
            c.kpi_card('ORDERS / CUSTOMER', _safe(fk.get('Orders per Customer')), _safe(bk.get('Orders per Customer')), formatter=lambda x: f"{x:.2f}×" if x else '-'),
        ])
    ])

# ─── PAGE 2: WHERE THE MONEY GOES ─────────────────────────────────
def build_page_money(year):
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')
    
    return html.Div(className='page-wrapper', children=[
        c.methodology_badge('P2', 'Derived from Nykaa financials'),
        html.H1("START WITH ₹100."),
        html.P("What happens to every ₹100 of Net Sales Value (NSV)?", className='editorial-substatement'),
        
        c.create_100_rupee_flow(
            f_nsv=_safe(fk.get('NSV')), b_nsv=_safe(bk.get('NSV')),
            f_gp=_safe(fk.get('Gross Profit')), b_gp=_safe(bk.get('Gross Profit')),
            f_log=_safe(fk.get('Fulfilment Expense')), b_log=_safe(bk.get('Fulfilment Expense')),
            f_mkt=_safe(fk.get('Marketing + S&D')), b_mkt=_safe(bk.get('Marketing + S&D')),
            f_cm=_safe(fk.get('Contribution Profit')), b_cm=_safe(bk.get('Contribution Profit')),
            f_oth=_safe(fk.get('Other Expenses')), b_oth=_safe(bk.get('Other Expenses')),
            f_ebitda=_safe(fk.get('EBITDA')), b_ebitda=_safe(bk.get('EBITDA'))
        ),
        
        html.Div(className='kpi-strip', children=[
            c.kpi_card('LOGISTICS / ORDER', _safe(fk.get('Logistics Cost per Order')), _safe(bk.get('Logistics Cost per Order')), formatter=c.fmt_inr),
            c.kpi_card('MARKETING / ORDER', _safe(fk.get('Marketing + S&D per Order')), _safe(bk.get('Marketing + S&D per Order')), formatter=c.fmt_inr),
            c.kpi_card('CONTRIB / ORDER', _safe(fk.get('Contribution per Order')), _safe(bk.get('Contribution per Order')), formatter=c.fmt_inr),
        ])
    ])


# ─── PAGE 3: GROWTH ───────────────────────────────────────────────
def build_page_growth(year):
    return html.Div(className='page-wrapper', children=[
        html.H1("GROWTH VS PROFITABILITY"),
        html.P("Is Fashion converging towards Beauty's economics?", className='editorial-substatement'),
        
        html.Div(className='flex-row', children=[
            html.Div(className='flex-1', children=[
                c.chart_card(dcc.Graph(figure=c.trend_chart(YEARS, 
                    [_safe(_kpis(y, 'Fashion').get('Contribution Margin %')) for y in YEARS],
                    [_safe(_kpis(y, 'Beauty').get('Contribution Margin %')) for y in YEARS],
                    "Contribution Margin Trend", "%", annotate_gap=True
                )))
            ]),
            html.Div(className='flex-1', children=[
                c.chart_card(dcc.Graph(figure=c.trend_chart(YEARS, 
                    [_safe(_kpis(y, 'Fashion').get('Marketing + S&D %')) for y in YEARS],
                    [_safe(_kpis(y, 'Beauty').get('Marketing + S&D %')) for y in YEARS],
                    "Marketing + S&D % Trend", "%", annotate_gap=True
                )))
            ])
        ])
    ])

# ─── PAGE 4: THE CUSTOMER ─────────────────────────────────────────
def build_page_customer(df):
    if len(df) == 0: return c.empty_state("No data")
    f_ret = _safe(calculate_return_rate_survey(df, 'Fashion'), 0)
    b_ret = _safe(calculate_return_rate_survey(df, 'Beauty'), 0)
    f_rep = _safe(calculate_repeat_purchase_rate(df, 'Fashion'), 0)
    b_rep = _safe(calculate_repeat_purchase_rate(df, 'Beauty'), 0)
    f_opc = _safe(calculate_purchase_frequency(df, 'Fashion'), 0)
    b_opc = _safe(calculate_purchase_frequency(df, 'Beauty'), 0)
    f_aov = _safe(calculate_aov_proxy(df, 'Fashion'), 0)
    b_aov = _safe(calculate_aov_proxy(df, 'Beauty'), 0)

    metrics = [
        {'label': 'DISCOVER', 'fashion': 'Ads/Influencer', 'beauty': 'Organic'},
        {'label': 'PURCHASE', 'fashion': f"₹{f_aov:,.0f} AOV", 'beauty': f"₹{b_aov:,.0f} AOV"},
        {'label': 'RETURN', 'fashion': f"{f_ret:.1f}%", 'beauty': f"{b_ret:.1f}%"},
        {'label': 'REPEAT', 'fashion': f"{f_rep:.1f}%", 'beauty': f"{b_rep:.1f}%"},
        {'label': 'LOYALTY', 'fashion': f"{f_opc:.1f}x freq", 'beauty': f"{b_opc:.1f}x freq"}
    ]

    return html.Div(className='page-wrapper', children=[
        c.synthetic_data_banner(),
        html.H1("THE CUSTOMER TELLS A DIFFERENT STORY"),
        html.P("Comparing the behavioural journey of a Fashion vs Beauty shopper.", className='editorial-substatement'),
        c.create_customer_journey(metrics),
        c.annotation_box(f"Fashion has a {(f_ret-b_ret):.1f}pp higher return rate and {(b_rep-f_rep):.1f}pp lower repeat purchase rate.", 'fashion'),
        
        c.chart_card(dcc.Graph(figure=c.create_gap_plot(
            ['Return Rate', 'Repeat Purchase', 'Repurchase Intent (1-5)'],
            [f_ret, f_rep, df[df['category']=='Fashion']['repurchase_intent_3m_1_5'].mean()],
            [b_ret, b_rep, df[df['category']=='Beauty']['repurchase_intent_3m_1_5'].mean()],
            "Behavioural Gaps", formatter=c.fmt_number
        )))
    ])

# ─── APP LAYOUT ─────────────────────────────────────────────────────
app.layout = html.Div(className='app-container', children=[
    dcc.Location(id='url', refresh=False),
    make_sidebar(),
    html.Div(id='page-content', className='main-content')
])

# ─── ROUTING ────────────────────────────────────────────────────────
@callback(
    [Output(f'nav-{href.strip("/") or "home"}', 'className') for href, _, _ in NAV_ITEMS],
    Input('url', 'pathname')
)
def update_active_links(pathname):
    if pathname is None: pathname = '/'
    classes = []
    for href, _, _ in NAV_ITEMS:
        classes.append('nav-link active' if pathname == href else 'nav-link')
    return classes

@callback(
    Output('url', 'search'),
    Input('year-filter', 'value'),
    State('url', 'search'),
    prevent_initial_call=True
)
def update_url_search(year, current_search):
    return f"?year={year}" if year else ""

@callback(
    Output('year-filter', 'value'),
    Input('url', 'search'),
    State('year-filter', 'value')
)
def load_state_from_url(search, current_year):
    if not search: return dash.no_update
    qs = parse_qs(search.lstrip('?'))
    if 'year' in qs and qs['year'][0] in YEARS:
        return qs['year'][0]
    return dash.no_update

@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    Input('year-filter', 'value')
)
def route_page(pathname, year):
    if pathname == '/': return build_page_gap(year)
    elif pathname == '/where-money-goes': return build_page_money(year)
    elif pathname == '/growth': return build_page_growth(year)
    elif pathname == '/customer': return build_page_customer(df_cust)
    elif pathname == '/returns': return build_page_returns(df_cust)
    elif pathname == '/acquisition': return build_page_acquisition(year)
    elif pathname == '/scenarios': return build_page_scenarios(year)
    elif pathname == '/propositions': return build_page_propositions()
    return html.Div("PAGE NOT FOUND (Building...)", className='editorial-statement')



# ─── PAGE 5: RETURNS ──────────────────────────────────────────────
def build_page_returns(df):
    if len(df) == 0: return c.empty_state("No data")
    
    # Reason Wall logic
    f_df = df[df['category'] == 'Fashion']
    reasons = f_df['return_reason'].value_counts()
    
    rows = []
    max_val = reasons.max() if len(reasons) > 0 else 1
    for reason, count in reasons.items():
        pct = (count / len(f_df)) * 100
        bar_pct = (count / max_val) * 100
        
        rows.append(html.Div(className='reason-row', children=[
            html.Div(reason, className='reason-label'),
            html.Div(className='flex-1', children=[
                html.Div(className='reason-bar', style={'width': f'{bar_pct}%'})
            ]),
            html.Div(f"{pct:.0f}%", className='reason-val')
        ]))
        
    return html.Div(className='page-wrapper', children=[
        c.synthetic_data_banner(),
        html.H1("WHY DO ORDERS COME BACK?"),
        html.P("Fashion return rates are highly driven by fit and subjective quality.", className='editorial-substatement'),
        
        html.Div(className='chart-section', children=[
            html.H3("FASHION RETURN REASONS"),
            html.Div(children=rows, style={'marginTop': '24px'})
        ]),
        
        c.annotation_box("Unlike Beauty (where returns are mostly damage/logistics), Fashion returns are intrinsic to the discovery process. Over 40% are driven by Size/Fit.", 'fashion')
    ])


# ─── PAGE 6: ACQUISITION ──────────────────────────────────────────
def build_page_acquisition(year):
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')
    f_cac = _safe(fk.get('CAC Proxy'))
    b_cac = _safe(bk.get('CAC Proxy'))
    
    return html.Div(className='page-wrapper', children=[
        c.methodology_badge('P2', 'Derived from Nykaa financials'),
        html.H1("HOW EXPENSIVE IS THE CUSTOMER?"),
        html.P("Marketing & S&D spread across Annual Unique Transacting Customers (AUTC).", className='editorial-substatement'),
        
        html.Div(className='flex-row', children=[
            html.Div([
                html.Div("FASHION CAC PROXY", className='giant-label'),
                html.Div(f"₹{f_cac:,.0f}", className='giant-number fashion')
            ]),
            html.Div([
                html.Div("BEAUTY CAC PROXY", className='giant-label'),
                html.Div(f"₹{b_cac:,.0f}", className='giant-number beauty')
            ])
        ]),
        
        c.annotation_box("Marketing + S&D per annual unique transacting customer. This is a public-data proxy and should not be interpreted as true incremental customer acquisition cost.", 'fashion'),
        
        c.chart_card(dcc.Graph(figure=c.trend_chart(YEARS, 
            [_safe(_kpis(y, 'Fashion').get('CAC Proxy')) for y in YEARS],
            [_safe(_kpis(y, 'Beauty').get('CAC Proxy')) for y in YEARS],
            "CAC Proxy Trend (₹)", annotate_gap=True
        )))
    ])


# ─── PAGE 7: SCENARIOS ────────────────────────────────────────────
def build_page_scenarios(year):
    return html.Div(className='page-wrapper', children=[
        html.H1("WHAT WOULD IT TAKE TO CLOSE THE GAP?"),
        html.P("Adjust the levers below to see how Fashion's EBITDA margin could hit Beauty's ~10% benchmark.", className='editorial-substatement'),
        
        html.Div(className='story-container', children=[
            html.Div(className='story-text', children=[
                html.Div([
                    html.Label("IMPROVE CONTRIBUTION MARGIN (%)"),
                    dcc.Slider(id='scen-cm', min=0, max=10, step=0.5, value=0, marks={i:f"+{i}%" for i in range(0,11,2)})
                ], style={'marginBottom': '32px'}),
                
                html.Div([
                    html.Label("REDUCE MARKETING SPEND (AS % OF NSV)"),
                    dcc.Slider(id='scen-mkt', min=0, max=10, step=0.5, value=0, marks={i:f"-{i}%" for i in range(0,11,2)})
                ], style={'marginBottom': '32px'}),
                
                html.Div([
                    html.Label("REDUCE FULFILMENT SPEND (AS % OF NSV)"),
                    dcc.Slider(id='scen-ful', min=0, max=5, step=0.5, value=0, marks={i:f"-{i}%" for i in range(0,6)})
                ], style={'marginBottom': '32px'}),
                
                html.Div([
                    html.Label("INCREASE ORDERS PER CUSTOMER (%)"),
                    dcc.Slider(id='scen-ord', min=0, max=50, step=5, value=0, marks={i:f"+{i}%" for i in range(0,51,10)})
                ], style={'marginBottom': '32px'}),
                
                html.Div([
                    html.Label("INCREASE AVERAGE ORDER VALUE (%)"),
                    dcc.Slider(id='scen-aov', min=0, max=30, step=2, value=0, marks={i:f"+{i}%" for i in range(0,31,10)})
                ]),
            ]),
            html.Div(className='story-visual', id='scenario-results')
        ])
    ])

@callback(
    Output('scenario-results', 'children'),
    Input('scen-cm', 'value'),
    Input('scen-mkt', 'value'),
    Input('scen-ful', 'value'),
    Input('scen-ord', 'value'),
    Input('scen-aov', 'value'),
    Input('year-filter', 'value'),
)
def update_scenario(cm_adj, mkt_adj, ful_adj, ord_adj, aov_adj, year):
    year = year or 'FY26'
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')

    base_nsv = _safe(_get(FINANCIAL_DATA, 'Fashion', 'NSV', year), 1)
    base_orders_mn = _safe(_get(FINANCIAL_DATA, 'Fashion', 'Orders (mn)', year), 1)
    base_cm_pct = _safe(fk.get('Contribution Margin %'), 0)
    base_ebitda_pct = _safe(fk.get('EBITDA Margin %'), 0)
    b_ebitda_pct = _safe(bk.get('EBITDA Margin %'), 0)

    # Note: mkt_adj and ful_adj sliders are "reductions", so we add them to margin
    new_cm_pct = base_cm_pct + cm_adj + mkt_adj + ful_adj  
    new_ebitda_pct = base_ebitda_pct + cm_adj + mkt_adj + ful_adj

    return html.Div(children=[
        html.H3("SCENARIO RESULT"),
        html.Div(className='giant-number fashion', children=[f"{new_ebitda_pct:.1f}%"]),
        html.P(f"At these assumptions, Fashion's EBITDA margin changes from {base_ebitda_pct:.1f}% to {new_ebitda_pct:.1f}%.", className='editorial-substatement'),
        c.annotation_box(f"Beauty benchmark is {b_ebitda_pct:.1f}%.", 'beauty')
    ])


# ─── PAGE 8: PROPOSITIONS ─────────────────────────────────────────
def build_page_propositions():
    return html.Div(className='page-wrapper', children=[
        html.H1("PROPOSITIONS"),
        html.P("What the evidence suggests we investigate next.", className='editorial-substatement'),
        
        c.insight_panel([
            "PROPOSITION 1: Fashion's structural deficit lies heavily in Marketing & Logistics per order, not just Gross Margin.",
            "PROPOSITION 2: Fashion returns structurally impair Contribution Margin, driving up reverse logistics.",
            "PROPOSITION 3: To break even, Fashion must drastically lower CAC or increase Repeat Purchase frequency."
        ], "HYPOTHESES")
    ])

# ─── ROUTING UPDATE (Appending the new pages) ────────────────────────


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)
