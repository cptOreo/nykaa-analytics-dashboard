"""
Nykaa Editorial Dashboard - app.py (Final UI Polish)
"""
from dash import Dash, html, dcc, callback, Input, Output, State
import dash
import pandas as pd
import numpy as np
from urllib.parse import parse_qs

from data_loader import load_financial_data, load_customer_data, FINANCIAL_DATA, get_years
from kpi_calculations import compute_all_financial_kpis, calculate_return_rate_survey, calculate_purchase_frequency, calculate_aov_proxy, calculate_repeat_purchase_rate
import components as c
import content as txt

app = Dash(__name__, suppress_callback_exceptions=True, title="Nykaa Analytics — Data Story")

YEARS = get_years()
df_fin = load_financial_data()
try: df_cust = load_customer_data()
except Exception as e: df_cust = pd.DataFrame()

def _get(data, segment, metric, year): return data.get(segment, {}).get(metric, {}).get(year)
def _kpis(year, segment): return compute_all_financial_kpis(FINANCIAL_DATA, year, segment)
def _safe(val, default=None): return default if val is None or (isinstance(val, float) and np.isnan(val)) else val

# ─── Top Navigation ───
def make_topnav():
    nav_links = []
    for href, num, label in txt.NAV_ITEMS:
        nav_links.append(dcc.Link(label, href=href, id=f'nav-{href.strip("/") or "home"}', className='nav-link'))
    
    return html.Div(className='editorial-nav', children=[
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/0/00/Nykaa_New_Logo.svg', style={'height': '28px', 'marginRight': '60px', 'marginBottom': '4px'}),
        html.Div(className='nav-links', children=nav_links),
        html.Div(className='nav-filters', children=[
            html.Label("FY"),
            dcc.Dropdown(id='year-filter', options=[{'label': y, 'value': y} for y in YEARS], value='FY26', clearable=False, searchable=False)
        ])
    ])

# ─── 01 THE GAP ───
def build_page_gap(year):
    fk, bk = _kpis(year, 'Fashion'), _kpis(year, 'Beauty')
    f_eb, b_eb = _safe(fk.get('EBITDA Margin %'), 0), _safe(bk.get('EBITDA Margin %'), 0)
    
    return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.methodology_badge('01', txt.BADGE_FINANCIAL),
            html.Div(className='hairline-top', style={'marginTop': '20px'}, children=[
                c.kpi_card('Realisation', _safe(fk.get('Realisation %')), _safe(bk.get('Realisation %')), subtitle="GMV converted into NSV", tooltip=txt.TOOLTIPS['realisation']),
                c.kpi_card('Contribution margin', _safe(fk.get('Contribution Margin %')), _safe(bk.get('Contribution Margin %')), subtitle="₹ retained per ₹100 of NSV", tooltip=txt.TOOLTIPS['cm']),
                c.kpi_card('Orders per customer', _safe(fk.get('Orders per Customer')), _safe(bk.get('Orders per Customer')), formatter=lambda x: f"{x:.2f}×" if x else '-', subtitle="Average annual order frequency", tooltip=txt.TOOLTIPS['opc']),
            ]),
            c.annotation_box(txt.p1_dynamic_gap(f_eb, b_eb)),
        ]),
        html.Div(className='main-column', children=[
            html.Div(className='editorial-statement', children=["Fashion scales.", html.Br(), "Margins lag Beauty."]),
            html.Div(txt.p1_gap_substatement(), className='editorial-substatement'),
            html.Div(className='hairline-top flex-row', children=[
                html.Div([html.Div("FASHION EBITDA", className='giant-label'), html.Div(f"{f_eb:.1f}%", className='giant-number-secondary fashion')]),
                html.Div([html.Div("BEAUTY EBITDA", className='giant-label'), html.Div(f"{b_eb:.1f}%", className='giant-number-secondary beauty')])
            ]),
            html.P(txt.p1_gap_implication(), style={'fontSize': '16px', 'marginTop': '20px'})
        ])
    ])

# ─── 02 PROFITABILITY ───
def build_page_money(year):
    fk, bk = _kpis(year, 'Fashion'), _kpis(year, 'Beauty')
    return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.methodology_badge('02', txt.BADGE_DERIVED),
            html.Div(className='hairline-top', children=[
                c.kpi_card('Cost per order', _safe(fk.get('Logistics Cost per Order')), _safe(bk.get('Logistics Cost per Order')), formatter=c.fmt_inr, subtitle="Fulfilment cost per order", tooltip=txt.TOOLTIPS['cpo']),
                c.kpi_card('Commercial spend', _safe(fk.get('Marketing + S&D %')), _safe(bk.get('Marketing + S&D %')), subtitle="Marketing + selling costs as % of NSV", tooltip=txt.TOOLTIPS['marketing']),
                c.kpi_card('Contribution / order', _safe(fk.get('Contribution per Order')), _safe(bk.get('Contribution per Order')), formatter=c.fmt_inr, subtitle="₹ profit per order before overheads", tooltip=None),
            ]),
            c.annotation_box(txt.p2_dynamic_commercial(_safe(fk.get('Marketing + S&D %')), _safe(bk.get('Marketing + S&D %'))))
        ]),
        html.Div(className='main-column', children=[
            html.Div("The ₹100 NSV flow", className='editorial-statement'),
            html.Div("Track the capital remaining after gross profit, fulfilment, and commercial spend.", className='editorial-substatement'),
            c.create_100_rupee_flow(
                f_nsv=_safe(fk.get('NSV')), b_nsv=_safe(bk.get('NSV')), f_gp=_safe(fk.get('Gross Profit')), b_gp=_safe(bk.get('Gross Profit')),
                f_log=_safe(fk.get('Fulfilment Expense')), b_log=_safe(bk.get('Fulfilment Expense')), f_mkt=_safe(fk.get('Marketing + S&D')), b_mkt=_safe(bk.get('Marketing + S&D')),
                f_cm=_safe(fk.get('Contribution Profit')), b_cm=_safe(bk.get('Contribution Profit')), f_oth=_safe(fk.get('Other Expenses')), b_oth=_safe(bk.get('Other Expenses')),
                f_ebitda=_safe(fk.get('EBITDA')), b_ebitda=_safe(bk.get('EBITDA'))
            )
        ])
    ])

# ─── 03 GROWTH ───
def build_page_growth(year):
    fk = _kpis(year, 'Fashion')
    return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.methodology_badge('03', txt.BADGE_DERIVED),
            c.annotation_box("Marketing and selling costs scale alongside Fashion's contribution margin.")
        ]),
        html.Div(className='main-column', children=[
            html.Div("Revenue scales alongside costs", className='editorial-statement'),
            html.Div(txt.p3_dynamic_growth(year, _safe(fk.get('Contribution Margin %')), _safe(fk.get('Marketing + S&D %'))), className='editorial-substatement'),
            html.Div(className='hairline-top flex-row', children=[
                html.Div(className='flex-1', children=[
                    c.chart_card(dcc.Graph(figure=c.trend_chart(YEARS, [_safe(_kpis(y, 'Fashion').get('Contribution Margin %')) for y in YEARS], [_safe(_kpis(y, 'Beauty').get('Contribution Margin %')) for y in YEARS], "CONTRIBUTION MARGIN", "%", annotate_gap=True, yaxis_range=[-5, 45])))
                ]),
                html.Div(className='flex-1', children=[
                    c.chart_card(dcc.Graph(figure=c.trend_chart(YEARS, [_safe(_kpis(y, 'Fashion').get('Marketing + S&D %')) for y in YEARS], [_safe(_kpis(y, 'Beauty').get('Marketing + S&D %')) for y in YEARS], "COMMERCIAL SPEND", "%", annotate_gap=True, yaxis_range=[-5, 45])))
                ])
            ])
        ])
    ])

# ─── 04 CUSTOMER ───
def build_page_customer(df, year):
    if len(df) == 0: return html.Div("Data unavailable.")
    f_ret, b_ret = _safe(calculate_return_rate_survey(df, 'Fashion'), 0), _safe(calculate_return_rate_survey(df, 'Beauty'), 0)
    f_rep, b_rep = _safe(calculate_repeat_purchase_rate(df, 'Fashion'), 0), _safe(calculate_repeat_purchase_rate(df, 'Beauty'), 0)
    f_aov, b_aov = _safe(calculate_aov_proxy(df, 'Fashion'), 0), _safe(calculate_aov_proxy(df, 'Beauty'), 0)
    fk, bk = _kpis(year, 'Fashion'), _kpis(year, 'Beauty')
    f_opc, b_opc = _safe(fk.get('Orders per Customer')), _safe(bk.get('Orders per Customer'))

    metrics = [
        {'label': 'DISCOVER', 'fashion': 'Ads/Influencer', 'beauty': 'Organic'},
        {'label': 'PURCHASE', 'fashion': f"₹{f_aov:,.0f} AOV", 'beauty': f"₹{b_aov:,.0f} AOV"},
        {'label': 'RETURN', 'fashion': f"{f_ret:.1f}%", 'beauty': f"{b_ret:.1f}%"},
        {'label': 'REPEAT', 'fashion': f"{f_rep:.1f}%", 'beauty': f"{b_rep:.1f}%"}
    ]

    return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.annotation_box(txt.p4_dynamic_frequency(f_opc, b_opc)),
        ]),
        html.Div(className='main-column', children=[
            html.Div("Customer frequency alters margins", className='editorial-statement'),
            html.Div("Frequency dictates economics. Single-purchase customers carry a different financial profile than repeat buyers.", className='editorial-substatement'),
            c.create_customer_journey(metrics),
            html.Div(style={'marginTop': '20px'}, children=[
                c.chart_card(dcc.Graph(figure=c.create_gap_plot(['Return Rate', 'Repeat Purchase', 'Repurchase Intent (1-5)'], [f_ret, f_rep, df[df['category']=='Fashion']['repurchase_intent_3m_1_5'].mean()], [b_ret, b_rep, df[df['category']=='Beauty']['repurchase_intent_3m_1_5'].mean()], "BEHAVIOURAL GAPS", formatter=lambda v: f"{v:.1f}%" if v > 10 else f"{v:.2f}")))
            ])
        ])
    ])

# ─── 05 RETURNS ───
def build_page_returns(df):
    if len(df) == 0: return html.Div("Data unavailable.")
    f_df = df[df['category'] == 'Fashion']
    reasons = f_df['return_reason'].value_counts()
    
    rows = []
    if not reasons.empty:
        max_count = reasons.max()
        for i, (reason, count) in enumerate(reasons.items()):
            pct = (count/len(f_df))*100
            bar_width = (count/max_count)*100
            
            bar_html = html.Div(style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-end', 'gap': '16px'}, children=[
                html.Div(style={'width': '150px', 'height': '3px', 'backgroundColor': '#F4F4F4', 'display': 'flex'}, children=[
                    html.Div(style={'width': f"{bar_width}%", 'height': '100%', 'backgroundColor': 'var(--nykaa-pink)'})
                ]),
                html.Div(f"{pct:.0f}%", style={'width': '35px', 'textAlign': 'right', 'color': 'var(--nykaa-pink)', 'fontWeight': '900'})
            ])
            
            rows.append(html.Tr([
                html.Td(f"{i+1:02d}", style={'color': 'var(--text-light)', 'width': '40px', 'fontWeight': '700'}), 
                html.Td(reason, style={'fontWeight': '700'}), 
                html.Td(bar_html, style={'paddingRight': '0'})
            ]))
        
    return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.annotation_box("Fashion's higher return rate correlates with a wider cost burden. Size and fit drive 40% of returns.")
        ]),
        html.Div(className='main-column', children=[
            html.Div("Returns extend the order lifecycle", className='editorial-statement'),
            html.Div("Order economics continue post-checkout for the Fashion segment.", className='editorial-substatement'),
            html.Div(className='hairline-top', children=[
                html.Table(className='returns-table', style={'width': '100%'}, children=[
                    html.Tbody(rows)
                ])
            ])
        ])
    ])

# ─── 06 ACQUISITION ───
def build_page_acquisition(year):
    fk, bk = _kpis(year, 'Fashion'), _kpis(year, 'Beauty')
    f_cac, b_cac = _safe(fk.get('CAC Proxy')), _safe(bk.get('CAC Proxy'))
    
    return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.methodology_badge('06', txt.BADGE_DERIVED),
            c.annotation_box("Fashion spends more marketing capital per active customer. This proxy blends new and returning efforts.")
        ]),
        html.Div(className='main-column', children=[
            html.Div("Acquisition sets the baseline", className='editorial-statement'),
            html.Div("Customer economics rely on post-purchase behavior.", className='editorial-substatement'),
            html.Div(className='hairline-top flex-row', children=[
                html.Div([html.Div("FASHION CAC PROXY", className='giant-label'), html.Div(f"₹{f_cac:,.0f}", className='giant-number-secondary fashion')]),
                html.Div([html.Div("BEAUTY CAC PROXY", className='giant-label'), html.Div(f"₹{b_cac:,.0f}", className='giant-number-secondary beauty')])
            ]),
            html.Div(style={'marginTop': '20px'}, children=[
                c.chart_card(dcc.Graph(figure=c.trend_chart(YEARS, [_safe(_kpis(y, 'Fashion').get('CAC Proxy')) for y in YEARS], [_safe(_kpis(y, 'Beauty').get('CAC Proxy')) for y in YEARS], "CUSTOMER ACQUISITION COST PROXY", annotate_gap=True)))
            ])
        ])
    ])

# ─── 07 SCENARIOS ───
def build_page_scenarios(year):
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
    ])

@callback(
    [Output('scenario-results', 'children'), Output('scenario-annotation', 'children')],
    Input('scen-cm', 'value'), Input('scen-mkt', 'value'), Input('scen-ful', 'value'),
    Input('scen-ord', 'value'), Input('scen-aov', 'value'), Input('year-filter', 'value'),
)
def update_scenario(cm_adj, mkt_adj, ful_adj, ord_adj, aov_adj, year):
    year = year or 'FY26'
    fk, bk = _kpis(year, 'Fashion'), _kpis(year, 'Beauty')

    base_orders_mn = _safe(_get(FINANCIAL_DATA, 'Fashion', 'Orders (mn)', year), 1)
    base_cm_pct = _safe(fk.get('Contribution Margin %'), 0)
    base_ebitda_pct = _safe(fk.get('EBITDA Margin %'), 0)
    base_cpo = _safe(fk.get('Contribution per Order'), 0)
    base_other_exp = _safe(_get(FINANCIAL_DATA, 'Fashion', 'Other Expenses', year), 0)

    new_ebitda_pct = base_ebitda_pct + cm_adj + mkt_adj + ful_adj
    new_orders_mn = base_orders_mn * (1 + ord_adj / 100)
    new_cpo = base_cpo * (1 + cm_adj / base_cm_pct) if base_cm_pct > 0 else base_cpo
    new_bev = (base_other_exp * 1e7) / new_cpo if new_cpo > 0 else 0

    results = html.Div(className='hairline-top', children=[
        html.Div("MODELLED EBITDA", className='giant-label'),
        html.Div(f"{new_ebitda_pct:.1f}%", className='giant-number-secondary fashion'),
        html.Div(f"Fashion's EBITDA margin shifts from {base_ebitda_pct:.1f}% to {new_ebitda_pct:.1f}% under these assumptions.", style={'marginTop': '16px', 'fontSize': '16px'}),
    ])
    
    annotation = c.annotation_box(txt.p7_dynamic_scenario(new_cpo, new_orders_mn, new_bev))
    return results, annotation

# ─── 08 PROPOSITIONS ───
def build_page_propositions():
    props = []
    for i, p in enumerate(txt.PROPOSITIONS):
        props.append(html.Div(className='prop-card', children=[
            html.Div(f"PROPOSITION 0{i+1}", className='giant-label', style={'marginBottom': '12px'}),
            html.Div(p['observation'], style={'fontSize': '20px', 'fontWeight': '900', 'fontFamily': 'Playfair Display, serif', 'marginBottom': '20px', 'lineHeight': '1.3'}),
            html.Div("QUESTION", className='giant-label', style={'color': 'var(--nykaa-pink)'}),
            html.Div(p['question'], style={'fontSize': '14px', 'marginBottom': '20px'}),
            html.Div("DIRECTION", className='giant-label'),
            html.Div(p['direction'], style={'fontSize': '14px'})
        ]))
        
    return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.methodology_badge('08', "STRATEGY, Executive Summary")
        ]),
        html.Div(className='main-column', children=[
            html.Div("Strategic propositions", className='editorial-statement'),
            html.Div("Evidence-led areas for investigation.", className='editorial-substatement'),
            html.Div(className='prop-grid hairline-top', children=props)
        ])
    ])

# ─── APP LAYOUT ───
app.layout = html.Div(className='app-container', children=[dcc.Location(id='url', refresh=False), make_topnav(), html.Div(id='page-content')])

# ─── ROUTING ───
@callback([Output(f'nav-{href.strip("/") or "home"}', 'className') for href, _, _ in txt.NAV_ITEMS], Input('url', 'pathname'))
def update_active_links(pathname): return ['nav-link active' if (pathname or '/') == href else 'nav-link' for href, _, _ in txt.NAV_ITEMS]

@callback(Output('url', 'search'), Input('year-filter', 'value'), State('url', 'search'), prevent_initial_call=True)
def update_url_search(year, current_search): return f"?year={year}" if year else ""

@callback(Output('year-filter', 'value'), Input('url', 'search'), State('year-filter', 'value'))
def load_state_from_url(search, current_year):
    if not search: return dash.no_update
    qs = parse_qs(search.lstrip('?'))
    return qs['year'][0] if 'year' in qs and qs['year'][0] in YEARS else dash.no_update

@callback(Output('page-content', 'children'), Input('url', 'pathname'), Input('year-filter', 'value'))
def route_page(pathname, year):
    if pathname == '/': return build_page_gap(year)
    elif pathname == '/where-money-goes': return build_page_money(year)
    elif pathname == '/growth': return build_page_growth(year)
    elif pathname == '/customer': return build_page_customer(df_cust, year)
    elif pathname == '/returns': return build_page_returns(df_cust)
    elif pathname == '/acquisition': return build_page_acquisition(year)
    elif pathname == '/scenarios': return build_page_scenarios(year)
    elif pathname == '/propositions': return build_page_propositions()
    return html.Div("PAGE NOT FOUND", className='editorial-statement')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=False)
