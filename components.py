"""
components.py — Nykaa Editorial UI Components
"""

from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

COLORS = {
    'fashion': '#E80071',
    'beauty': '#8F7C9E',
    'black': '#111111',
    'charcoal': '#333333',
    'muted': '#666666',
    'light': '#999999',
    'border': '#DDDDDD',
    'positive': '#1A9E5C',
    'negative': '#D94B4B'
}

SEGMENT_COLORS = {'Fashion': COLORS['fashion'], 'Beauty': COLORS['beauty']}

# ─── Formatting Helpers ─────────────────────────────────────────────
def fmt_pct(val, decimals=1):
    if val is None or (isinstance(val, float) and np.isnan(val)): return '-'
    return f"{val:.{decimals}f}%"

def fmt_inr(val):
    if val is None or (isinstance(val, float) and np.isnan(val)): return '-'
    return f"₹{val:,.0f}"

def fmt_cr(val):
    if val is None or (isinstance(val, float) and np.isnan(val)): return '-'
    return f"₹{val:.1f} Cr"

def fmt_number(val, decimals=2):
    if val is None or (isinstance(val, float) and np.isnan(val)): return '-'
    return f"{val:.{decimals}f}"

def fmt_pts(val, decimals=1):
    if val is None or (isinstance(val, float) and np.isnan(val)): return '-'
    return f"{abs(val):.{decimals}f} pp"

# ─── Chart Defaults ──────────────────────────────────────────────────
def get_chart_layout(**kwargs):
    """Editorial, minimalistic Plotly layout."""
    layout = dict(
        font=dict(family="Inter, sans-serif", color=COLORS['charcoal']),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor=COLORS['black'], linewidth=2),
        yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor=COLORS['black'], linewidth=2),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    layout.update(kwargs)
    return layout

# ─── KPI Strip Components ────────────────────────────────────────────

def kpi_card(label, f_val, b_val, formatter=fmt_pct, tooltip=None):
    """Compact editorial KPI item for the strip."""
    fd = formatter(f_val)
    bd = formatter(b_val)
    gap = None
    if f_val is not None and b_val is not None:
        try: gap = f_val - b_val
        except: gap = None
    
    label_el = [label]
    if tooltip:
        label_el.append(html.Span("ⓘ", className='tooltip-icon', title=tooltip))

    children = [
        html.Div(label_el, className='kpi-label'),
        html.Div([
            html.Span('FASHION', className='kpi-seg fashion'),
            html.Span(fd, className='kpi-val')
        ], className='kpi-row'),
        html.Div([
            html.Span('BEAUTY', className='kpi-seg beauty'),
            html.Span(bd, className='kpi-val')
        ], className='kpi-row')
    ]
    if gap is not None:
        children.append(html.Div(f"{'▼' if gap < 0 else '▲'} {fmt_pts(gap)} Gap", className='kpi-gap'))
    
    return html.Div(children, className='kpi-item')

# ─── HTML-based Editorial Visuals ────────────────────────────────────

def create_100_rupee_flow(f_nsv, b_nsv, f_gp, b_gp, f_log, b_log, f_mkt, b_mkt, f_cm, b_cm, f_oth, b_oth, f_ebitda, b_ebitda):
    """Creates the 'Start with 100' parallel flow visualization using HTML."""
    
    def _scale(val, nsv_base):
        return max(0, min(100, (val / nsv_base) * 100)) if nsv_base else 0
        
    def _step(label, f_v, b_v):
        f_pct = _scale(f_v, f_nsv)
        b_pct = _scale(b_v, b_nsv)
        return html.Div(className='flow-step', children=[
            html.Div(label, className='flow-label'),
            html.Div(className='flow-bar-wrapper', children=[
                html.Div(
                    f"{f_pct:.1f}%", 
                    className=f"flow-bar-fill fashion {'negative' if f_v < 0 else ''}", 
                    style={'width': f"{f_pct}%" if f_v >= 0 else f"{-f_pct}%", 'top': 0, 'height': '50%'}
                ),
                html.Div(
                    f"{b_pct:.1f}%", 
                    className=f"flow-bar-fill beauty {'negative' if b_v < 0 else ''}", 
                    style={'width': f"{b_pct}%" if b_v >= 0 else f"{-b_pct}%", 'top': '50%', 'height': '50%'}
                )
            ])
        ])

    return html.Div(className='flow-container', children=[
        html.Div(className='flow-column', children=[
            _step('Gross Profit', f_gp, b_gp),
            _step('- Fulfilment', f_log, b_log),
            _step('- Marketing & S&D', f_mkt, b_mkt),
            _step('Contribution', f_cm, b_cm),
            _step('- Other Expenses', f_oth, b_oth),
            _step('EBITDA', f_ebitda, b_ebitda),
        ])
    ])

def create_customer_journey(metrics):
    """Editorial Customer Journey Flow"""
    nodes = []
    for m in metrics:
        nodes.append(html.Div(className='journey-node', children=[
            html.Div(m['label'], className='node-title'),
            html.Div(m['fashion'], className='node-val', style={'color': COLORS['fashion'], 'fontSize': '24px', 'marginBottom': '4px'}),
            html.Div(m['beauty'], className='node-val', style={'color': COLORS['beauty'], 'fontSize': '16px'})
        ]))
        if m != metrics[-1]:
            nodes.append(html.Div("→", className='journey-arrow'))
            
    return html.Div(className='journey-container', children=nodes)

# ─── Plotly Custom Charts ────────────────────────────────────────────

def create_gap_plot(labels, f_vals, b_vals, title, formatter=fmt_pct):
    """Custom dumbbell/gap plot for comparing Fashion vs Beauty directly."""
    fig = go.Figure()

    for i in range(len(labels)):
        fv = f_vals[i]
        bv = b_vals[i]
        
        # Line connecting them
        fig.add_trace(go.Scatter(
            x=[fv, bv], y=[labels[i], labels[i]],
            mode='lines', line=dict(color=COLORS['border'], width=4),
            showlegend=False
        ))
        # Fashion dot
        fig.add_trace(go.Scatter(
            x=[fv], y=[labels[i]],
            mode='markers+text',
            marker=dict(color=COLORS['fashion'], size=16),
            text=[formatter(fv)],
            textposition="top center",
            textfont=dict(color=COLORS['fashion'], size=12, weight='bold'),
            name='Fashion' if i == 0 else '', showlegend=(i==0)
        ))
        # Beauty dot
        fig.add_trace(go.Scatter(
            x=[bv], y=[labels[i]],
            mode='markers+text',
            marker=dict(color=COLORS['beauty'], size=12),
            text=[formatter(bv)],
            textposition="bottom center",
            textfont=dict(color=COLORS['beauty'], size=11, weight='bold'),
            name='Beauty' if i == 0 else '', showlegend=(i==0)
        ))

    fig.update_layout(**get_chart_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        height=len(labels) * 80 + 100,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, linewidth=2, linecolor=COLORS['black'])
    ))
    return fig

def trend_chart(x_labels, y_fashion, y_beauty, title, y_suffix='', annotate_gap=False):
    """Editorial trend line chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_labels, y=y_fashion, name='Fashion',
        mode='lines+markers', line=dict(color=COLORS['fashion'], width=3),
        marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=x_labels, y=y_beauty, name='Beauty',
        mode='lines+markers', line=dict(color=COLORS['beauty'], width=2),
        marker=dict(size=6)
    ))

    # Add Gap Annotation on last point
    if annotate_gap and y_fashion[-1] is not None and y_beauty[-1] is not None:
        gap = y_fashion[-1] - y_beauty[-1]
        fig.add_annotation(
            x=x_labels[-1], y=(y_fashion[-1] + y_beauty[-1])/2,
            text=f"{'▲' if gap>0 else '▼'} {abs(gap):.1f} Gap",
            showarrow=False, xshift=40,
            font=dict(size=12, color=COLORS['charcoal'], weight='bold')
        )

    fig.update_layout(**get_chart_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        height=350,
        yaxis=dict(ticksuffix=y_suffix, showgrid=True, gridcolor=COLORS['border'])
    ))
    return fig

def waterfall_chart(labels, values, title, seg='Fashion', height=400):
    """Editorial Waterfall."""
    measures = ['total' if i==0 or lbl in ('EBITDA', 'Contribution Profit') else 'relative' for i, lbl in enumerate(labels)]
    c_pri = COLORS['fashion'] if seg == 'Fashion' else COLORS['beauty']
    
    fig = go.Figure(go.Waterfall(
        orientation='v', x=labels, y=values, measure=measures,
        connector=dict(line=dict(color=COLORS['border'], width=2)),
        decreasing=dict(marker=dict(color=COLORS['negative'])),
        increasing=dict(marker=dict(color=COLORS['positive'])),
        totals=dict(marker=dict(color=c_pri)),
        text=[f"{v:.1f}%" if abs(v) < 100 else f"₹{v:.0f}" for v in values],
        textposition='outside',
        textfont=dict(size=12, color=COLORS['black'], weight='bold')
    ))

    fig.update_layout(**get_chart_layout(
        title=dict(text=title, font=dict(size=18, weight='bold')),
        height=height, showlegend=False
    ))
    return fig


# ─── Layout Wrappers ────────────────────────────────────────────────

def chart_card(chart_component, title='', subtitle='', source=''):
    """Wraps a chart in an editorial container."""
    # Inject Export capability
    export_config = {
        'displayModeBar': True, 'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'toImageButtonOptions': {'format': 'png', 'filename': 'nykaa_chart'}
    }
    if hasattr(chart_component, 'config'):
        if isinstance(chart_component.config, dict):
            chart_component.config.update(export_config)
        else:
            chart_component.config = export_config
    else:
        chart_component.config = export_config

    children = []
    if title: children.append(html.H3(title, className='chart-title'))
    if subtitle: children.append(html.P(subtitle, className='chart-subtitle'))
    children.append(chart_component)
    if source: children.append(html.Div(source, className='chart-source'))

    return html.Div(children, className='chart-container')

def annotation_box(text, segment='fashion'):
    """Editorial annotation callout."""
    return html.Div(text, className=f'annotation-box {segment}')

def insight_panel(text, title='THE BUSINESS PROBLEM'):
    """Reused for large text blocks."""
    if isinstance(text, list):
        content = html.Ul([html.Li(t) for t in text if t])
    else:
        content = html.P(text)
    return html.Div([
        html.H3(title),
        content
    ], className='annotation-box')

def methodology_badge(tier, text):
    return html.Div(f"{tier} — {text}", className='chart-source')

def synthetic_data_banner():
    return html.Div("SYNTHETIC PRIMARY-RESEARCH DATA (PLACEHOLDER)", className='synthetic-warning')
