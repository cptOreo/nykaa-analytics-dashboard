"""
app.py — Nykaa Fashion × Beauty Analytics Dashboard
Single-page, five-umbrella structure:
  1. Business Problem Statement
  2. Industry KPIs (8)
  3. Marketing Metrics (5)
  4. Analysis — Visual Representations (7 charts + scenario model)
  5. Propositions — DM/S (4)
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

from data_loader import FINANCIAL_DATA, load_customer_data, get_years
from kpi_calculations import (
    compute_all_financial_kpis, calculate_nsv_cagr, calculate_yoy_growth,
    calculate_return_rate_survey, calculate_repeat_purchase_rate,
    _is_valid,
)
from components import (
    kpi_card, trend_chart, comparison_bar, waterfall_chart, chart_card,
    proposition_card, section_anchor, COLORS, fmt_pct, fmt_inr, fmt_pts,
    get_chart_layout,
)

# ─── Load data ───────────────────────────────────────────────────────
DF_CUST = load_customer_data()
YEARS = get_years()
FY_OPTIONS = [{'label': y, 'value': y} for y in YEARS]

# ─── Helpers ─────────────────────────────────────────────────────────

def _get(data, segment, metric, year):
    try:
        v = data[segment][metric].get(year)
        if v is not None and not (isinstance(v, float) and np.isnan(v)):
            return v
    except (KeyError, TypeError):
        pass
    return None

def _kpis(year, segment):
    return compute_all_financial_kpis(FINANCIAL_DATA, year, segment)

def _trend(segment, metric):
    res = []
    for y in YEARS:
        val = compute_all_financial_kpis(FINANCIAL_DATA, y, segment).get(metric)
        res.append(_safe(val))
    return res

def _safe(val, default=None):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return default
    return val

def _fmt_ratio(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    return f"{val:.2f}×"


# ═══════════════════════════════════════════════════════════════════
#  APP INIT
# ═══════════════════════════════════════════════════════════════════

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    title="Nykaa Fashion × Beauty Analytics",
)
server = app.server

# ─── Top Navbar ──────────────────────────────────────────────────────

NAV_SECTIONS = [
    ('problem', 'Problem'),
    ('industry-kpis', 'Industry KPIs'),
    ('marketing-metrics', 'Marketing'),
    ('analysis', 'Analysis'),
    ('propositions', 'Propositions'),
]

def make_navbar():
    nav_links = []
    for section_id, label in NAV_SECTIONS:
        nav_links.append(
            html.A(label, href=f'#{section_id}', className='nav-link')
        )

    return html.Div(className='top-navbar', children=[
        html.Div(className='nav-brand', children=[
            html.Img(
                src='https://upload.wikimedia.org/wikipedia/commons/0/00/Nykaa_New_Logo.svg',
                style={'height': '22px', 'filter': 'brightness(0) invert(1)'}
            ),
            html.Span('Fashion × Beauty', className='nav-brand-text'),
        ]),
        html.Div(className='nav-divider'),
        html.Div(className='nav-links', children=nav_links),
        html.Div(className='nav-filters', children=[
            html.Label('FY'),
            dcc.Dropdown(
                id='year-filter', options=FY_OPTIONS, value='FY26',
                clearable=False, searchable=False,
                style={'width': '90px', 'fontSize': '12px'}
            ),
        ]),
    ])


# ═══════════════════════════════════════════════════════════════════
#  DASHBOARD BUILDER
# ═══════════════════════════════════════════════════════════════════

def build_dashboard(year):
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')
    df = DF_CUST

    # ─── Key values ──────────────────────────────────────────────
    f_ebitda = _safe(fk.get('EBITDA Margin %'), 0)
    b_ebitda = _safe(bk.get('EBITDA Margin %'), 0)
    gap_ebitda = f_ebitda - b_ebitda

    # ─── § 1. BUSINESS PROBLEM STATEMENT ─────────────────────────
    section_1 = html.Div([
        section_anchor('problem', 1, 'Business Problem Statement'),
        html.Div(className='problem-statement', children=[
            html.P(
                f"Nykaa's Fashion segment grew NSV from ₹573 Cr (FY22) to ₹{_safe(_get(FINANCIAL_DATA, 'Fashion', 'NSV', year), 0):,.0f} Cr ({year}), "
                f"yet posted an EBITDA margin of {fmt_pct(f_ebitda)} while Beauty achieved {fmt_pct(b_ebitda)}. "
                "The gap persists despite a similar platform business model. "
                "This analysis identifies where profitability leaks and what levers could close the gap.",
                className='problem-text'
            ),
            html.Div(className='problem-numbers', children=[
                html.Div(className='problem-stat', children=[
                    html.Div('FASHION EBITDA', className='problem-stat-label'),
                    html.Div(fmt_pct(f_ebitda), className='problem-stat-value fashion'),
                ]),
                html.Div(className='problem-stat', children=[
                    html.Div('BEAUTY EBITDA', className='problem-stat-label'),
                    html.Div(fmt_pct(b_ebitda), className='problem-stat-value beauty'),
                ]),
                html.Div(className='problem-stat', children=[
                    html.Div('MARGIN GAP', className='problem-stat-label'),
                    html.Div(fmt_pts(gap_ebitda), className='problem-stat-value gap'),
                ]),
            ]),
        ]),
    ])

    # ─── § 2. INDUSTRY KPIs (8) ──────────────────────────────────

    # NSV CAGR
    f_cagr = calculate_nsv_cagr(
        _safe(_get(FINANCIAL_DATA, 'Fashion', 'NSV', 'FY23'), 0),
        _safe(_get(FINANCIAL_DATA, 'Fashion', 'NSV', 'FY26'), 0), 3
    )
    b_cagr = calculate_nsv_cagr(
        _safe(_get(FINANCIAL_DATA, 'Beauty', 'NSV', 'FY23'), 0),
        _safe(_get(FINANCIAL_DATA, 'Beauty', 'NSV', 'FY26'), 0), 3
    )

    section_2 = html.Div([
        section_anchor('industry-kpis', 2, 'Industry KPIs',
                       f'{year} Fashion vs Beauty — all margins computed as % of NSV'),
        html.Div(className='kpi-row', children=[
            kpi_card('EBITDA MARGIN', _safe(fk.get('EBITDA Margin %')), _safe(bk.get('EBITDA Margin %')),
                     higher_is_better=True, tooltip='EBITDA ÷ Net Sales Value'),
            kpi_card('CONTRIBUTION MARGIN', _safe(fk.get('Contribution Margin %')), _safe(bk.get('Contribution Margin %')),
                     higher_is_better=True, tooltip='(GP − Fulfilment − Marketing) ÷ NSV'),
            kpi_card('REALISATION (NSV/GMV)', _safe(fk.get('Realisation %')), _safe(bk.get('Realisation %')),
                     higher_is_better=True, tooltip='Net Sales Value ÷ Gross Merchandise Value'),
            kpi_card('GROSS MARGIN', _safe(fk.get('Gross Margin %')), _safe(bk.get('Gross Margin %')),
                     higher_is_better=True, tooltip='Gross Profit ÷ NSV'),
            kpi_card('MARKETING + S&D %', _safe(fk.get('Marketing + S&D %')), _safe(bk.get('Marketing + S&D %')),
                     higher_is_better=False),
            kpi_card('FULFILMENT %', _safe(fk.get('Fulfilment %')), _safe(bk.get('Fulfilment %')),
                     higher_is_better=False),
            kpi_card('ORDERS / CUSTOMER', _safe(fk.get('Orders per Customer')), _safe(bk.get('Orders per Customer')),
                     formatter=_fmt_ratio, higher_is_better=True),
            kpi_card('NSV CAGR (FY23→26)', _safe(f_cagr), _safe(b_cagr),
                     higher_is_better=True, tooltip='3-year compound annual growth rate of NSV'),
        ]),
        html.Div(className='chart-grid chart-grid-4', children=[
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'EBITDA Margin %'), _trend('Beauty', 'EBITDA Margin %'), 'EBITDA Margin %', height=200), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'Contribution Margin %'), _trend('Beauty', 'Contribution Margin %'), 'Contribution Margin %', height=200), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'Realisation %'), _trend('Beauty', 'Realisation %'), 'Realisation (NSV/GMV) %', height=200), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'Gross Margin %'), _trend('Beauty', 'Gross Margin %'), 'Gross Margin %', height=200), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'Marketing + S&D %'), _trend('Beauty', 'Marketing + S&D %'), 'Marketing + S&D %', height=200), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'Fulfilment %'), _trend('Beauty', 'Fulfilment %'), 'Fulfilment %', height=200), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'Orders per Customer'), _trend('Beauty', 'Orders per Customer'), 'Orders per Customer', height=200, y_suffix='×'), config={'displayModeBar': False})),
        ]),
        html.Div('Source: Nykaa reported financials (P1) and derived calculations (P2). All margins use NSV as denominator.',
                 style={'fontSize': '10px', 'color': '#8E8EA0', 'marginBottom': '8px'}),
    ])

    # ─── § 3. MARKETING METRICS (5) ──────────────────────────────
    section_3 = html.Div([
        section_anchor('marketing-metrics', 3, 'Marketing Metrics',
                       f'{year} customer acquisition and unit economics'),
        html.Div(className='kpi-row', children=[
            kpi_card('CAC PROXY', _safe(fk.get('CAC Proxy')), _safe(bk.get('CAC Proxy')),
                     formatter=fmt_inr, higher_is_better=False,
                     tooltip='Marketing + S&D ÷ Annual Unique Transacting Customers'),
            kpi_card('LOGISTICS / ORDER', _safe(fk.get('Logistics Cost per Order')), _safe(bk.get('Logistics Cost per Order')),
                     formatter=fmt_inr, higher_is_better=False),
            kpi_card('CONTRIBUTION / ORDER', _safe(fk.get('Contribution per Order')), _safe(bk.get('Contribution per Order')),
                     formatter=fmt_inr, higher_is_better=True),
            kpi_card('BREAK-EVEN VOLUME',
                     _safe(fk.get('Break-even Volume'), 0) / 1e6 if _safe(fk.get('Break-even Volume')) else None,
                     _safe(bk.get('Break-even Volume'), 0) / 1e6 if _safe(bk.get('Break-even Volume')) else None,
                     formatter=lambda v: f"{v:.1f}M orders" if v else '-',
                     show_gap=False, higher_is_better=False,
                     tooltip='Other Expenses ÷ Contribution per Order'),
            kpi_card('OWNED BRAND SHARE', _safe(fk.get('Owned Brand Share %')), _safe(bk.get('Owned Brand Share %')),
                     higher_is_better=True, tooltip='Owned-brand GMV ÷ Total GMV'),
        ]),
        html.Div(className='chart-grid chart-grid-4', children=[
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'CAC Proxy'), _trend('Beauty', 'CAC Proxy'), 'CAC Proxy', height=200, y_suffix=''), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'Logistics Cost per Order'), _trend('Beauty', 'Logistics Cost per Order'), 'Logistics / Order', height=200, y_suffix=''), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'Contribution per Order'), _trend('Beauty', 'Contribution per Order'), 'Contribution / Order', height=200, y_suffix=''), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, [_safe(v)/1e6 if v else None for v in _trend('Fashion', 'Break-even Volume')], [_safe(v)/1e6 if v else None for v in _trend('Beauty', 'Break-even Volume')], 'Break-even Volume (M)', height=200, y_suffix='M'), config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=trend_chart(YEARS, _trend('Fashion', 'Owned Brand Share %'), _trend('Beauty', 'Owned Brand Share %'), 'Owned Brand Share %', height=200), config={'displayModeBar': False})),
        ]),
        html.Div('Source: Derived from Nykaa financials (P2). CAC Proxy blends acquisition and retention spend.',
                 style={'fontSize': '10px', 'color': '#8E8EA0', 'marginBottom': '8px'}),
    ])

    # ─── § 4. ANALYSIS — VISUAL REPRESENTATIONS ──────────────────

    # 4a. EBITDA Margin trend
    f_ebitda_m = [_safe(_get(FINANCIAL_DATA, 'Fashion', 'EBITDA Margin', y)) for y in YEARS]
    b_ebitda_m = [_safe(_get(FINANCIAL_DATA, 'Beauty', 'EBITDA Margin', y)) for y in YEARS]
    f_ebitda_pct = [v * 100 if v is not None else None for v in f_ebitda_m]
    b_ebitda_pct = [v * 100 if v is not None else None for v in b_ebitda_m]

    # 4b. Waterfalls (% of NSV)
    def _waterfall_pct(kpis_dict):
        gm = _safe(kpis_dict.get('Gross Margin %'), 0)
        ful = _safe(kpis_dict.get('Fulfilment %'), 0)
        mkt = _safe(kpis_dict.get('Marketing + S&D %'), 0)
        cm = _safe(kpis_dict.get('Contribution Margin %'), 0)
        oe = _safe(kpis_dict.get('Other Expenses %'), 0)
        em = _safe(kpis_dict.get('EBITDA Margin %'), 0)
        cogs_pct = 100 - gm
        labels = ['NSV', '−COGS', 'GP', '−Fulfil', '−Mkt+S&D', 'CM', '−Other', 'EBITDA']
        values = [100, -cogs_pct, gm, -ful, -mkt, cm, -oe, em]
        return labels, values

    f_labels, f_values = _waterfall_pct(fk)
    b_labels, b_values = _waterfall_pct(bk)
    
    # Unify waterfall y-axis
    max_w = max([sum([v for v in f_values if v > 0]), sum([v for v in b_values if v > 0])])
    min_w = min([sum([v for v in f_values if v < 0]), sum([v for v in b_values if v < 0])])
    w_range = [min(-20, min_w), max(110, max_w)]
    
    fig_f_w = waterfall_chart(f_labels, f_values, f'Fashion — {year} P&L (% of NSV)')
    fig_f_w.update_layout(yaxis=dict(range=w_range))
    fig_b_w = waterfall_chart(b_labels, b_values, f'Beauty — {year} P&L (% of NSV)')
    fig_b_w.update_layout(yaxis=dict(range=w_range))

    # 4c. Cost structure comparison
    margin_labels = ['Gross Margin', 'Fulfilment', 'Marketing+S&D', 'Contribution', 'EBITDA']
    margin_keys = ['Gross Margin %', 'Fulfilment %', 'Marketing + S&D %', 'Contribution Margin %', 'EBITDA Margin %']
    f_margins = [_safe(fk.get(m), 0) for m in margin_keys]
    b_margins = [_safe(bk.get(m), 0) for m in margin_keys]

    from components import dumbbell_chart

    # 4d. Growth vs Contribution Margin scatter
    import pandas as pd
    scatter_rows = []
    for y in YEARS:
        for seg in ['Fashion', 'Beauty']:
            k = compute_all_financial_kpis(FINANCIAL_DATA, y, seg)
            py_num = int(y[2:]) - 1
            py = f"FY{py_num}"
            nsv_curr = _safe(_get(FINANCIAL_DATA, seg, 'NSV', y))
            nsv_prev = _safe(_get(FINANCIAL_DATA, seg, 'NSV', py)) if py in YEARS else None
            yoy = calculate_yoy_growth(nsv_curr, nsv_prev) if nsv_curr and nsv_prev else None
            cm = _safe(k.get('Contribution Margin %'))
            if yoy is not None and cm is not None:
                scatter_rows.append({
                    'Year': y, 'Segment': seg, 'NSV Growth %': yoy,
                    'Contribution Margin %': cm, 'NSV (₹ Cr)': nsv_curr,
                })
    sdf = pd.DataFrame(scatter_rows)

    fig_scatter = go.Figure()
    if len(sdf) > 0:
        for seg, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
            sub = sdf[sdf['Segment'] == seg]
            if len(sub) > 0:
                fig_scatter.add_trace(go.Scatter(
                    x=sub['NSV Growth %'], y=sub['Contribution Margin %'],
                    name=seg, mode='markers+text',
                    marker=dict(size=sub['NSV (₹ Cr)'].apply(lambda v: max(8, min(35, v / 250))),
                                color=color, opacity=0.8),
                    text=sub['Year'], textposition='top center',
                    textfont=dict(size=9, color=COLORS['text_muted']),
                    hovertemplate='<b>%{text}</b><br>NSV Growth: %{x:.1f}%<br>CM: %{y:.1f}%<extra></extra>',
                ))
    fig_scatter.update_layout(**get_chart_layout(
        height=280,
        title=dict(text='Does faster growth improve margins?', font=dict(size=12), x=0, xanchor='left'),
        xaxis_title='NSV YoY Growth %', yaxis_title='Contribution Margin %',
    ))

    # 4e. Owned Brand Share trend
    f_owned = [_safe(compute_all_financial_kpis(FINANCIAL_DATA, y, 'Fashion').get('Owned Brand Share %')) for y in YEARS]
    b_owned = [_safe(compute_all_financial_kpis(FINANCIAL_DATA, y, 'Beauty').get('Owned Brand Share %')) for y in YEARS]

    # 4f. Return Reasons (from survey)
    fig_returns = go.Figure()
    if len(df) > 0:
        rr_fashion = df[(df['category'] == 'Fashion') & (df['return_reason'] != 'No return in last 5 orders')]['return_reason'].value_counts()
        rr_beauty = df[(df['category'] == 'Beauty') & (df['return_reason'] != 'No return in last 5 orders')]['return_reason'].value_counts()
        all_reasons = sorted(set(rr_fashion.index) | set(rr_beauty.index))
        fig_returns.add_trace(go.Bar(y=all_reasons, x=[rr_fashion.get(r, 0) for r in all_reasons],
                                     name='Fashion', marker_color=COLORS['fashion'], orientation='h'))
        fig_returns.add_trace(go.Bar(y=all_reasons, x=[rr_beauty.get(r, 0) for r in all_reasons],
                                     name='Beauty', marker_color=COLORS['beauty'], orientation='h'))
    fig_returns.update_layout(**get_chart_layout(
        height=280, barmode='group',
        title=dict(text='Return reasons (survey, n=200)', font=dict(size=12), x=0, xanchor='left'),
        margin=dict(l=180, r=20, t=40, b=30),
    ))

    section_4 = html.Div([
        section_anchor('analysis', 4, 'Analysis — Visual Representations',
                       'Charts answer specific analytical questions about the profitability gap'),

        # Row 1: Waterfalls
        html.Div(className='chart-grid', children=[
            chart_card(dcc.Graph(figure=fig_f_w, config={'displayModeBar': False}), source='P2 — Derived'),
            chart_card(dcc.Graph(figure=fig_b_w, config={'displayModeBar': False}), source='P2 — Derived'),
        ]),

        # Row 2: Cost structure + Scatter
        html.Div(className='chart-grid', children=[
            chart_card(dcc.Graph(
                figure=dumbbell_chart(margin_labels, f_margins, b_margins,
                                      f'Where does Fashion lose? ({year}, % of NSV)', y_suffix='%'),
                config={'displayModeBar': False}
            ), source='P2 — Derived'),
            chart_card(dcc.Graph(figure=fig_scatter, config={'displayModeBar': False}),
                       source='P2 — Derived'),
        ]),

        # Row 3: Owned brand trend + Return reasons
        html.Div(className='chart-grid', children=[
            chart_card(dcc.Graph(
                figure=trend_chart(YEARS, f_owned, b_owned,
                                   'Is Fashion building its owned-brand advantage?', y_suffix='%'),
                config={'displayModeBar': False}
            ), source='P2 — Derived'),
            chart_card(dcc.Graph(figure=fig_returns, config={'displayModeBar': False}),
                       source='P3 — Synthetic survey data'),
        ]),

        # Row 4: Scenario Model
        html.Div(className='scenario-panel', children=[
            html.H3('Scenario Model — What would it take for Fashion to break even?'),
            html.Div(className='scenario-layout', children=[
                html.Div(className='scenario-sliders', children=[
                    html.Div(className='slider-row', children=[
                        html.Div('Marketing + S&D reduction (pts of NSV)', className='slider-label'),
                        dcc.Slider(id='scen-mkt', min=0, max=15, step=0.5, value=0,
                                   marks={0: '0', 5: '−5', 10: '−10', 15: '−15'}),
                    ]),
                    html.Div(className='slider-row', children=[
                        html.Div('Fulfilment cost reduction (pts of NSV)', className='slider-label'),
                        dcc.Slider(id='scen-ful', min=0, max=5, step=0.5, value=0,
                                   marks={0: '0', 2: '−2', 5: '−5'}),
                    ]),
                    html.Div(className='slider-row', children=[
                        html.Div('Order volume growth (%)', className='slider-label'),
                        dcc.Slider(id='scen-ord', min=0, max=50, step=5, value=0,
                                   marks={0: '0%', 25: '+25%', 50: '+50%'}),
                    ]),
                    html.Div(className='slider-row', children=[
                        html.Div('AOV improvement (%)', className='slider-label'),
                        dcc.Slider(id='scen-aov', min=0, max=30, step=5, value=0,
                                   marks={0: '0%', 15: '+15%', 30: '+30%'}),
                    ]),
                ]),
                html.Div(id='scenario-results', className='scenario-results'),
            ]),
        ]),
    ])

    # ─── § 5. PROPOSITIONS — DM/S ────────────────────────────────

    f_mkt_pct = _safe(fk.get('Marketing + S&D %'), 0)
    b_mkt_pct = _safe(bk.get('Marketing + S&D %'), 0)
    f_opc = _safe(fk.get('Orders per Customer'), 0)
    b_opc = _safe(bk.get('Orders per Customer'), 0)
    f_real = _safe(fk.get('Realisation %'), 0)
    b_real = _safe(bk.get('Realisation %'), 0)
    f_cpo = _safe(fk.get('Contribution per Order'), 0)
    b_cpo = _safe(bk.get('Contribution per Order'), 0)

    section_5 = html.Div([
        section_anchor('propositions', 5, 'Propositions — Decision Support',
                       'Evidence-based hypotheses, not strategic recommendations'),
        html.Div(className='propositions-grid', children=[
            proposition_card(1,
                "Marketing efficiency is the primary lever. Cutting marketing intensity could improve EBITDA faster than chasing gross margin gains.",
                f"Fashion Marketing + S&D is {f_mkt_pct:.1f}% of NSV vs Beauty's {b_mkt_pct:.1f}%. "
                f"Gross margins are nearly identical ({_safe(fk.get('Gross Margin %'),0):.1f}% vs {_safe(bk.get('Gross Margin %'),0):.1f}%). "
                f"A 5-pt reduction in marketing intensity would add ~₹{_safe(fk.get('NSV'),0) * 0.05:,.0f} Cr to contribution profit.",
            ),
            proposition_card(2,
                "Repeat purchase frequency multiplies customer value. Higher frequency amortizes acquisition costs across more orders.",
                f"Beauty customers place {b_opc:.1f} orders per year vs Fashion's {f_opc:.1f}. "
                f"Contribution per customer: Beauty ₹{b_cpo * b_opc:,.0f} vs Fashion ₹{f_cpo * f_opc:,.0f}. "
                "Increasing Fashion's order frequency by 20% would reduce effective CAC per order.",
            ),
            proposition_card(3,
                "GMV-to-NSV leakage is a structural disadvantage. Fashion loses ~71% of gross value before it can be monetized.",
                f"Fashion realisation is {f_real:.1f}% vs Beauty's {b_real:.1f}%. "
                f"Fashion drops ~{100 - f_real:.0f}% of GMV to returns, discounts, and cancellations before it becomes net sales. "
                "Improving realisation by 5 pts would be equivalent to acquiring significant additional revenue.",
            ),
            proposition_card(4,
                "Owned-brand retreat weakens margin control. Fashion's private-label GMV declined while Beauty's surged.",
                f"Fashion owned-brand GMV fell from ₹{_safe(_get(FINANCIAL_DATA, 'Fashion', 'Owned Brand GMV', 'FY25'), 0):,.0f} Cr (FY25) "
                f"to ₹{_safe(_get(FINANCIAL_DATA, 'Fashion', 'Owned Brand GMV', 'FY26'), 0):,.0f} Cr (FY26), "
                f"while Beauty's surged to ₹{_safe(_get(FINANCIAL_DATA, 'Beauty', 'Owned Brand GMV', 'FY26'), 0):,.0f} Cr. "
                "Private-label products typically carry higher margins and improve platform stickiness.",
            ),
        ]),
    ])

    # ─── Footer ──────────────────────────────────────────────────
    footer = html.Div(className='dashboard-footer', children=[
        html.Div('Data Sources & Methodology', className='footer-title'),
        html.Div([
            html.P("P1 (Reported): Nykaa investor presentations and annual reports, FY22–FY26.", className='footer-text'),
            html.P("P2 (Derived): Calculated from P1 data. All margin percentages use NSV as denominator.", className='footer-text'),
            html.P("P3 (Synthetic): Customer survey data is synthetic placeholder for prototyping (n=200, 100 respondents × 2 categories). "
                   "All P3 metrics should be validated with actual primary research before use in decision-making.", className='footer-text'),
            html.P("Scenario model: Marketing and fulfilment reductions flow through to contribution margin. "
                   "Order growth and AOV improvement scale NSV proportionally. Break-even volume = Other Expenses ÷ Contribution per Order.", className='footer-text'),
        ]),
    ])

    return html.Div(className='dashboard-page', children=[
        section_1, section_2, section_3, section_4, section_5, footer
    ])


# ═══════════════════════════════════════════════════════════════════
#  APP LAYOUT
# ═══════════════════════════════════════════════════════════════════

app.layout = html.Div([
    make_navbar(),
    html.Div(id='dashboard-content'),
])


# ═══════════════════════════════════════════════════════════════════
#  CALLBACKS
# ═══════════════════════════════════════════════════════════════════

@callback(
    Output('dashboard-content', 'children'),
    Input('year-filter', 'value'),
)
def update_dashboard(year):
    year = year or 'FY26'
    return build_dashboard(year)


@callback(
    Output('scenario-results', 'children'),
    Input('scen-mkt', 'value'),
    Input('scen-ful', 'value'),
    Input('scen-ord', 'value'),
    Input('scen-aov', 'value'),
    Input('year-filter', 'value'),
)
def update_scenario(mkt_adj, ful_adj, ord_adj, aov_adj, year):
    year = year or 'FY26'
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')

    base_nsv = _safe(_get(FINANCIAL_DATA, 'Fashion', 'NSV', year), 1)
    base_orders_mn = _safe(_get(FINANCIAL_DATA, 'Fashion', 'Orders (mn)', year), 1)
    base_cm_pct = _safe(fk.get('Contribution Margin %'), 0)
    base_ebitda_pct = _safe(fk.get('EBITDA Margin %'), 0)
    base_other_exp = _safe(_get(FINANCIAL_DATA, 'Fashion', 'Other Expenses', year), 0)
    base_cpo = _safe(fk.get('Contribution per Order'), 0)

    # Adjustments: marketing and fulfilment reductions improve CM and EBITDA
    new_orders_mn = base_orders_mn * (1 + ord_adj / 100)
    aov_mult = 1 + aov_adj / 100
    new_nsv = base_nsv * (new_orders_mn / base_orders_mn) * aov_mult

    # CM improves by the sum of cost reductions
    new_cm_pct = base_cm_pct + mkt_adj + ful_adj
    new_ebitda_pct = base_ebitda_pct + mkt_adj + ful_adj

    # Update contribution per order proportionally
    new_cpo = base_cpo + (base_nsv * 10 / base_orders_mn) * (mkt_adj + ful_adj) / 100 if base_orders_mn > 0 else base_cpo
    new_cpo = new_cpo * aov_mult

    new_ebitda = new_nsv * new_ebitda_pct / 100
    new_bev = (base_other_exp * 1e7) / new_cpo if new_cpo > 0 else 0
    new_coverage = (new_orders_mn * 1e6 / new_bev * 100) if new_bev > 0 else 0

    b_ebitda_pct = _safe(bk.get('EBITDA Margin %'), 0)

    stat_style = {'display': 'flex', 'flexDirection': 'column', 'gap': '2px'}
    label_style = {'fontSize': '10px', 'fontWeight': '700', 'letterSpacing': '0.5px', 'color': '#8E8EA0', 'textTransform': 'uppercase'}
    value_style = {'fontSize': '20px', 'fontWeight': '800', 'letterSpacing': '-0.5px'}

    return html.Div([
        html.Div(style={**stat_style, 'marginBottom': '16px', 'paddingBottom': '12px', 'borderBottom': '1px solid #F0ECF2'}, children=[
            html.Div('PROJECTED EBITDA MARGIN', style=label_style),
            html.Div(f"{new_ebitda_pct:.1f}%", style={**value_style, 'fontSize': '28px',
                     'color': '#1A9E5C' if new_ebitda_pct > 0 else '#E80071'}),
            html.Div(f"vs current {base_ebitda_pct:.1f}% | Beauty benchmark {b_ebitda_pct:.1f}%",
                     style={'fontSize': '11px', 'color': '#5A5A7A'}),
        ]),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px'}, children=[
            html.Div(style=stat_style, children=[
                html.Div('Contribution Margin', style=label_style),
                html.Div(f"{new_cm_pct:.1f}%", style=value_style),
            ]),
            html.Div(style=stat_style, children=[
                html.Div('Projected EBITDA', style=label_style),
                html.Div(f"₹{new_ebitda:,.0f} Cr", style={**value_style,
                         'color': '#1A9E5C' if new_ebitda > 0 else '#D94B4B'}),
            ]),
            html.Div(style=stat_style, children=[
                html.Div('Break-even Coverage', style=label_style),
                html.Div(f"{new_coverage:.0f}%", style=value_style),
            ]),
            html.Div(style=stat_style, children=[
                html.Div('Projected Orders', style=label_style),
                html.Div(f"{new_orders_mn:.1f}M", style=value_style),
            ]),
        ]),
    ])


# ═══════════════════════════════════════════════════════════════════
#  RUN
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    app.run(debug=False, port=8050, host='0.0.0.0')
