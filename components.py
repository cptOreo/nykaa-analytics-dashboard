"""
components.py — Nykaa Editorial UI Components
"""

from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
import content as txt

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

def fmt_pct(val, decimals=1):
    return f"{val:.{decimals}f}%" if val is not None and not np.isnan(val) else '-'

def fmt_inr(val):
    return f"₹{val:,.0f}" if val is not None and not np.isnan(val) else '-'

def fmt_number(val, decimals=2):
    return f"{val:.{decimals}f}" if val is not None and not np.isnan(val) else '-'

def get_chart_layout(**kwargs):
    layout = dict(
        font=dict(family="Inter, sans-serif", color=COLORS['charcoal']),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=True, tickfont=dict(weight='bold')),
        yaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
        showlegend=False,
    )
    layout.update(kwargs)
    return layout

def kpi_card(label, f_val, b_val, formatter=fmt_pct, tooltip=None, subtitle=None):
    fd, bd = formatter(f_val), formatter(b_val)
    gap = f_val - b_val if f_val is not None and b_val is not None else None
    
    label_el = [html.Span(label)]
    if tooltip: label_el.append(html.Span("ⓘ", className='tooltip-icon', title=tooltip))

    children = [html.Div(label_el, className='kpi-label')]
    if subtitle:
        children.append(html.Div(subtitle, style={'fontSize': '11px', 'color': 'var(--text-muted)', 'marginBottom': '12px', 'lineHeight': '1.3'}))
        
    children.extend([
        html.Div([html.Span('FASHION', className='kpi-seg fashion'), html.Span(fd, className='kpi-val')], className='kpi-row'),
        html.Div([html.Span('BEAUTY', className='kpi-seg beauty'), html.Span(bd, className='kpi-val')], className='kpi-row')
    ])
    if gap is not None:
        children.append(html.Div(f"{'▼' if gap < 0 else '▲'} {abs(gap):.1f} Gap", className='kpi-gap'))
    
    return html.Div(children, className='kpi-item')

def create_100_rupee_flow(f_nsv, b_nsv, f_gp, b_gp, f_log, b_log, f_mkt, b_mkt, f_cm, b_cm, f_oth, b_oth, f_ebitda, b_ebitda):
    def _scale(val, nsv_base): return max(0, min(100, (val / nsv_base) * 100)) if nsv_base else 0
        
    def _step(label, sublabel, f_v, b_v):
        f_pct, b_pct = _scale(f_v, f_nsv), _scale(b_v, b_nsv)
        return html.Div(style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}, children=[
            html.Div(style={'width': '200px', 'paddingRight': '16px'}, children=[
                html.Div(label, style={'fontSize': '12px', 'fontWeight': '800', 'textTransform': 'uppercase', 'color': COLORS['black']}),
                html.Div(sublabel, style={'fontSize': '10px', 'color': COLORS['muted']})
            ]),
            html.Div(style={'flex': 1, 'paddingRight': '40px'}, children=[
                html.Div(style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '4px'}, children=[
                    html.Div(f"{f_pct:.1f}%", style={'width': '40px', 'fontSize': '11px', 'fontWeight': '700', 'color': COLORS['fashion'], 'textAlign': 'right', 'marginRight': '12px'}),
                    html.Div(style={'flex': 1, 'height': '6px', 'background': 'rgba(0,0,0,0.04)'}, children=[
                        html.Div(style={'width': f"{f_pct}%" if f_v >=0 else f"{-f_pct}%", 'height': '100%', 'background': COLORS['fashion'] if f_v >=0 else COLORS['negative']})
                    ])
                ]),
                html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                    html.Div(f"{b_pct:.1f}%", style={'width': '40px', 'fontSize': '11px', 'fontWeight': '700', 'color': COLORS['beauty'], 'textAlign': 'right', 'marginRight': '12px'}),
                    html.Div(style={'flex': 1, 'height': '6px', 'background': 'rgba(0,0,0,0.04)'}, children=[
                        html.Div(style={'width': f"{b_pct}%" if b_v >=0 else f"{-b_pct}%", 'height': '100%', 'background': COLORS['beauty'] if b_v >=0 else COLORS['negative']})
                    ])
                ])
            ])
        ])

    return html.Div(style={'margin': '40px 0'}, children=[
        _step('Gross Profit', 'Capital after product cost', f_gp, b_gp),
        _step('Fulfilment', 'Cost of processing the order', f_log, b_log),
        _step('Commercial Spend', 'Cost of selling', f_mkt, b_mkt),
        _step('Contribution', 'Capital before other expenses', f_cm, b_cm),
        _step('Other Expenses', 'Overhead costs above EBITDA', f_oth, b_oth),
        _step('EBITDA', 'Capital surviving', f_ebitda, b_ebitda),
    ])

def create_customer_journey(metrics):
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

def create_gap_plot(labels, f_vals, b_vals, title, formatter=fmt_number):
    fig = go.Figure()
    for i in range(len(labels)):
        fv, bv = f_vals[i], b_vals[i]
        fig.add_trace(go.Scatter(x=[fv, bv], y=[labels[i], labels[i]], mode='lines', line=dict(color=COLORS['border'], width=1), showlegend=False))
        fig.add_trace(go.Scatter(x=[fv], y=[labels[i]], mode='markers+text', marker=dict(color=COLORS['fashion'], size=12), text=[formatter(fv)], textposition="top center", textfont=dict(color=COLORS['fashion'], size=11, weight='bold'), showlegend=False))
        fig.add_trace(go.Scatter(x=[bv], y=[labels[i]], mode='markers+text', marker=dict(color=COLORS['beauty'], size=12), text=[formatter(bv)], textposition="bottom center", textfont=dict(color=COLORS['beauty'], size=11, weight='bold'), showlegend=False))
    
    fig.update_layout(**get_chart_layout(
        title=dict(text=title, font=dict(size=14, weight='bold')), height=len(labels) * 80 + 100,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
    ))
    return fig

def trend_chart(x_labels, y_fashion, y_beauty, title, y_suffix='', annotate_gap=False):
    fig = go.Figure()
    f_text = [f"{v:.1f}{y_suffix}" if i in (0, len(y_fashion)-1) else "" for i, v in enumerate(y_fashion)]
    b_text = [f"{v:.1f}{y_suffix}" if i in (0, len(y_beauty)-1) else "" for i, v in enumerate(y_beauty)]
    
    fig.add_trace(go.Scatter(x=x_labels, y=y_fashion, mode='lines+markers+text', line=dict(color=COLORS['fashion'], width=3), marker=dict(size=8), text=f_text, textposition="top center", textfont=dict(color=COLORS['fashion'], weight='bold'), showlegend=False))
    fig.add_trace(go.Scatter(x=x_labels, y=y_beauty, mode='lines+markers+text', line=dict(color=COLORS['beauty'], width=3), marker=dict(size=8), text=b_text, textposition="bottom center", textfont=dict(color=COLORS['beauty'], weight='bold'), showlegend=False))

    if annotate_gap and y_fashion[-1] is not None and y_beauty[-1] is not None:
        gap = y_fashion[-1] - y_beauty[-1]
        fig.add_annotation(x=x_labels[-1], y=(y_fashion[-1] + y_beauty[-1])/2, text=f"{'▲' if gap>0 else '▼'} {abs(gap):.1f} Gap", showarrow=False, xshift=45, font=dict(size=12, color=COLORS['charcoal'], weight='bold'))

    fig.update_layout(**get_chart_layout(
        title=dict(text=title, font=dict(size=14, weight='bold')), height=320,
        margin=dict(r=80, l=10, t=40, b=20)
    ))
    return fig

def chart_card(chart_component, subtitle=''):
    if hasattr(chart_component, 'config'):
        if isinstance(chart_component.config, dict): chart_component.config.update({'displayModeBar': False})
        else: chart_component.config = {'displayModeBar': False}
    else: chart_component.config = {'displayModeBar': False}

    children = [chart_component]
    if subtitle: children.append(html.Div(subtitle, style={'fontSize': '11px', 'color': COLORS['muted'], 'marginTop': '8px'}))
    return html.Div(children, className='chart-container')

def annotation_box(text, segment='fashion'):
    return html.Div(text, className=f'annotation-box {segment}')

def methodology_badge(tier, text):
    return html.Div(text, className='chart-source', style={'textAlign': 'left', 'marginBottom': '24px'})

def synthetic_data_banner():
    return html.Div(txt.BADGE_SYNTHETIC, className='chart-source', style={'textAlign': 'left', 'marginBottom': '24px'})

