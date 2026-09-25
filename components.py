"""
components.py — Reusable UI components for the Nykaa Fashion × Beauty Dashboard.
Single-page, five-umbrella structure.
"""

from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


# ─── Color Palette ───────────────────────────────────────────────────
COLORS = {
    'fashion': '#E80071',
    'fashion_light': '#FF4DA6',
    'fashion_soft': '#FFF0F7',
    'beauty': '#7B6D8D',
    'beauty_light': '#A394B4',
    'beauty_soft': '#F3EFF6',
    'charcoal': '#1A1A2E',
    'text_primary': '#1A1A2E',
    'text_secondary': '#5A5A7A',
    'text_muted': '#8E8EA0',
    'positive': '#1A9E5C',
    'negative': '#D94B4B',
    'surface': '#FFFFFF',
    'grid': '#F0ECF2',
    'border': '#EEEAEF',
}

SEGMENT_COLORS = {'Fashion': COLORS['fashion'], 'Beauty': COLORS['beauty']}


# ─── Formatting Helpers ─────────────────────────────────────────────

def fmt_pct(val, decimals=1):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    return f"{val:.{decimals}f}%"

def fmt_inr(val, decimals=0):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    if abs(val) >= 1e7:
        return f"₹{val/1e7:.1f} Cr"
    if abs(val) >= 1e5:
        return f"₹{val/1e5:.1f} L"
    if abs(val) >= 1000:
        return f"₹{val:,.{decimals}f}"
    return f"₹{val:.{decimals}f}"

def fmt_cr(val, decimals=0):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    if abs(val) >= 100:
        return f"₹{val:,.{decimals}f} Cr"
    return f"₹{val:.1f} Cr"

def fmt_number(val, decimals=1):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    if abs(val) >= 1e6:
        return f"{val/1e6:.1f}M"
    if abs(val) >= 1000:
        return f"{val:,.{decimals}f}"
    return f"{val:.{decimals}f}"

def fmt_pts(val, decimals=1):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    sign = '+' if val > 0 else ''
    return f"{sign}{val:.{decimals}f} pts"


# ─── Plotly Layout Template ─────────────────────────────────────────

def get_chart_layout(**overrides):
    base = dict(
        font=dict(family="Inter, Segoe UI, system-ui, sans-serif", color=COLORS['text_primary']),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=80, b=60),
        legend=dict(
            orientation='h', yanchor='top', y=-0.2, xanchor='center', x=0.5,
            font=dict(size=11, color=COLORS['text_secondary']),
            bgcolor='rgba(0,0,0,0)',
        ),
        xaxis=dict(
            gridcolor=COLORS['grid'], gridwidth=1, showline=False,
            tickfont=dict(size=11, color=COLORS['text_muted']),
        ),
        yaxis=dict(
            gridcolor=COLORS['grid'], gridwidth=1, showline=False,
            tickfont=dict(size=11, color=COLORS['text_muted']),
            zeroline=True, zerolinecolor=COLORS['grid'], zerolinewidth=1,
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor=COLORS['surface'], bordercolor=COLORS['border'],
            font=dict(size=12, family="Inter, sans-serif", color=COLORS['text_primary']),
        ),
    )
    base.update(overrides)
    return base


# ─── Section Anchor ─────────────────────────────────────────────────

def section_anchor(section_id, number, title, subtitle=''):
    """Creates a section anchor with number, title, and optional subtitle."""
    children = [
        html.Div(f"0{number}", className='section-number'),
        html.H2(title, className='section-title'),
    ]
    if subtitle:
        children.append(html.P(subtitle, className='section-subtitle'))
    return html.Div(children, className='section-anchor', id=section_id)


# ─── KPI Card (compact for single-page) ─────────────────────────────

def kpi_sparkline(f_vals, b_vals):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=f_vals, mode='lines', line=dict(color=COLORS['fashion'], width=1.5), hoverinfo='skip'))
    fig.add_trace(go.Scatter(y=b_vals, mode='lines', line=dict(color=COLORS['beauty'], width=1.5), hoverinfo='skip'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=8, b=0),
        height=24,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True)
    )
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def kpi_card(label, fashion_val, beauty_val, formatter=fmt_pct,
             show_gap=True, tooltip=None, higher_is_better=True,
             f_trend=None, b_trend=None):
    f_display = formatter(fashion_val)
    b_display = formatter(beauty_val)

    gap = None
    if fashion_val is not None and beauty_val is not None:
        try:
            gap = fashion_val - beauty_val
        except (TypeError, ValueError):
            gap = None

    gap_class = 'neutral'
    if gap is not None:
        if higher_is_better:
            gap_class = 'negative' if gap < 0 else 'positive'
        else:
            gap_class = 'positive' if gap < 0 else 'negative'

    card_children = [
        html.Div(
            [label, html.Span(" ⓘ", style={'fontSize': '0.85em', 'opacity': '0.5', 'cursor': 'help'})] if tooltip else label,
            className='kpi-card-label',
            title=tooltip or ''
        ),
        html.Div([
            html.Div([
                html.Div('F', className='kpi-segment-label fashion'),
                html.Div(f_display, className='kpi-value fashion'),
            ], className='kpi-segment'),
            html.Div([
                html.Div('B', className='kpi-segment-label beauty'),
                html.Div(b_display, className='kpi-value beauty'),
            ], className='kpi-segment'),
        ], className='kpi-values'),
    ]

    if show_gap and gap is not None:
        card_children.append(
            html.Div([
                html.Span('Gap: ', className='kpi-gap-label'),
                html.Span(fmt_pts(gap), className=f'kpi-gap-value {gap_class}'),
            ], className='kpi-gap')
        )

    if f_trend is not None and b_trend is not None:
        card_children.append(html.Div(kpi_sparkline(f_trend, b_trend), style={'marginTop': '2px'}))

    return html.Div(card_children, className='kpi-card')


# ─── Trend Chart ─────────────────────────────────────────────────────

def trend_chart(years, fashion_vals, beauty_vals, title, y_suffix='%',
                height=260, show_gap=False):
    fig = go.Figure()

    f_years = [y for y, v in zip(years, fashion_vals) if v is not None]
    f_vals = [v for v in fashion_vals if v is not None]
    b_years = [y for y, v in zip(years, beauty_vals) if v is not None]
    b_vals = [v for v in beauty_vals if v is not None]

    fig.add_trace(go.Scatter(
        x=f_years, y=f_vals, name='Fashion',
        line=dict(color=COLORS['fashion'], width=2.5),
        mode='lines+markers',
        marker=dict(size=5, color=COLORS['fashion']),
        hovertemplate='Fashion: %{y:.1f}' + y_suffix + '<extra></extra>',
    ))
    fig.add_trace(go.Scatter(
        x=b_years, y=b_vals, name='Beauty',
        line=dict(color=COLORS['beauty'], width=2.5),
        mode='lines+markers',
        marker=dict(size=5, color=COLORS['beauty']),
        hovertemplate='Beauty: %{y:.1f}' + y_suffix + '<extra></extra>',
    ))

    fig.update_layout(**get_chart_layout(
        height=height,
        title=dict(text=title, font=dict(size=12, color=COLORS['text_primary']),
                   x=0, xanchor='left'),
    ))
    return fig


# ─── Bar Comparison Chart ────────────────────────────────────────────

def comparison_bar(categories, fashion_vals, beauty_vals, title,
                   height=260, y_suffix=''):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories, y=fashion_vals, name='Fashion',
        marker_color=COLORS['fashion'],
        text=[f"{v:.1f}{y_suffix}" for v in fashion_vals], textposition='outside',
        textfont=dict(size=9),
        hovertemplate='Fashion: %{y:.1f}' + y_suffix + '<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        x=categories, y=beauty_vals, name='Beauty',
        marker_color=COLORS['beauty'],
        text=[f"{v:.1f}{y_suffix}" for v in beauty_vals], textposition='outside',
        textfont=dict(size=9),
        hovertemplate='Beauty: %{y:.1f}' + y_suffix + '<extra></extra>',
    ))
    fig.update_layout(**get_chart_layout(
        height=height, barmode='group', bargap=0.25,
        title=dict(text=title, font=dict(size=12), x=0, xanchor='left'),
    ))
    return fig


# ─── Dumbbell Chart ──────────────────────────────────────────────────

def dumbbell_chart(categories, fashion_vals, beauty_vals, title, height=260, y_suffix='%'):
    fig = go.Figure()
    
    for i, cat in enumerate(categories):
        f_val = fashion_vals[i]
        b_val = beauty_vals[i]
        
        # Add the line connecting them
        fig.add_trace(go.Scatter(
            x=[f_val, b_val], y=[cat, cat],
            mode='lines',
            line=dict(color=COLORS['grid'], width=3),
            showlegend=False, hoverinfo='skip'
        ))
        
    # Add Fashion dots
    fig.add_trace(go.Scatter(
        x=fashion_vals, y=categories, name='Fashion',
        mode='markers', marker=dict(color=COLORS['fashion'], size=10),
        hovertemplate='Fashion: %{x:.1f}' + y_suffix + '<extra></extra>'
    ))
    
    # Add Beauty dots
    fig.add_trace(go.Scatter(
        x=beauty_vals, y=categories, name='Beauty',
        mode='markers', marker=dict(color=COLORS['beauty'], size=10),
        hovertemplate='Beauty: %{x:.1f}' + y_suffix + '<extra></extra>'
    ))

    fig.update_layout(**get_chart_layout(
        height=height, 
        title=dict(text=title, font=dict(size=12), x=0, xanchor='left'),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=100, r=40, t=80, b=60)
    ))
    return fig


# ─── Waterfall Chart ─────────────────────────────────────────────────

def waterfall_chart(labels, values, title, height=280, segment='fashion'):
    measures = []
    for i, label in enumerate(labels):
        if i == 0:
            measures.append('absolute')
        elif label in ('GP', 'CM', 'EBITDA', 'Contribution'):
            measures.append('total')
        else:
            measures.append('relative')

    fig = go.Figure(go.Waterfall(
        name='', orientation='v',
        x=labels, y=values, measure=measures,
        connector=dict(line=dict(color=COLORS['grid'], width=1)),
        decreasing=dict(marker=dict(color=COLORS['negative'])),
        increasing=dict(marker=dict(color=COLORS['positive'])),
        totals=dict(marker=dict(color=COLORS[segment], line=dict(color=COLORS[segment], width=1))),
        textposition='outside',
        text=[f"{v:.1f}%" for v in values],
        textfont=dict(size=9, color=COLORS['text_secondary']),
        hovertemplate='%{x}: %{y:.1f}<extra></extra>',
    ))
    fig.update_layout(**get_chart_layout(
        height=height, showlegend=False,
        title=dict(text=title, font=dict(size=12), x=0, xanchor='left'),
    ))
    return fig


# ─── Chart Card ──────────────────────────────────────────────────────

def chart_card(chart_component, source='', full_width=False):
    children = [chart_component]
    if source:
        children.append(html.Div(source, className='chart-source'))
    cls = 'chart-card chart-card-full' if full_width else 'chart-card'
    return html.Div(children, className=cls)


# ─── Proposition Card ────────────────────────────────────────────────

def proposition_card(number, proposition, evidence, rationale, impact, measure):
    return html.Div([
        html.Div(f"PROPOSITION {number}", className='prop-number'),
        html.P(proposition, className='prop-statement', style={'marginBottom': '16px'}),
        html.Div([
            html.Span("EVIDENCE: ", style={'fontWeight': '800', 'fontSize': '10px', 'color': COLORS['text_muted']}),
            html.Span(evidence)
        ], className='prop-evidence', style={'marginBottom': '8px'}),
        html.Div([
            html.Span("RATIONALE: ", style={'fontWeight': '800', 'fontSize': '10px', 'color': COLORS['text_muted']}),
            html.Span(rationale)
        ], className='prop-evidence', style={'marginBottom': '8px'}),
        html.Div([
            html.Span("EXPECTED IMPACT: ", style={'fontWeight': '800', 'fontSize': '10px', 'color': COLORS['text_muted']}),
            html.Span(impact)
        ], className='prop-evidence', style={'marginBottom': '8px'}),
        html.Div([
            html.Span("MEASURE: ", style={'fontWeight': '800', 'fontSize': '10px', 'color': COLORS['text_muted']}),
            html.Span(measure)
        ], className='prop-evidence'),
    ], className='proposition-card')
