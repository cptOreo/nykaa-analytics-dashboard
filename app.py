"""
app.py - Nykaa Fashion × Beauty Analytics Dashboard
A multi-page Dash application analysing the Fashion vs Beauty profitability gap.
"""

import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from data_loader import FINANCIAL_DATA, load_customer_data, get_years
from kpi_calculations import (
    compute_all_financial_kpis, calculate_realisation, calculate_gross_margin,
    calculate_fulfilment_pct, calculate_marketing_sd_pct, calculate_contribution_margin,
    calculate_ebitda_margin, calculate_logistics_cost_per_order,
    calculate_orders_per_customer, calculate_breakeven_volume,
    calculate_contribution_per_order, calculate_cac_proxy, calculate_nsv_per_order,
    calculate_marketing_sd_per_order, calculate_nsv_cagr, calculate_yoy_growth,
    calculate_owned_brand_share, calculate_return_rate_survey,
    calculate_repeat_purchase_rate, calculate_aov_proxy,
    calculate_share_of_wallet, calculate_repurchase_intent,
    calculate_other_expenses_pct,
)
from components import (
    kpi_card, trend_chart, comparison_bar, waterfall_chart, distribution_chart,
    horizontal_bar_single, scatter_plot, page_header, section_header,
    insight_panel, methodology_badge, synthetic_data_banner, chart_card,
    empty_state, proposition_card, COLORS, fmt_pct, fmt_inr, fmt_cr,
    fmt_number, fmt_pts, get_chart_layout,
)

# ─── Load data ───────────────────────────────────────────────────────
DF_CUST = load_customer_data()
YEARS = get_years()
FY_OPTIONS = [{'label': y, 'value': y} for y in YEARS]

# ─── Helpers ─────────────────────────────────────────────────────────

def _get(data, segment, metric, year):
    """Safely get a value from FINANCIAL_DATA."""
    try:
        v = data[segment][metric].get(year)
        if v is not None and not (isinstance(v, float) and np.isnan(v)):
            return v
    except (KeyError, TypeError):
        pass
    return None

def _kpis(year, segment):
    return compute_all_financial_kpis(FINANCIAL_DATA, year, segment)

def _prev_year(year):
    try:
        num = int(year[2:])
        p = f"FY{num - 1}"
        return p if p in YEARS else None
    except:
        return None

def _safe(val, default=None):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return default
    return val

def _gap(f, b):
    f2, b2 = _safe(f), _safe(b)
    if f2 is not None and b2 is not None:
        return f2 - b2
    return None

def _fmt_ratio(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    return f"{val:.2f}×"

def _fmt_score(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    return f"{val:.1f} / 5"


# ═══════════════════════════════════════════════════════════════════
#  APP INIT
# ═══════════════════════════════════════════════════════════════════

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    title="Nykaa Fashion × Beauty Analytics",
)
server = app.server

# ─── Sidebar ─────────────────────────────────────────────────────────

NAV_ITEMS = [
    ('/', '📊', 'Executive Overview'),
    ('/margin-gap', '📉', 'Margin Gap Analysis'),
    ('/growth', '📈', 'Growth vs Profitability'),
    ('/customers', '👥', 'Customer Economics'),
    ('/acquisition', '🎯', 'Acquisition & Marketing'),
    ('/returns', '🔄', 'Returns & Friction'),
    ('/platforms', '📱', 'Platform & Competitive'),
    ('/breakeven', '⚖️', 'Break-even & Scenarios'),
]

def make_sidebar():
    nav_links = []
    for href, icon, label in NAV_ITEMS:
        nav_links.append(
            dcc.Link(
                [html.Span(icon, className='nav-icon'), label],
                href=href, className='nav-link', id=f'nav-{href.strip("/") or "home"}'
            )
        )

    return html.Div(className='sidebar', children=[
        # Brand
        html.Div(className='sidebar-brand', children=[
            html.H2('NYKAA'),
            html.P('Fashion × Beauty Analytics'),
        ]),
        html.Div(className='sidebar-edge'),

        # Nav
        html.Div(className='sidebar-nav', children=[
            html.Div('ANALYSIS', className='nav-section-label'),
            *nav_links,
        ]),

        # Year filter
        html.Div(className='sidebar-filters', children=[
            html.Label('FINANCIAL YEAR'),
            dcc.Dropdown(
                id='year-filter', options=FY_OPTIONS, value='FY26',
                clearable=False, style={'fontSize': '12px'}
            ),
        ]),

        # Source note
        html.Div(className='sidebar-source-badge', children=[
            html.P('P1/P2 - Nykaa reported or derived'),
            html.P('P3 - Synthetic placeholder for prototyping'),
        ]),
    ])


# ─── App Layout ──────────────────────────────────────────────────────

app.layout = html.Div(className='dashboard-container', children=[
    dcc.Location(id='url', refresh=False),
    make_sidebar(),
    html.Div(id='page-content', className='main-content'),
])


# ═══════════════════════════════════════════════════════════════════
#  PAGE BUILDERS
# ═══════════════════════════════════════════════════════════════════

# ──────────────────── PAGE 1: Executive Overview ─────────────────────

def build_page1(year):
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')
    py = _prev_year(year)
    fk_p = _kpis(py, 'Fashion') if py else {}
    bk_p = _kpis(py, 'Beauty') if py else {}

    def _gap_prev(metric):
        fp = _safe(fk_p.get(metric))
        bp = _safe(bk_p.get(metric))
        if fp is not None and bp is not None:
            return fp - bp
        return None

    hero_kpis = html.Div(className='kpi-row', children=[
        kpi_card('EBITDA MARGIN', _safe(fk.get('EBITDA Margin %')), _safe(bk.get('EBITDA Margin %')),
                 prev_gap=_gap_prev('EBITDA Margin %'), higher_is_better=True, tooltip='EBITDA ÷ Net Sales Value (NSV)'),
        kpi_card('CONTRIBUTION MARGIN', _safe(fk.get('Contribution Margin %')), _safe(bk.get('Contribution Margin %')),
                 prev_gap=_gap_prev('Contribution Margin %'), higher_is_better=True, tooltip='Gross Profit minus Fulfilment and Marketing, divided by NSV'),
        kpi_card('MARKETING + S&D %', _safe(fk.get('Marketing + S&D %')), _safe(bk.get('Marketing + S&D %')),
                 prev_gap=_gap_prev('Marketing + S&D %'), higher_is_better=False),
        kpi_card('NSV ÷ GMV (REALISATION)', _safe(fk.get('Realisation %')), _safe(bk.get('Realisation %')),
                 prev_gap=_gap_prev('Realisation %'), higher_is_better=True, tooltip='Net Sales Value ÷ Gross Merchandise Value. Measures value lost to cancellations, returns, and discounts.'),
        kpi_card('LOGISTICS / ORDER', _safe(fk.get('Logistics Cost per Order')), _safe(bk.get('Logistics Cost per Order')),
                 formatter=fmt_inr, prev_gap=_gap_prev('Logistics Cost per Order'), higher_is_better=False, tooltip='Fulfilment Expense ÷ Total Orders'),
        kpi_card('ORDERS / CUSTOMER', _safe(fk.get('Orders per Customer')), _safe(bk.get('Orders per Customer')),
                 formatter=_fmt_ratio, prev_gap=_gap_prev('Orders per Customer'), higher_is_better=True),
        kpi_card('BREAK-EVEN VOLUME', _safe(fk.get('Break-even Volume'), 0) / 1e6 if _safe(fk.get('Break-even Volume')) else None,
                 _safe(bk.get('Break-even Volume'), 0) / 1e6 if _safe(bk.get('Break-even Volume')) else None,
                 formatter=lambda v: f"{v:.1f}M orders" if v else '-',
                 show_gap=False, higher_is_better=False),
    ])

    # Build trend data
    def _series(metric_key, seg, multiply=1):
        return [_safe(compute_all_financial_kpis(FINANCIAL_DATA, y, seg).get(metric_key), None)
                for y in YEARS]

    def _series_m(metric_key, seg):
        """Series multiplied by nothing (already in %)"""
        return _series(metric_key, seg)

    # EBITDA margin from reported data
    f_ebitda_m = [_safe(_get(FINANCIAL_DATA, 'Fashion', 'EBITDA Margin', y))
                  for y in YEARS]
    b_ebitda_m = [_safe(_get(FINANCIAL_DATA, 'Beauty', 'EBITDA Margin', y))
                  for y in YEARS]
    f_ebitda_pct = [v * 100 if v is not None else None for v in f_ebitda_m]
    b_ebitda_pct = [v * 100 if v is not None else None for v in b_ebitda_m]

    charts = html.Div(className='chart-grid chart-grid-3', children=[
        chart_card(dcc.Graph(
            figure=trend_chart(YEARS, f_ebitda_pct, b_ebitda_pct,
                               'EBITDA Margin % (Reported)', y_suffix='%'),
            config={'displayModeBar': False}
        ), source='P1 - Nykaa reported'),

        chart_card(dcc.Graph(
            figure=trend_chart(YEARS,
                               _series('Contribution Margin %', 'Fashion'),
                               _series('Contribution Margin %', 'Beauty'),
                               'Contribution Margin %', y_suffix='%'),
            config={'displayModeBar': False}
        ), source='P2 - Derived'),

        chart_card(dcc.Graph(
            figure=trend_chart(YEARS,
                               _series('Marketing + S&D %', 'Fashion'),
                               _series('Marketing + S&D %', 'Beauty'),
                               'Marketing + S&D % of NSV', y_suffix='%'),
            config={'displayModeBar': False}
        ), source='P2 - Derived'),

        chart_card(dcc.Graph(
            figure=trend_chart(YEARS,
                               _series('Realisation %', 'Fashion'),
                               _series('Realisation %', 'Beauty'),
                               'NSV / GMV Realisation %', y_suffix='%'),
            config={'displayModeBar': False}
        ), source='P2 - Derived'),

        chart_card(dcc.Graph(
            figure=trend_chart(YEARS,
                               _series('Logistics Cost per Order', 'Fashion'),
                               _series('Logistics Cost per Order', 'Beauty'),
                               'Logistics Cost per Order (₹)', y_suffix=''),
            config={'displayModeBar': False}
        ), source='P2 - Derived'),

        chart_card(dcc.Graph(
            figure=trend_chart(YEARS,
                               _series('Orders per Customer', 'Fashion'),
                               _series('Orders per Customer', 'Beauty'),
                               'Orders per Customer', y_suffix='×'),
            config={'displayModeBar': False}
        ), source='P2 - Derived'),
    ])

    # Dynamic insights
    f_ebitda_val = _safe(fk.get('EBITDA Margin %'), 0)
    b_ebitda_val = _safe(bk.get('EBITDA Margin %'), 0)
    f_cm = _safe(fk.get('Contribution Margin %'), 0)
    b_cm = _safe(bk.get('Contribution Margin %'), 0)
    f_mkt = _safe(fk.get('Marketing + S&D %'), 0)
    b_mkt = _safe(bk.get('Marketing + S&D %'), 0)
    f_log = _safe(fk.get('Logistics Cost per Order'), 0)
    b_log = _safe(bk.get('Logistics Cost per Order'), 0)
    f_opc = _safe(fk.get('Orders per Customer'), 0)
    b_opc = _safe(bk.get('Orders per Customer'), 0)

    insights = [
        f"Fashion's {year} EBITDA margin is {fmt_pct(f_ebitda_val)} vs Beauty's {fmt_pct(b_ebitda_val)}. That is a gap of {fmt_pts(f_ebitda_val - b_ebitda_val)}.",
        f"Fashion's contribution margin ({fmt_pct(f_cm)}) trails Beauty ({fmt_pct(b_cm)}) by {abs(f_cm - b_cm):.1f} pts.",
        f"Fashion's Marketing + S&D burden is {fmt_pct(f_mkt)} of NSV versus {fmt_pct(b_mkt)} for Beauty, which is {abs(f_mkt - b_mkt):.1f} pts higher.",
        f"Fashion's logistics cost per order is ₹{f_log:.0f} vs ₹{b_log:.0f} for Beauty.",
        f"Fashion customers average {f_opc:.2f} orders/customer vs {b_opc:.2f} for Beauty.",
    ]

    return html.Div([
        page_header(
            'Understanding the Profitability Gap',
            'Why does Fashion make less money than Beauty?',
            'NYKAA FASHION × BEAUTY',
        ),
        html.Div(className='page-body', children=[
            insight_panel(
                'THE BUSINESS PROBLEM',
                "Nykaa has not matched Beauty's EBITDA margins in Fashion, despite Fashion being in the market for ~8 years and operating with a broadly similar platform model."
            ),
            html.Div(className='nykaa-edge-line', style={'marginTop': '24px'}),
            methodology_badge('P1/P2', 'Nykaa reported or derived'),
            hero_kpis,
            charts,
            insight_panel(insights),
        ]),
    ])


# ──────────────────── PAGE 2: Margin Gap ─────────────────────────────

def build_page2(year):
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')

    f_nsv = _safe(_get(FINANCIAL_DATA, 'Fashion', 'NSV', year), 0)
    b_nsv = _safe(_get(FINANCIAL_DATA, 'Beauty', 'NSV', year), 0)

    def _waterfall_pct(seg, kpis_dict, nsv_val):
        """Build waterfall values as % of NSV."""
        gm = _safe(kpis_dict.get('Gross Margin %'), 0)
        ful = _safe(kpis_dict.get('Fulfilment %'), 0)
        mkt = _safe(kpis_dict.get('Marketing + S&D %'), 0)
        cm = _safe(kpis_dict.get('Contribution Margin %'), 0)
        oe = _safe(kpis_dict.get('Other Expenses %'), 0)
        em = _safe(kpis_dict.get('EBITDA Margin %'), 0)
        cogs_pct = 100 - gm

        labels = ['NSV', '−COGS', 'Gross Profit', '−Fulfilment', '−Marketing+S&D',
                  'Contribution', '−Other Exp', 'EBITDA']
        values = [100, -cogs_pct, gm, -ful, -mkt, cm, -oe, em]
        return labels, values

    f_labels, f_values = _waterfall_pct('Fashion', fk, f_nsv)
    b_labels, b_values = _waterfall_pct('Beauty', bk, b_nsv)

    # Per-order metrics comparison
    metrics_labels = ['Marketing+S&D / Order', 'Logistics / Order', 'Contribution / Order', 'CAC Proxy']
    f_per_order = [
        _safe(fk.get('Marketing + S&D per Order'), 0),
        _safe(fk.get('Logistics Cost per Order'), 0),
        _safe(fk.get('Contribution per Order'), 0),
        _safe(fk.get('CAC Proxy'), 0),
    ]
    b_per_order = [
        _safe(bk.get('Marketing + S&D per Order'), 0),
        _safe(bk.get('Logistics Cost per Order'), 0),
        _safe(bk.get('Contribution per Order'), 0),
        _safe(bk.get('CAC Proxy'), 0),
    ]

    # Margin comparison table
    margin_labels = ['Gross Margin %', 'Fulfilment %', 'Marketing + S&D %',
                     'Contribution Margin %', 'Other Expenses %', 'EBITDA Margin %']
    f_margins = [_safe(fk.get(m), 0) for m in margin_labels]
    b_margins = [_safe(bk.get(m), 0) for m in margin_labels]
    gaps = [f - b for f, b in zip(f_margins, b_margins)]

    # Build margin comparison bar chart
    fig_margin = go.Figure()
    fig_margin.add_trace(go.Bar(
        x=margin_labels, y=f_margins, name='Fashion',
        marker_color=COLORS['fashion'],
        text=[f"{v:.1f}%" for v in f_margins], textposition='outside',
        textfont=dict(size=10), hovertemplate='Fashion: %{y:.1f}%<extra></extra>',
    ))
    fig_margin.add_trace(go.Bar(
        x=margin_labels, y=b_margins, name='Beauty',
        marker_color=COLORS['beauty'],
        text=[f"{v:.1f}%" for v in b_margins], textposition='outside',
        textfont=dict(size=10), hovertemplate='Beauty: %{y:.1f}%<extra></extra>',
    ))
    fig_margin.update_layout(**get_chart_layout(
        height=320, barmode='group', bargap=0.25,
        title=dict(text=f'{year} Cost Structure (% of NSV)', font=dict(size=13), x=0, xanchor='left'),
    ))

    insights = [
        f"Gross margins are comparable: Fashion {f_margins[0]:.1f}% vs Beauty {b_margins[0]:.1f}%.",
        f"Marketing + S&D is the widest gap at {abs(gaps[2]):.1f} pts - Fashion {f_margins[2]:.1f}% vs Beauty {b_margins[2]:.1f}%).",
        f"Fashion spends ₹{_safe(fk.get('Marketing + S&D per Order'),0):.0f}/order on marketing vs ₹{_safe(bk.get('Marketing + S&D per Order'),0):.0f} for Beauty.",
        f"CAC proxy: Fashion ₹{_safe(fk.get('CAC Proxy'),0):.0f} vs Beauty ₹{_safe(bk.get('CAC Proxy'),0):.0f}.",
    ]

    return html.Div([
        page_header(
            'Fashion holds its own on gross margin. The real gap opens up later.',
            f'{year} profitability decomposition: where the economics are consumed.',
            'WHERE THE MARGIN GAP COMES FROM',
        ),
        html.Div(className='page-body', children=[
            html.Div(className='nykaa-edge-line'),
            methodology_badge('P1/P2', 'Nykaa reported or derived'),

            # Waterfall charts side by side
            html.Div(className='chart-grid', children=[
                chart_card(dcc.Graph(
                    figure=waterfall_chart(f_labels, f_values, f'Fashion - {year} (% of NSV)'),
                    config={'displayModeBar': False}
                ), source='P2 - Derived from Nykaa data'),
                chart_card(dcc.Graph(
                    figure=waterfall_chart(b_labels, b_values, f'Beauty - {year} (% of NSV)'),
                    config={'displayModeBar': False}
                ), source='P2 - Derived from Nykaa data'),
            ]),

            # Margin comparison
            chart_card(dcc.Graph(figure=fig_margin, config={'displayModeBar': False}),
                       source='P2 - Derived', full_width=True),

            # Per-order metrics
            html.Div(className='chart-grid', children=[
                chart_card(dcc.Graph(
                    figure=comparison_bar(metrics_labels, f_per_order, b_per_order,
                                          f'Per-Order Economics - {year} (₹)', y_suffix=' ₹'),
                    config={'displayModeBar': False}
                ), source='P2 - Derived', full_width=True),
            ]),

            insight_panel(insights),
        ]),
    ])


# ──────────────────── PAGE 3: Growth vs Profitability ────────────────

def build_page3(year):
    f_gmv = [_safe(_get(FINANCIAL_DATA, 'Fashion', 'GMV', y), None) for y in YEARS]
    b_gmv = [_safe(_get(FINANCIAL_DATA, 'Beauty', 'GMV', y), None) for y in YEARS]
    f_nsv = [_safe(_get(FINANCIAL_DATA, 'Fashion', 'NSV', y), None) for y in YEARS]
    b_nsv = [_safe(_get(FINANCIAL_DATA, 'Beauty', 'NSV', y), None) for y in YEARS]
    f_rev = [_safe(_get(FINANCIAL_DATA, 'Fashion', 'Revenue from Operations', y), None) for y in YEARS]
    b_rev = [_safe(_get(FINANCIAL_DATA, 'Beauty', 'Revenue from Operations', y), None) for y in YEARS]

    # NSV CAGR (FY23 → FY26)
    f_cagr = calculate_nsv_cagr(
        _safe(_get(FINANCIAL_DATA, 'Fashion', 'NSV', 'FY23'), 0),
        _safe(_get(FINANCIAL_DATA, 'Fashion', 'NSV', 'FY26'), 0), 3
    )
    b_cagr = calculate_nsv_cagr(
        _safe(_get(FINANCIAL_DATA, 'Beauty', 'NSV', 'FY23'), 0),
        _safe(_get(FINANCIAL_DATA, 'Beauty', 'NSV', 'FY26'), 0), 3
    )

    fig_cagr = go.Figure()
    fig_cagr.add_trace(go.Bar(
        x=['Fashion', 'Beauty'], y=[_safe(f_cagr, 0), _safe(b_cagr, 0)],
        marker_color=[COLORS['fashion'], COLORS['beauty']],
        text=[f"{_safe(f_cagr,0):.1f}%", f"{_safe(b_cagr,0):.1f}%"],
        textposition='outside', textfont=dict(size=12, color=COLORS['text_primary']),
        hovertemplate='%{x}: %{y:.1f}%<extra></extra>',
    ))
    fig_cagr.update_layout(**get_chart_layout(
        height=280, showlegend=False,
        title=dict(text='NSV CAGR FY23→FY26', font=dict(size=13), x=0, xanchor='left'),
    ))

    # Scatter: growth vs contribution margin
    scatter_rows = []
    for y in YEARS:
        for seg in ['Fashion', 'Beauty']:
            k = compute_all_financial_kpis(FINANCIAL_DATA, y, seg)
            py = _prev_year(y)
            nsv_curr = _safe(_get(FINANCIAL_DATA, seg, 'NSV', y))
            nsv_prev = _safe(_get(FINANCIAL_DATA, seg, 'NSV', py)) if py else None
            yoy = calculate_yoy_growth(nsv_curr, nsv_prev) if nsv_curr and nsv_prev else None
            cm = _safe(k.get('Contribution Margin %'))
            em = _safe(k.get('EBITDA Margin %'))
            if yoy is not None and cm is not None:
                scatter_rows.append({
                    'Year': y, 'Segment': seg, 'NSV Growth %': yoy,
                    'Contribution Margin %': cm, 'NSV (₹ Cr)': nsv_curr,
                    'EBITDA Margin %': _safe(em, 0),
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
                    marker=dict(size=sub['NSV (₹ Cr)'].apply(lambda v: max(8, min(40, v / 200))),
                                color=color, opacity=0.8),
                    text=sub['Year'], textposition='top center',
                    textfont=dict(size=9, color=COLORS['text_muted']),
                    customdata=sub[['Year', 'NSV (₹ Cr)', 'EBITDA Margin %']].values,
                    hovertemplate='<b>%{text}</b><br>NSV Growth: %{x:.1f}%<br>Contribution Margin: %{y:.1f}%<br>NSV: ₹%{customdata[1]:.0f} Cr<br>EBITDA Margin: %{customdata[2]:.1f}%<extra></extra>',
                ))
    fig_scatter.update_layout(**get_chart_layout(
        height=360,
        title=dict(text='Growth vs Contribution Margin', font=dict(size=13), x=0, xanchor='left'),
        xaxis_title='NSV YoY Growth %', yaxis_title='Contribution Margin %',
    ))

    insights = [
        f"Fashion NSV CAGR (FY23→FY26): {_safe(f_cagr,0):.1f}% vs Beauty {_safe(b_cagr,0):.1f}%.",
        f"Fashion GMV grew from ₹{_safe(f_gmv[0],0):,.0f} Cr (FY22) to ₹{_safe(f_gmv[-1],0):,.0f} Cr (FY26).",
        "Growth doesn't automatically mean profits. The scatter plot shows Fashion growing fast but with lower contribution margin.",
    ]

    return html.Div([
        page_header('Growth alone does not explain the gap.',
                     'How growth impacts the bottom line.',
                     'GROWTH VS PROFITABILITY'),
        html.Div(className='page-body', children=[
            html.Div(className='nykaa-edge-line'),
            methodology_badge('P1/P2', 'Nykaa reported or derived'),

            html.Div(className='chart-grid chart-grid-3', children=[
                chart_card(dcc.Graph(
                    figure=trend_chart(YEARS, f_gmv, b_gmv, 'GMV Trend (₹ Cr)', y_suffix=' Cr'),
                    config={'displayModeBar': False}), source='P1 - Reported'),
                chart_card(dcc.Graph(
                    figure=trend_chart(YEARS, f_nsv, b_nsv, 'NSV Trend (₹ Cr)', y_suffix=' Cr'),
                    config={'displayModeBar': False}), source='P1 - Reported'),
                chart_card(dcc.Graph(
                    figure=trend_chart(YEARS, f_rev, b_rev, 'Revenue from Operations (₹ Cr)', y_suffix=' Cr'),
                    config={'displayModeBar': False}), source='P1 - Reported'),
            ]),

            html.Div(className='chart-grid', children=[
                chart_card(dcc.Graph(figure=fig_cagr, config={'displayModeBar': False}),
                           source='P2 - Derived'),
                chart_card(dcc.Graph(figure=fig_scatter, config={'displayModeBar': False}),
                           source='P2 - Derived'),
            ]),

            insight_panel(insights),
        ]),
    ])


# ──────────────────── PAGE 4: Customer Economics ─────────────────────

def build_page4(df):
    if len(df) == 0:
        return html.Div([
            page_header('Are Fashion customers behaving differently?', '', 'CUSTOMER ECONOMICS'),
            html.Div(className='page-body', children=[empty_state()]),
        ])

    f_ret = _safe(calculate_return_rate_survey(df, 'Fashion'), 0)
    b_ret = _safe(calculate_return_rate_survey(df, 'Beauty'), 0)
    f_rep = _safe(calculate_repeat_purchase_rate(df, 'Fashion'), 0)
    b_rep = _safe(calculate_repeat_purchase_rate(df, 'Beauty'), 0)
    f_aov = _safe(calculate_aov_proxy(df, 'Fashion'), 0)
    b_aov = _safe(calculate_aov_proxy(df, 'Beauty'), 0)
    f_intent = _safe(calculate_repurchase_intent(df, 'Fashion'), 0)
    b_intent = _safe(calculate_repurchase_intent(df, 'Beauty'), 0)
    f_sow = _safe(calculate_share_of_wallet(df, 'Fashion'), 0)
    b_sow = _safe(calculate_share_of_wallet(df, 'Beauty'), 0)

    kpis = html.Div(className='kpi-row', children=[
        kpi_card('RETURN RATE', f_ret, b_ret, higher_is_better=False),
        kpi_card('REPEAT PURCHASE RATE', f_rep, b_rep, higher_is_better=True),
        kpi_card('AOV (SURVEY PROXY)', f_aov, b_aov, formatter=fmt_inr, higher_is_better=True),
        kpi_card('REPURCHASE INTENT', f_intent, b_intent, formatter=_fmt_score, higher_is_better=True),
    ])

    # AOV distribution
    fig_aov = distribution_chart(df, 'aov_mid_inr', title='AOV Distribution (₹)')

    # Return rate comparison
    fig_return = go.Figure()
    fig_return.add_trace(go.Bar(x=['Fashion', 'Beauty'], y=[f_ret, b_ret],
                                marker_color=[COLORS['fashion'], COLORS['beauty']],
                                text=[f"{f_ret:.1f}%", f"{b_ret:.1f}%"], textposition='outside',
                                textfont=dict(size=12)))
    fig_return.update_layout(**get_chart_layout(height=280, showlegend=False,
        title=dict(text='Return Rate (% of last 5 orders)', font=dict(size=13), x=0, xanchor='left')))

    # Return reasons
    rr_fashion = df[(df['category'] == 'Fashion') & (df['return_reason'] != 'No return in last 5 orders')]['return_reason'].value_counts()
    rr_beauty = df[(df['category'] == 'Beauty') & (df['return_reason'] != 'No return in last 5 orders')]['return_reason'].value_counts()
    all_reasons = sorted(set(rr_fashion.index) | set(rr_beauty.index))
    fig_reasons = go.Figure()
    fig_reasons.add_trace(go.Bar(y=all_reasons, x=[rr_fashion.get(r, 0) for r in all_reasons],
                                  name='Fashion', marker_color=COLORS['fashion'], orientation='h'))
    fig_reasons.add_trace(go.Bar(y=all_reasons, x=[rr_beauty.get(r, 0) for r in all_reasons],
                                  name='Beauty', marker_color=COLORS['beauty'], orientation='h'))
    fig_reasons.update_layout(**get_chart_layout(height=340, barmode='group',
        title=dict(text='Return Reason Distribution', font=dict(size=13), x=0, xanchor='left'),
        margin=dict(l=200, r=20, t=40, b=30)))

    # Repurchase intent
    fig_intent = go.Figure()
    fig_intent.add_trace(go.Bar(x=['Fashion', 'Beauty'], y=[f_intent, b_intent],
                                 marker_color=[COLORS['fashion'], COLORS['beauty']],
                                 text=[f"{f_intent:.1f}", f"{b_intent:.1f}"], textposition='outside'))
    fig_intent.update_layout(**get_chart_layout(height=280, showlegend=False,
        title=dict(text='Repurchase Intent (1–5 scale)', font=dict(size=13), x=0, xanchor='left')))

    # Share of wallet
    fig_sow = go.Figure()
    fig_sow.add_trace(go.Bar(x=['Fashion', 'Beauty'], y=[f_sow, b_sow],
                              marker_color=[COLORS['fashion'], COLORS['beauty']],
                              text=[f"{f_sow:.1f}%", f"{b_sow:.1f}%"], textposition='outside'))
    fig_sow.update_layout(**get_chart_layout(height=280, showlegend=False,
        title=dict(text='Share of Wallet / Requirements (%)', font=dict(size=13), x=0, xanchor='left')))

    insights = [
        f"Fashion return rate ({f_ret:.1f}%) is {'higher' if f_ret > b_ret else 'lower'} than Beauty ({b_ret:.1f}%).",
        f"Fashion repeat purchase rate ({f_rep:.1f}%) {'trails' if f_rep < b_rep else 'leads'} Beauty ({b_rep:.1f}%).",
        f"Fashion AOV proxy (₹{f_aov:,.0f}) is {'higher' if f_aov > b_aov else 'lower'} than Beauty (₹{b_aov:,.0f}).",
        f"Fashion's share of wallet ({f_sow:.1f}%) vs Beauty ({b_sow:.1f}%) suggests {'lower' if f_sow < b_sow else 'higher'} platform stickiness.",
    ]

    return html.Div([
        page_header('Are Fashion customers behaving differently?',
                     'Survey insights on how people buy.',
                     'CUSTOMER ECONOMICS'),
        html.Div(className='page-body', children=[
            html.Div(className='nykaa-edge-line'),
            synthetic_data_banner(),
            methodology_badge('P3', 'Synthetic primary-research data - placeholder for dashboard prototyping'),

            # Filters
            html.Div(style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px'}, children=[
                html.Div([
                    html.Label('Age Group', style={'fontSize': '11px', 'fontWeight': '600', 'color': '#5A5A7A'}),
                    dcc.Dropdown(id='p4-age',
                                 options=[{'label': 'All', 'value': 'All'}] +
                                         [{'label': a, 'value': a} for a in sorted(DF_CUST['age_group'].dropna().unique())],
                                 value='All', clearable=False, style={'width': '180px', 'fontSize': '12px'}),
                ]),
                html.Div([
                    html.Label('Platform', style={'fontSize': '11px', 'fontWeight': '600', 'color': '#5A5A7A'}),
                    dcc.Dropdown(id='p4-platform',
                                 options=[{'label': 'All', 'value': 'All'}] +
                                         [{'label': p, 'value': p} for p in sorted(DF_CUST['primary_platform'].dropna().unique())],
                                 value='All', clearable=False, style={'width': '180px', 'fontSize': '12px'}),
                ]),
            ]),

            html.Div(id='p4-dynamic-content', children=[
                kpis,
                html.Div(className='chart-grid', children=[
                    chart_card(dcc.Graph(figure=fig_aov, config={'displayModeBar': False})),
                    chart_card(dcc.Graph(figure=fig_return, config={'displayModeBar': False})),
                    chart_card(dcc.Graph(figure=fig_reasons, config={'displayModeBar': False}), full_width=True),
                    chart_card(dcc.Graph(figure=fig_intent, config={'displayModeBar': False})),
                    chart_card(dcc.Graph(figure=fig_sow, config={'displayModeBar': False})),
                ]),
                insight_panel(insights),
            ]),
        ]),
    ])


# ──────────────────── PAGE 5: Acquisition & Marketing ────────────────

def build_page5(year, df):
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')

    kpis = html.Div(className='kpi-row', children=[
        kpi_card('CAC PROXY', _safe(fk.get('CAC Proxy')), _safe(bk.get('CAC Proxy')),
                 formatter=fmt_inr, higher_is_better=False,
                 tooltip='Marketing + S&D per annual unique transacting customer; proxy for CAC.'),
        kpi_card('MARKETING + S&D / NSV', _safe(fk.get('Marketing + S&D %')), _safe(bk.get('Marketing + S&D %')),
                 higher_is_better=False),
        kpi_card('MARKETING / ORDER', _safe(fk.get('Marketing + S&D per Order')), _safe(bk.get('Marketing + S&D per Order')),
                 formatter=fmt_inr, higher_is_better=False),
    ])

    # Trend charts
    f_cac = [_safe(compute_all_financial_kpis(FINANCIAL_DATA, y, 'Fashion').get('CAC Proxy')) for y in YEARS]
    b_cac = [_safe(compute_all_financial_kpis(FINANCIAL_DATA, y, 'Beauty').get('CAC Proxy')) for y in YEARS]
    f_mkt = [_safe(compute_all_financial_kpis(FINANCIAL_DATA, y, 'Fashion').get('Marketing + S&D %')) for y in YEARS]
    b_mkt = [_safe(compute_all_financial_kpis(FINANCIAL_DATA, y, 'Beauty').get('Marketing + S&D %')) for y in YEARS]
    f_mkt_cust = [_safe(compute_all_financial_kpis(FINANCIAL_DATA, y, 'Fashion').get('CAC Proxy')) for y in YEARS]
    b_mkt_cust = [_safe(compute_all_financial_kpis(FINANCIAL_DATA, y, 'Beauty').get('CAC Proxy')) for y in YEARS]

    # Platform preference from customer data
    plat_fashion = df[df['category'] == 'Fashion']['primary_platform'].value_counts()
    plat_beauty = df[df['category'] == 'Beauty']['primary_platform'].value_counts()
    all_plats = sorted(set(plat_fashion.index) | set(plat_beauty.index))

    fig_plat = go.Figure()
    fig_plat.add_trace(go.Bar(y=all_plats, x=[plat_fashion.get(p, 0) for p in all_plats],
                               name='Fashion', marker_color=COLORS['fashion'], orientation='h'))
    fig_plat.add_trace(go.Bar(y=all_plats, x=[plat_beauty.get(p, 0) for p in all_plats],
                               name='Beauty', marker_color=COLORS['beauty'], orientation='h'))
    fig_plat.update_layout(**get_chart_layout(height=320, barmode='group',
        title=dict(text='Platform Preference (Survey)', font=dict(size=13), x=0, xanchor='left'),
        margin=dict(l=120, r=20, t=40, b=30)))

    # Repurchase intent by platform
    intent_by_plat = df.groupby(['category', 'primary_platform'])['repurchase_intent_3m_1_5'].mean().reset_index()
    fig_intent_plat = go.Figure()
    for cat, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
        sub = intent_by_plat[intent_by_plat['category'] == cat]
        fig_intent_plat.add_trace(go.Bar(
            x=sub['primary_platform'], y=sub['repurchase_intent_3m_1_5'],
            name=cat, marker_color=color,
            hovertemplate='%{x}: %{y:.1f}/5<extra></extra>'
        ))
    fig_intent_plat.update_layout(**get_chart_layout(height=300, barmode='group',
        title=dict(text='Repurchase Intent by Platform', font=dict(size=13), x=0, xanchor='left')))

    return html.Div([
        page_header('How expensive is growth, and what drives acquisition?',
                     'How much it costs to acquire customers and where they come from.',
                     'ACQUISITION & MARKETING'),
        html.Div(className='page-body', children=[
            html.Div(className='nykaa-edge-line'),
            methodology_badge('P1/P2', 'Company financial data - Nykaa reported or derived'),
            kpis,

            html.Div(className='chart-grid chart-grid-3', children=[
                chart_card(dcc.Graph(
                    figure=trend_chart(YEARS, f_cac, b_cac, 'CAC Proxy Trend (₹)', y_suffix=''),
                    config={'displayModeBar': False}), source='P2 - Derived'),
                chart_card(dcc.Graph(
                    figure=trend_chart(YEARS, f_mkt, b_mkt, 'Marketing + S&D % of NSV', y_suffix='%'),
                    config={'displayModeBar': False}), source='P2 - Derived'),
                chart_card(dcc.Graph(
                    figure=trend_chart(YEARS, f_mkt_cust, b_mkt_cust, 'Marketing + S&D per Customer (₹)', y_suffix=''),
                    config={'displayModeBar': False}), source='P2 - Derived'),
            ]),

            section_header('Customer Acquisition Behaviour', 'From synthetic primary research'),
            synthetic_data_banner(),

            html.Div(className='chart-grid', children=[
                chart_card(dcc.Graph(figure=fig_plat, config={'displayModeBar': False}),
                           source='P3 - Synthetic data'),
                chart_card(dcc.Graph(figure=fig_intent_plat, config={'displayModeBar': False}),
                           source='P3 - Synthetic data'),
            ]),
        ]),
    ])


# ──────────────────── PAGE 6: Returns & Friction ─────────────────────

def build_page6(df):
    if len(df) == 0:
        return html.Div([page_header('Returns & Friction', '', 'RETURNS'),
                          html.Div(className='page-body', children=[empty_state()])])

    f_ret = _safe(calculate_return_rate_survey(df, 'Fashion'), 0)
    b_ret = _safe(calculate_return_rate_survey(df, 'Beauty'), 0)

    # Return rate bar
    fig_ret = go.Figure()
    fig_ret.add_trace(go.Bar(x=['Fashion', 'Beauty'], y=[f_ret, b_ret],
                              marker_color=[COLORS['fashion'], COLORS['beauty']],
                              text=[f"{f_ret:.1f}%", f"{b_ret:.1f}%"], textposition='outside'))
    fig_ret.update_layout(**get_chart_layout(height=280, showlegend=False,
        title=dict(text='Return Rate (avg % of last 5 orders)', font=dict(size=13), x=0, xanchor='left')))

    # Return reasons
    rr_fashion = df[(df['category'] == 'Fashion') & (df['return_reason'] != 'No return in last 5 orders')]['return_reason'].value_counts()
    rr_beauty = df[(df['category'] == 'Beauty') & (df['return_reason'] != 'No return in last 5 orders')]['return_reason'].value_counts()
    all_reasons = sorted(set(rr_fashion.index) | set(rr_beauty.index))
    fig_rr = go.Figure()
    fig_rr.add_trace(go.Bar(y=all_reasons, x=[rr_fashion.get(r, 0) for r in all_reasons],
                             name='Fashion', marker_color=COLORS['fashion'], orientation='h'))
    fig_rr.add_trace(go.Bar(y=all_reasons, x=[rr_beauty.get(r, 0) for r in all_reasons],
                             name='Beauty', marker_color=COLORS['beauty'], orientation='h'))
    fig_rr.update_layout(**get_chart_layout(height=360, barmode='group',
        title=dict(text='Return Reasons', font=dict(size=13), x=0, xanchor='left'),
        margin=dict(l=220, r=20, t=40, b=30)))

    # Returners vs non-returners analysis
    df['is_returner'] = df['returned_last5'].fillna(0).astype(int) > 0

    # Intent by return status
    intent_ret = df.groupby(['category', 'is_returner'])['repurchase_intent_3m_1_5'].mean().reset_index()
    fig_intent_ret = go.Figure()
    for cat, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
        sub = intent_ret[intent_ret['category'] == cat]
        fig_intent_ret.add_trace(go.Bar(
            x=['Non-returner', 'Returner'], y=[sub[sub['is_returner'] == False]['repurchase_intent_3m_1_5'].values[0] if len(sub[sub['is_returner'] == False]) > 0 else 0,
                                                sub[sub['is_returner'] == True]['repurchase_intent_3m_1_5'].values[0] if len(sub[sub['is_returner'] == True]) > 0 else 0],
            name=cat, marker_color=color
        ))
    fig_intent_ret.update_layout(**get_chart_layout(height=280, barmode='group',
        title=dict(text='Repurchase Intent: Returners vs Non-returners', font=dict(size=13), x=0, xanchor='left')))

    # AOV by return status
    aov_ret = df.groupby(['category', 'is_returner'])['aov_mid_inr'].mean().reset_index()
    fig_aov_ret = go.Figure()
    for cat, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
        sub = aov_ret[aov_ret['category'] == cat]
        fig_aov_ret.add_trace(go.Bar(
            x=['Non-returner', 'Returner'],
            y=[sub[sub['is_returner'] == False]['aov_mid_inr'].values[0] if len(sub[sub['is_returner'] == False]) > 0 else 0,
               sub[sub['is_returner'] == True]['aov_mid_inr'].values[0] if len(sub[sub['is_returner'] == True]) > 0 else 0],
            name=cat, marker_color=color
        ))
    fig_aov_ret.update_layout(**get_chart_layout(height=280, barmode='group',
        title=dict(text='AOV: Returners vs Non-returners', font=dict(size=13), x=0, xanchor='left')))

    # Share of wallet by return status
    sow_ret = df.groupby(['category', 'is_returner'])['share_requirements_mid_pct'].mean().reset_index()
    fig_sow_ret = go.Figure()
    for cat, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
        sub = sow_ret[sow_ret['category'] == cat]
        fig_sow_ret.add_trace(go.Bar(
            x=['Non-returner', 'Returner'],
            y=[sub[sub['is_returner'] == False]['share_requirements_mid_pct'].values[0] if len(sub[sub['is_returner'] == False]) > 0 else 0,
               sub[sub['is_returner'] == True]['share_requirements_mid_pct'].values[0] if len(sub[sub['is_returner'] == True]) > 0 else 0],
            name=cat, marker_color=color
        ))
    fig_sow_ret.update_layout(**get_chart_layout(height=280, barmode='group',
        title=dict(text='Share of Wallet: Returners vs Non-returners', font=dict(size=13), x=0, xanchor='left')))

    insights = [
        f"Fashion return rate ({f_ret:.1f}%) vs Beauty ({b_ret:.1f}%).",
        "Respondents reporting returns also show different repurchase intent and spending patterns.",
        "Size, fit, and color mismatch drive most Fashion returns, mirroring broader apparel trends.",
        "These are associations, not causal claims.",
    ]

    return html.Div([
        page_header('Returns may be a symptom of shopping friction.',
                     'How returns connect to customer spending.',
                     'RETURNS & SHOPPING FRICTION'),
        html.Div(className='page-body', children=[
            html.Div(className='nykaa-edge-line'),
            synthetic_data_banner(),
            methodology_badge('P3', 'Synthetic primary-research data - placeholder for dashboard prototyping'),

            html.Div(className='chart-grid', children=[
                chart_card(dcc.Graph(figure=fig_ret, config={'displayModeBar': False})),
                chart_card(dcc.Graph(figure=fig_rr, config={'displayModeBar': False})),
            ]),
            html.Div(className='chart-grid chart-grid-3', children=[
                chart_card(dcc.Graph(figure=fig_intent_ret, config={'displayModeBar': False})),
                chart_card(dcc.Graph(figure=fig_aov_ret, config={'displayModeBar': False})),
                chart_card(dcc.Graph(figure=fig_sow_ret, config={'displayModeBar': False})),
            ]),
            insight_panel(insights),
        ]),
    ])


# ──────────────────── PAGE 7: Platform & Competitive ─────────────────

def build_page7(df):
    if len(df) == 0:
        return html.Div([page_header('Platform & Competitive', '', 'PLATFORMS'),
                          html.Div(className='page-body', children=[empty_state()])])

    # Platform preference by category
    plat_f = df[df['category'] == 'Fashion']['primary_platform'].value_counts()
    plat_b = df[df['category'] == 'Beauty']['primary_platform'].value_counts()
    all_plats = sorted(set(plat_f.index) | set(plat_b.index))

    fig_plat = go.Figure()
    fig_plat.add_trace(go.Bar(y=all_plats, x=[plat_f.get(p, 0) for p in all_plats],
                               name='Fashion', marker_color=COLORS['fashion'], orientation='h'))
    fig_plat.add_trace(go.Bar(y=all_plats, x=[plat_b.get(p, 0) for p in all_plats],
                               name='Beauty', marker_color=COLORS['beauty'], orientation='h'))
    fig_plat.update_layout(**get_chart_layout(height=340, barmode='group',
        title=dict(text='Platform Preference', font=dict(size=13), x=0, xanchor='left'),
        margin=dict(l=120, r=20, t=40, b=30)))

    # Share of wallet by platform
    sow_plat = df.groupby(['category', 'primary_platform'])['share_requirements_mid_pct'].mean().reset_index()
    fig_sow = go.Figure()
    for cat, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
        sub = sow_plat[sow_plat['category'] == cat].sort_values('primary_platform')
        fig_sow.add_trace(go.Bar(x=sub['primary_platform'], y=sub['share_requirements_mid_pct'],
                                  name=cat, marker_color=color,
                                  hovertemplate='%{x}: %{y:.1f}%<extra></extra>'))
    fig_sow.update_layout(**get_chart_layout(height=300, barmode='group',
        title=dict(text='Share of Wallet by Platform', font=dict(size=13), x=0, xanchor='left')))

    # Repurchase intent by platform
    intent_plat = df.groupby(['category', 'primary_platform'])['repurchase_intent_3m_1_5'].mean().reset_index()
    fig_intent = go.Figure()
    for cat, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
        sub = intent_plat[intent_plat['category'] == cat].sort_values('primary_platform')
        fig_intent.add_trace(go.Bar(x=sub['primary_platform'], y=sub['repurchase_intent_3m_1_5'],
                                     name=cat, marker_color=color))
    fig_intent.update_layout(**get_chart_layout(height=300, barmode='group',
        title=dict(text='Repurchase Intent by Platform (1–5)', font=dict(size=13), x=0, xanchor='left')))

    # AOV by platform
    aov_plat = df.groupby(['category', 'primary_platform'])['aov_mid_inr'].mean().reset_index()
    fig_aov = go.Figure()
    for cat, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
        sub = aov_plat[aov_plat['category'] == cat].sort_values('primary_platform')
        fig_aov.add_trace(go.Bar(x=sub['primary_platform'], y=sub['aov_mid_inr'],
                                  name=cat, marker_color=color,
                                  hovertemplate='%{x}: ₹%{y:,.0f}<extra></extra>'))
    fig_aov.update_layout(**get_chart_layout(height=300, barmode='group',
        title=dict(text='AOV by Platform (₹)', font=dict(size=13), x=0, xanchor='left')))

    # Return rate by platform
    ret_plat = df.groupby(['category', 'primary_platform'])['return_rate'].mean().reset_index()
    ret_plat['return_rate'] = ret_plat['return_rate'] * 100
    fig_ret_plat = go.Figure()
    for cat, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
        sub = ret_plat[ret_plat['category'] == cat].sort_values('primary_platform')
        fig_ret_plat.add_trace(go.Bar(x=sub['primary_platform'], y=sub['return_rate'],
                                       name=cat, marker_color=color,
                                       hovertemplate='%{x}: %{y:.1f}%<extra></extra>'))
    fig_ret_plat.update_layout(**get_chart_layout(height=300, barmode='group',
        title=dict(text='Return Rate by Platform (%)', font=dict(size=13), x=0, xanchor='left')))

    return html.Div([
        page_header('Where customers choose to shop',
                     'Where else customers shop and how loyal they are.',
                     'PLATFORM & COMPETITIVE BEHAVIOUR'),
        html.Div(className='page-body', children=[
            html.Div(className='nykaa-edge-line'),
            synthetic_data_banner(),
            methodology_badge('P3', 'Synthetic primary-research data - placeholder for dashboard prototyping'),
            html.P("Market share metrics (value share, volume share, relative market share) require total-market denominators that are not publicly available. Displayed where data exists.",
                   style={'fontSize': '11px', 'color': '#8E8EA0', 'marginBottom': '16px'}),

            chart_card(dcc.Graph(figure=fig_plat, config={'displayModeBar': False}),
                       source='P3 - Synthetic data', full_width=True),

            html.Div(className='chart-grid', children=[
                chart_card(dcc.Graph(figure=fig_sow, config={'displayModeBar': False}), source='P3'),
                chart_card(dcc.Graph(figure=fig_intent, config={'displayModeBar': False}), source='P3'),
                chart_card(dcc.Graph(figure=fig_aov, config={'displayModeBar': False}), source='P3'),
                chart_card(dcc.Graph(figure=fig_ret_plat, config={'displayModeBar': False}), source='P3'),
            ]),
        ]),
    ])


# ──────────────────── PAGE 8: Break-even & Scenarios ─────────────────

def build_page8(year):
    fk = _kpis(year, 'Fashion')
    bk = _kpis(year, 'Beauty')

    f_cpo = _safe(fk.get('Contribution per Order'), 0)
    b_cpo = _safe(bk.get('Contribution per Order'), 0)
    f_bev = _safe(fk.get('Break-even Volume'), 0)
    b_bev = _safe(bk.get('Break-even Volume'), 0)
    f_orders = _safe(_get(FINANCIAL_DATA, 'Fashion', 'Orders (mn)', year), 0) * 1e6
    b_orders = _safe(_get(FINANCIAL_DATA, 'Beauty', 'Orders (mn)', year), 0) * 1e6
    f_coverage = (f_orders / f_bev * 100) if f_bev > 0 else 0
    b_coverage = (b_orders / b_bev * 100) if b_bev > 0 else 0

    kpis = html.Div(className='kpi-row', children=[
        kpi_card('CONTRIBUTION / ORDER', f_cpo, b_cpo, formatter=fmt_inr, higher_is_better=True),
        kpi_card('BREAK-EVEN VOLUME', f_bev / 1e6 if f_bev else None, b_bev / 1e6 if b_bev else None,
                 formatter=lambda v: f"{v:.1f}M" if v else '-', higher_is_better=False,
                 show_gap=False, tooltip='Fixed & Other Expenses ÷ Contribution Profit per Order'),
        kpi_card('ACTUAL ORDERS',
                 f_orders / 1e6, b_orders / 1e6,
                 formatter=lambda v: f"{v:.1f}M" if v else '-', higher_is_better=True,
                 show_gap=False),
        kpi_card('BREAK-EVEN COVERAGE', f_coverage, b_coverage,
                 formatter=fmt_pct, higher_is_better=True),
    ])

    sliders = html.Div(className='scenario-panel', children=[
        html.H3('Scenario Adjustments (Fashion)'),
        html.P('Adjust operating variables to model profitability impact.',
               style={'fontSize': '12px', 'color': '#5A5A7A', 'marginBottom': '20px'}),

        html.Div(className='slider-row', children=[
            html.Div('Contribution Margin Improvement (pts)', className='slider-label'),
            dcc.Slider(id='scen-cm', min=0, max=15, step=0.5, value=0,
                       marks={0: '0', 5: '+5', 10: '+10', 15: '+15'},
                       tooltip={'placement': 'bottom', 'always_visible': False}),
        ]),
        html.Div(className='slider-row', children=[
            html.Div('Marketing + S&D Reduction (pts)', className='slider-label'),
            dcc.Slider(id='scen-mkt', min=0, max=15, step=0.5, value=0,
                       marks={0: '0', 5: '−5', 10: '−10', 15: '−15'},
                       tooltip={'placement': 'bottom', 'always_visible': False}),
        ]),
        html.Div(className='slider-row', children=[
            html.Div('Fulfilment Cost Reduction (pts)', className='slider-label'),
            dcc.Slider(id='scen-ful', min=0, max=5, step=0.5, value=0,
                       marks={0: '0', 2: '−2', 5: '−5'},
                       tooltip={'placement': 'bottom', 'always_visible': False}),
        ]),
        html.Div(className='slider-row', children=[
            html.Div('Order Growth (%)', className='slider-label'),
            dcc.Slider(id='scen-ord', min=0, max=50, step=5, value=0,
                       marks={0: '0%', 25: '+25%', 50: '+50%'},
                       tooltip={'placement': 'bottom', 'always_visible': False}),
        ]),
        html.Div(className='slider-row', children=[
            html.Div('AOV Improvement (%)', className='slider-label'),
            dcc.Slider(id='scen-aov', min=0, max=30, step=5, value=0,
                       marks={0: '0%', 15: '+15%', 30: '+30%'},
                       tooltip={'placement': 'bottom', 'always_visible': False}),
        ]),
    ])

    propositions = html.Div(style={'marginTop': '32px'}, children=[
        section_header('Testable Propositions', 'Evidence-based hypotheses from the data, not strategic recommendations.'),
        proposition_card(1,
            "Cutting marketing costs could boost contribution margins faster than chasing better gross margins.",
            f"Fashion Marketing + S&D is {_safe(fk.get('Marketing + S&D %'),0):.1f}% of NSV compared to Beauty's {_safe(bk.get('Marketing + S&D %'),0):.1f}%. Gross margins are nearly identical.",
        ),
        proposition_card(2,
            "Higher repeat purchase frequency is associated with higher customer value.",
            f"Beauty customers average {_safe(bk.get('Orders per Customer'),0):.2f} orders/customer vs {_safe(fk.get('Orders per Customer'),0):.2f} for Fashion. Contribution per customer: Beauty ₹{_safe(bk.get('Contribution per Order'),0) * _safe(bk.get('Orders per Customer'),0):.0f} vs Fashion ₹{_safe(fk.get('Contribution per Order'),0) * _safe(fk.get('Orders per Customer'),0):.0f}.",
        ),
        proposition_card(3,
            "Fashion loses a massive chunk of value between GMV and NSV. This matters much more than gross margins.",
            f"Fashion realisation is {_safe(fk.get('Realisation %'),0):.1f}% vs Beauty's {_safe(bk.get('Realisation %'),0):.1f}%. Fashion drops ~{100 - _safe(fk.get('Realisation %'),0):.0f}% of GMV before it even hits net sales.",
        ),
        proposition_card(4,
            "Fashion spends more on logistics per order, likely because higher-value items need more careful handling.",
            f"Fashion logistics: ₹{_safe(fk.get('Logistics Cost per Order'),0):.0f}/order vs Beauty ₹{_safe(bk.get('Logistics Cost per Order'),0):.0f}/order. Fashion AOV: ₹{_safe(fk.get('AOV (Reported)'),0):,.0f} vs Beauty ₹{_safe(bk.get('AOV (Reported)'),0):,.0f}.",
        ),
    ])

    return html.Div([
        page_header('What would it take to close the profitability gap?',
                     'Interactive break-even modeling.',
                     'BREAK-EVEN & DECISION SUPPORT'),
        html.Div(className='page-body', children=[
            html.Div(className='nykaa-edge-line'),
            methodology_badge('P2', 'Derived from Nykaa reported financial data'),
            kpis,
            html.Div(style={'display': 'flex', 'gap': '24px', 'alignItems': 'flex-start'}, children=[
                html.Div(sliders, style={'flex': '1'}),
                html.Div(id='scenario-results', style={'flex': '1'}),
            ]),
            propositions,
        ]),
    ])


# ═══════════════════════════════════════════════════════════════════
#  CALLBACKS
# ═══════════════════════════════════════════════════════════════════


@callback(
    [Output(f'nav-{href.strip("/") or "home"}', 'className') for href, _, _ in NAV_ITEMS],
    Input('url', 'pathname')
)
def update_active_links(pathname):
    if pathname is None:
        pathname = '/'
    
    classes = []
    for href, _, _ in NAV_ITEMS:
        # Match exact path, or root
        if pathname == href:
            classes.append('nav-link active')
        else:
            classes.append('nav-link')
    return classes


import urllib.parse

@callback(
    Output('url', 'search'),
    Input('year-filter', 'value'),
    State('url', 'search')
)
def update_url_search(year, current_search):
    if not year:
        return dash.no_update
        
    current_params = urllib.parse.parse_qs(current_search.lstrip('?')) if current_search else {}
    if current_params.get('year', [None])[0] == year:
        return dash.no_update
        
    current_params['year'] = [year]
    return '?' + urllib.parse.urlencode(current_params, doseq=True)

@callback(
    Output('year-filter', 'value'),
    Input('url', 'search'),
    State('year-filter', 'value')
)
def load_state_from_url(search, current_year):
    if not search:
        return dash.no_update
    params = urllib.parse.parse_qs(search.lstrip('?'))
    url_year = params.get('year', [None])[0]
    
    if url_year and url_year != current_year and url_year in ['FY22','FY23','FY24','FY25','FY26']:
        return url_year
        
    return dash.no_update

@callback(Output('page-content', 'children'),
          Input('url', 'pathname'),
          Input('year-filter', 'value'))
def route_page(pathname, year):
    year = year or 'FY26'
    if pathname == '/margin-gap':
        return build_page2(year)
    elif pathname == '/growth':
        return build_page3(year)
    elif pathname == '/customers':
        return build_page4(DF_CUST)
    elif pathname == '/acquisition':
        return build_page5(year, DF_CUST)
    elif pathname == '/returns':
        return build_page6(DF_CUST)
    elif pathname == '/platforms':
        return build_page7(DF_CUST)
    elif pathname == '/breakeven':
        return build_page8(year)
    else:
        return build_page1(year)


# Customer data filter callback for Page 4
@callback(
    Output('p4-dynamic-content', 'children'),
    Input('p4-age', 'value'),
    Input('p4-platform', 'value'),
    prevent_initial_call=True
)
def filter_customer_page(age, platform):
    df = DF_CUST.copy()
    if age and age != 'All':
        df = df[df['age_group'] == age]
    if platform and platform != 'All':
        df = df[df['primary_platform'] == platform]

    if len(df) == 0:
        return empty_state('No respondents match the selected filters.')

    # Rebuild the content for filtered data
    page = build_page4(df)
    # Extract just the dynamic content portion
    body = page.children[1]  # page-body div
    dynamic = body.children[-1] if hasattr(body, 'children') else empty_state()
    
    # Recalculate all customer metrics
    f_ret = _safe(calculate_return_rate_survey(df, 'Fashion'), 0)
    b_ret = _safe(calculate_return_rate_survey(df, 'Beauty'), 0)
    f_rep = _safe(calculate_repeat_purchase_rate(df, 'Fashion'), 0)
    b_rep = _safe(calculate_repeat_purchase_rate(df, 'Beauty'), 0)
    f_aov = _safe(calculate_aov_proxy(df, 'Fashion'), 0)
    b_aov = _safe(calculate_aov_proxy(df, 'Beauty'), 0)
    f_intent = _safe(calculate_repurchase_intent(df, 'Fashion'), 0)
    b_intent = _safe(calculate_repurchase_intent(df, 'Beauty'), 0)
    f_sow = _safe(calculate_share_of_wallet(df, 'Fashion'), 0)
    b_sow = _safe(calculate_share_of_wallet(df, 'Beauty'), 0)

    kpis = html.Div(className='kpi-row', children=[
        kpi_card('RETURN RATE', f_ret, b_ret, higher_is_better=False),
        kpi_card('REPEAT PURCHASE RATE', f_rep, b_rep, higher_is_better=True),
        kpi_card('AOV (SURVEY PROXY)', f_aov, b_aov, formatter=fmt_inr, higher_is_better=True),
        kpi_card('REPURCHASE INTENT', f_intent, b_intent, formatter=_fmt_score, higher_is_better=True),
    ])

    fig_aov = distribution_chart(df, 'aov_mid_inr', title='AOV Distribution (₹)')

    fig_return = go.Figure()
    fig_return.add_trace(go.Bar(x=['Fashion', 'Beauty'], y=[f_ret, b_ret],
                                marker_color=[COLORS['fashion'], COLORS['beauty']],
                                text=[f"{f_ret:.1f}%", f"{b_ret:.1f}%"], textposition='outside'))
    fig_return.update_layout(**get_chart_layout(height=280, showlegend=False,
        title=dict(text='Return Rate', font=dict(size=13), x=0, xanchor='left')))

    fig_intent = go.Figure()
    fig_intent.add_trace(go.Bar(x=['Fashion', 'Beauty'], y=[f_intent, b_intent],
                                 marker_color=[COLORS['fashion'], COLORS['beauty']],
                                 text=[f"{f_intent:.1f}", f"{b_intent:.1f}"], textposition='outside'))
    fig_intent.update_layout(**get_chart_layout(height=280, showlegend=False,
        title=dict(text='Repurchase Intent (1–5)', font=dict(size=13), x=0, xanchor='left')))

    fig_sow = go.Figure()
    fig_sow.add_trace(go.Bar(x=['Fashion', 'Beauty'], y=[f_sow, b_sow],
                              marker_color=[COLORS['fashion'], COLORS['beauty']],
                              text=[f"{f_sow:.1f}%", f"{b_sow:.1f}%"], textposition='outside'))
    fig_sow.update_layout(**get_chart_layout(height=280, showlegend=False,
        title=dict(text='Share of Wallet (%)', font=dict(size=13), x=0, xanchor='left')))

    return [
        kpis,
        html.Div(className='chart-grid', children=[
            chart_card(dcc.Graph(figure=fig_aov, config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=fig_return, config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=fig_intent, config={'displayModeBar': False})),
            chart_card(dcc.Graph(figure=fig_sow, config={'displayModeBar': False})),
        ]),
        insight_panel([
            f"Filtered sample: {len(df)} rows ({len(df[df['category']=='Fashion'])} Fashion, {len(df[df['category']=='Beauty'])} Beauty).",
            f"Fashion return rate: {f_ret:.1f}% | Beauty: {b_ret:.1f}%.",
            f"Fashion AOV proxy: ₹{f_aov:,.0f} | Beauty: ₹{b_aov:,.0f}.",
        ]),
    ]


# Scenario simulation callback
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
    base_other_exp = _safe(_get(FINANCIAL_DATA, 'Fashion', 'Other Expenses', year), 0)
    base_cpo = _safe(fk.get('Contribution per Order'), 0)

    # Adjustments
    new_orders_mn = base_orders_mn * (1 + ord_adj / 100)
    aov_mult = 1 + aov_adj / 100
    new_nsv = base_nsv * (new_orders_mn / base_orders_mn) * aov_mult

    new_cm_pct = base_cm_pct + cm_adj + mkt_adj + ful_adj  # mkt_adj and ful_adj are negative improvements
    new_ebitda_pct = base_ebitda_pct + cm_adj + mkt_adj + ful_adj

    new_cpo = base_cpo * (1 + cm_adj / base_cm_pct) if base_cm_pct > 0 else base_cpo
    new_contrib_profit = new_nsv * new_cm_pct / 100
    new_ebitda = new_nsv * new_ebitda_pct / 100
    new_bev = (base_other_exp * 1e7) / new_cpo if new_cpo > 0 else 0
    new_coverage = (new_orders_mn * 1e6 / new_bev * 100) if new_bev > 0 else 0

    b_ebitda_pct = _safe(bk.get('EBITDA Margin %'), 0)

    card_style = {
        'background': 'white', 'borderRadius': '12px', 'padding': '24px',
        'border': '1px solid #EEEAEF', 'boxShadow': '0 4px 16px rgba(26,26,46,0.06)',
    }

    return html.Div(style=card_style, children=[
        html.H3('Scenario Results', style={'fontSize': '14px', 'fontWeight': '700', 'marginBottom': '20px'}),

        html.Div([
            html.Div('PROJECTED EBITDA MARGIN', style={'fontSize': '10px', 'fontWeight': '600', 'letterSpacing': '1px', 'color': '#8E8EA0', 'marginBottom': '4px'}),
            html.Div(f"{new_ebitda_pct:.1f}%", style={'fontSize': '32px', 'fontWeight': '800', 'color': '#E80071', 'marginBottom': '4px'}),
            html.Div(f"vs current {base_ebitda_pct:.1f}% | Beauty benchmark {b_ebitda_pct:.1f}%",
                     style={'fontSize': '11px', 'color': '#5A5A7A'}),
        ], style={'marginBottom': '20px', 'paddingBottom': '16px', 'borderBottom': '1px solid #F0ECF2'}),

        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px'}, children=[
            html.Div([
                html.Div('Contribution Margin', style={'fontSize': '10px', 'fontWeight': '600', 'color': '#8E8EA0'}),
                html.Div(f"{new_cm_pct:.1f}%", style={'fontSize': '20px', 'fontWeight': '700'}),
                html.Div(f"(base: {base_cm_pct:.1f}%)", style={'fontSize': '10px', 'color': '#8E8EA0'}),
            ]),
            html.Div([
                html.Div('Projected NSV', style={'fontSize': '10px', 'fontWeight': '600', 'color': '#8E8EA0'}),
                html.Div(f"₹{new_nsv:,.0f} Cr", style={'fontSize': '20px', 'fontWeight': '700'}),
                html.Div(f"(base: ₹{base_nsv:,.0f} Cr)", style={'fontSize': '10px', 'color': '#8E8EA0'}),
            ]),
            html.Div([
                html.Div('Projected EBITDA', style={'fontSize': '10px', 'fontWeight': '600', 'color': '#8E8EA0'}),
                html.Div(f"₹{new_ebitda:,.0f} Cr", style={
                    'fontSize': '20px', 'fontWeight': '700',
                    'color': '#1A9E5C' if new_ebitda > 0 else '#D94B4B',
                }),
            ]),
            html.Div([
                html.Div('Break-even Coverage', style={'fontSize': '10px', 'fontWeight': '600', 'color': '#8E8EA0'}),
                html.Div(f"{new_coverage:.0f}%", style={'fontSize': '20px', 'fontWeight': '700'}),
            ]),
            html.Div([
                html.Div('Projected Orders', style={'fontSize': '10px', 'fontWeight': '600', 'color': '#8E8EA0'}),
                html.Div(f"{new_orders_mn:.1f}M", style={'fontSize': '20px', 'fontWeight': '700'}),
            ]),
            html.Div([
                html.Div('Break-even Volume', style={'fontSize': '10px', 'fontWeight': '600', 'color': '#8E8EA0'}),
                html.Div(f"{new_bev/1e6:.1f}M", style={'fontSize': '20px', 'fontWeight': '700'}),
            ]),
        ]),
    ])


# ═══════════════════════════════════════════════════════════════════
#  RUN
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    app.run(debug=False, port=8050, host='0.0.0.0')
