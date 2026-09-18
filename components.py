import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html
import pandas as pd
import numpy as np

COLORS = {'fashion': '#E80071', 'beauty': '#8F7C9E', 'charcoal': '#111111', 'muted': '#666666'}

def fmt_inr(v): return f"₹{v:,.0f}" if v else "-"
def fmt_pct(v): return f"{v:.1f}%" if v else "-"
def fmt_number(v): return f"{v:.2f}" if v else "-"

def methodology_badge(number, text):
    return html.Div([html.Div(number, style={'fontSize': '12px', 'fontWeight': '900', 'color': 'var(--nykaa-pink)', 'marginBottom': '4px'}), html.Div(text, style={'fontSize': '9px', 'fontWeight': '800', 'textTransform': 'uppercase', 'color': 'var(--text-muted)'})], style={'marginBottom': '16px'})

def kpi_card(title, val_f, val_b, formatter=fmt_pct, subtitle=None, tooltip=None):
    gap = val_f - val_b if val_f is not None and val_b is not None else None
    
    return html.Div(className='kpi-item', children=[
        html.Div(className='kpi-label', children=title),
        (html.Div(className='kpi-subtitle', children=subtitle) if subtitle else None),
        html.Div(className='kpi-row', children=[html.Div("FASHION", className='kpi-seg fashion'), html.Div(formatter(val_f), className='kpi-val')]),
        html.Div(className='kpi-row', children=[html.Div("BEAUTY", className='kpi-seg beauty'), html.Div(formatter(val_b), className='kpi-val')]),
        (html.Div(f"+{abs(gap):.1f}pts" if gap>0 else f"-{abs(gap):.1f}pts", className='kpi-gap') if gap is not None else None)
    ])

def annotation_box(text, chart_name=None):
    return html.Div([
        (html.Div(chart_name, className='chart-source') if chart_name else None),
        html.Div(text, className='annotation-box')
    ])

def synthetic_data_banner():
    return methodology_badge('04', "RESEARCH, SYNTHETIC PRIMARY RESEARCH DATA (PLACEHOLDER FOR PROTOTYPING)")

def create_100_rupee_flow(f_nsv, b_nsv, f_gp, b_gp, f_log, b_log, f_mkt, b_mkt, f_cm, b_cm, f_oth, b_oth, f_ebitda, b_ebitda):
    def pct(val, nsv): return (val/nsv)*100 if nsv and val else 0
    
    metrics = [
        ("GROSS PROFIT", "Capital after product cost", pct(f_gp, f_nsv), pct(b_gp, b_nsv)),
        ("FULFILMENT", "Cost of processing the order", pct(f_log, f_nsv), pct(b_log, b_nsv)),
        ("COMMERCIAL SPEND", "Cost of selling", pct(f_mkt, f_nsv), pct(b_mkt, b_nsv)),
        ("CONTRIBUTION", "Capital before other expenses", pct(f_cm, f_nsv), pct(b_cm, b_nsv)),
        ("OTHER EXPENSES", "Overhead costs above EBITDA", pct(f_oth, f_nsv), pct(b_oth, b_nsv)),
        ("EBITDA", "Capital surviving", pct(f_ebitda, f_nsv), pct(b_ebitda, b_nsv))
    ]
    
    rows = []
    for title, desc, f_pct, b_pct in metrics:
        rows.append(html.Div(className='kpi-item', style={'paddingTop': '12px', 'paddingBottom': '12px'}, children=[
            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '40px'}, children=[
                html.Div(style={'width': '200px', 'flexShrink': '0'}, children=[
                    html.Div(title, className='kpi-label'),
                    html.Div(desc, className='kpi-subtitle', style={'marginBottom': '0'})
                ]),
                html.Div(style={'flex': '1', 'position': 'relative'}, children=[
                    html.Div(style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '12px'}, children=[
                        html.Div(f"{f_pct:.1f}%", style={'width': '40px', 'fontSize': '10px', 'fontWeight': '800', 'color': COLORS['fashion']}),
                        html.Div(style={'flex': '1', 'height': '4px', 'backgroundColor': '#EEE'}, children=[
                            html.Div(style={'width': f"{min(100, f_pct)}%", 'height': '100%', 'backgroundColor': COLORS['fashion']})
                        ])
                    ]),
                    html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                        html.Div(f"{b_pct:.1f}%", style={'width': '40px', 'fontSize': '10px', 'fontWeight': '800', 'color': COLORS['beauty']}),
                        html.Div(style={'flex': '1', 'height': '4px', 'backgroundColor': '#EEE'}, children=[
                            html.Div(style={'width': f"{min(100, b_pct)}%", 'height': '100%', 'backgroundColor': COLORS['beauty']})
                        ])
                    ])
                ])
            ])
        ]))
    return html.Div(rows)

def trend_chart(x_labels, y_fashion, y_beauty, title, y_suffix='', annotate_gap=False, yaxis_range=None):
    fig = go.Figure()
    f_text = [f"{v:.1f}{y_suffix}" if i in (0, len(y_fashion)-1) else "" for i, v in enumerate(y_fashion)]
    b_text = [f"{v:.1f}{y_suffix}" if i in (0, len(y_beauty)-1) else "" for i, v in enumerate(y_beauty)]
    
    fig.add_trace(go.Scatter(x=x_labels, y=y_fashion, mode='lines+markers+text', line=dict(color=COLORS['fashion'], width=3), marker=dict(size=6), text=f_text, textposition="top center", textfont=dict(color=COLORS['fashion'], weight='bold', size=10), showlegend=False))
    fig.add_trace(go.Scatter(x=x_labels, y=y_beauty, mode='lines+markers+text', line=dict(color=COLORS['beauty'], width=3), marker=dict(size=6), text=b_text, textposition="bottom center", textfont=dict(color=COLORS['beauty'], weight='bold', size=10), showlegend=False))

    if annotate_gap and y_fashion[-1] is not None and y_beauty[-1] is not None:
        gap = y_fashion[-1] - y_beauty[-1]
        fig.add_annotation(x=x_labels[-1], y=(y_fashion[-1] + y_beauty[-1])/2, text=f"+{abs(gap):.1f}pts" if gap>0 else f"-{abs(gap):.1f}pts", showarrow=False, xshift=35, font=dict(size=10, color=COLORS['charcoal'], weight='bold'))

    y_axis_layout = dict(showticklabels=False, showgrid=False, zeroline=False)
    if yaxis_range: y_axis_layout['range'] = yaxis_range

    fig.update_layout(
        title=dict(text=title, font=dict(size=10, weight='bold', color=COLORS['muted']), x=0, y=0.9),
        height=240,
        margin=dict(l=0, r=60, t=40, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showline=False, tickfont=dict(size=10, weight='bold', color=COLORS['charcoal'])),
        yaxis=y_axis_layout
    )
    return fig

def chart_card(chart_component):
    return html.Div(chart_component)

def create_customer_journey(metrics):
    cols = []
    for m in metrics:
        cols.append(html.Div(className='journey-col', children=[
            html.Div(m['label'], className='journey-step'),
            html.Div(m['fashion'], className='journey-val-f'),
            html.Div(m['beauty'], className='journey-val-b')
        ]))
    return html.Div(className='journey-matrix', children=cols)

def create_gap_plot(labels, fashion_vals, beauty_vals, title, formatter=fmt_pct):
    fig = make_subplots(rows=len(labels), cols=1, shared_xaxes=False, vertical_spacing=0.15)
    
    for i, (label, f_val, b_val) in enumerate(zip(labels, fashion_vals, beauty_vals)):
        row = i + 1
        
        # Add invisible annotation for row label (simulating y-axis)
        fig.add_annotation(
            x=0, y=0.5, xref=f"x{row if row > 1 else ''} domain", yref=f"y{row if row > 1 else ''} domain",
            text=label, showarrow=False, xanchor="right", xshift=-40,
            font=dict(size=10, weight="bold", color=COLORS['charcoal'])
        )

        if pd.isna(f_val) or pd.isna(b_val): continue
            
        min_val, max_val = min(f_val, b_val), max(f_val, b_val)
        
        fig.add_trace(go.Scatter(x=[min_val, max_val], y=[0, 0], mode='lines', line=dict(color='#E5E5E5', width=2), showlegend=False, hoverinfo='skip'), row=row, col=1)
        fig.add_trace(go.Scatter(x=[f_val], y=[0], mode='markers+text', name='Fashion', marker=dict(color=COLORS['fashion'], size=8), text=[formatter(f_val)], textposition='top center', textfont=dict(color=COLORS['fashion'], size=10, weight='bold'), showlegend=False), row=row, col=1)
        fig.add_trace(go.Scatter(x=[b_val], y=[0], mode='markers+text', name='Beauty', marker=dict(color=COLORS['beauty'], size=8), text=[formatter(b_val)], textposition='bottom center', textfont=dict(color=COLORS['beauty'], size=10, weight='bold'), showlegend=False), row=row, col=1)
        
        # Add padding to x-axis to prevent cutoff
        x_range = max_val - min_val
        pad = max(x_range * 0.2, 0.5)
        fig.update_xaxes(range=[min_val - pad, max_val + pad], showgrid=False, zeroline=False, showticklabels=False, row=row, col=1)
        fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 1], row=row, col=1)

    fig.update_layout(
        title=dict(text=title, font=dict(size=10, weight='bold', color=COLORS['muted']), x=0, y=0.95),
        height=max(120, len(labels) * 60 + 60),
        margin=dict(l=190, r=40, t=40, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig
