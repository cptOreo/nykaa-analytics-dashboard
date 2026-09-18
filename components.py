"""
components.py — Reusable UI components for the Nykaa Fashion × Beauty Dashboard.
Provides KPI cards, chart wrappers, insight panels, methodology badges, and layout helpers.
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
    """Format percentage."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    return f"{val:.{decimals}f}%"


def fmt_inr(val, decimals=0):
    """Format INR value."""
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
    """Format crore values."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    if abs(val) >= 100:
        return f"₹{val:,.{decimals}f} Cr"
    return f"₹{val:.1f} Cr"


def fmt_number(val, decimals=1):
    """Format generic number."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    if abs(val) >= 1e6:
        return f"{val/1e6:.1f}M"
    if abs(val) >= 1000:
        return f"{val:,.{decimals}f}"
    return f"{val:.{decimals}f}"


def fmt_pts(val, decimals=1):
    """Format percentage-point gap."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return '-'
    sign = '+' if val > 0 else ''
    return f"{sign}{val:.{decimals}f} pts"


# ─── Plotly Layout Template ─────────────────────────────────────────

def get_chart_layout(**overrides):
    """Returns a consistent Plotly layout dict with Nykaa styling."""
    base = dict(
        font=dict(family="Inter, Segoe UI, system-ui, sans-serif", color=COLORS['text_primary']),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=55, b=40),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
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


# ─── KPI Card Component ─────────────────────────────────────────────

def kpi_card(label, fashion_val, beauty_val, formatter=fmt_pct,
             gap_label='Gap', show_gap=True, tooltip=None,
             prev_gap=None, higher_is_better=True):
    """
    Creates a KPI comparison card showing Fashion vs Beauty values.
    
    Args:
        label: KPI name
        fashion_val: Fashion value
        beauty_val: Beauty value  
        formatter: formatting function
        gap_label: label for the gap row
        show_gap: whether to show gap
        tooltip: optional tooltip text
        prev_gap: previous period gap for showing direction
        higher_is_better: determines arrow color semantics
    """
    f_display = formatter(fashion_val)
    b_display = formatter(beauty_val)

    # Calculate gap
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

    # Direction indicator
    direction_el = []
    if prev_gap is not None and gap is not None:
        try:
            change = gap - prev_gap
            if abs(change) > 0.01:
                improving = (change > 0) if higher_is_better else (change < 0)
                arrow = '▲' if change > 0 else '▼'
                dir_class = 'improving' if improving else 'worsening'
                direction_el = [html.Span(
                    f"{arrow} {abs(change):.1f} pts vs prior",
                    className=f'kpi-change {dir_class}'
                )]
        except (TypeError, ValueError):
            pass

    card_children = [
        html.Div(
            [label, html.Span(" ⓘ", style={'fontSize': '0.9em', 'opacity': '0.6', 'cursor': 'help'})] if tooltip else label,
            className='kpi-card-label',
            title=tooltip or ''
        ),
        html.Div([
            html.Div([
                html.Div('Fashion', className='kpi-segment-label fashion'),
                html.Div(f_display, className='kpi-value fashion'),
            ], className='kpi-segment'),
            html.Div([
                html.Div('Beauty', className='kpi-segment-label beauty'),
                html.Div(b_display, className='kpi-value beauty'),
            ], className='kpi-segment'),
        ], className='kpi-values'),
    ]

    if show_gap and gap is not None:
        card_children.append(
            html.Div([
                html.Span(f'{gap_label}: ', className='kpi-gap-label'),
                html.Span(fmt_pts(gap), className=f'kpi-gap-value {gap_class}'),
            ], className='kpi-gap')
        )

    if direction_el:
        card_children.extend(direction_el)

    return html.Div(card_children, className='kpi-card')


# ─── Trend Chart ─────────────────────────────────────────────────────

def trend_chart(years, fashion_vals, beauty_vals, title, y_suffix='%',
                height=280, show_gap=False, y_format=None):
    """Creates a Fashion vs Beauty trend line chart."""
    fig = go.Figure()

    # Filter out None values for clean lines
    f_years = [y for y, v in zip(years, fashion_vals) if v is not None]
    f_vals = [v for v in fashion_vals if v is not None]
    b_years = [y for y, v in zip(years, beauty_vals) if v is not None]
    b_vals = [v for v in beauty_vals if v is not None]

    fig.add_trace(go.Scatter(
        x=f_years, y=f_vals, name='Fashion',
        line=dict(color=COLORS['fashion'], width=2.5),
        mode='lines+markers',
        marker=dict(size=6, color=COLORS['fashion']),
        hovertemplate='Fashion: %{y:.1f}' + y_suffix + '<extra></extra>',
    ))

    fig.add_trace(go.Scatter(
        x=b_years, y=b_vals, name='Beauty',
        line=dict(color=COLORS['beauty'], width=2.5),
        mode='lines+markers',
        marker=dict(size=6, color=COLORS['beauty']),
        hovertemplate='Beauty: %{y:.1f}' + y_suffix + '<extra></extra>',
    ))

    if show_gap and f_vals and b_vals:
        common_years = sorted(set(f_years) & set(b_years))
        gap_vals = []
        for y in common_years:
            fi = f_years.index(y)
            bi = b_years.index(y)
            gap_vals.append(f_vals[fi] - b_vals[bi])
        fig.add_trace(go.Bar(
            x=common_years, y=gap_vals, name='Gap (F−B)',
            marker_color='rgba(232,0,113,0.12)',
            hovertemplate='Gap: %{y:.1f}' + y_suffix + '<extra></extra>',
            width=0.3,
        ))

    layout_args = get_chart_layout(
        height=height,
        title=dict(text=title, font=dict(size=13, color=COLORS['text_primary']),
                   x=0, xanchor='left', y=0.98),
    )
    if y_format:
        layout_args['yaxis']['tickformat'] = y_format

    fig.update_layout(**layout_args)
    return fig


# ─── Bar Comparison Chart ────────────────────────────────────────────

def comparison_bar(categories, fashion_vals, beauty_vals, title,
                   height=280, horizontal=False, y_suffix=''):
    """Creates a grouped bar chart comparing Fashion and Beauty."""
    fig = go.Figure()

    if horizontal:
        fig.add_trace(go.Bar(
            y=categories, x=fashion_vals, name='Fashion',
            marker_color=COLORS['fashion'], orientation='h',
            hovertemplate='Fashion: %{x:.1f}' + y_suffix + '<extra></extra>',
        ))
        fig.add_trace(go.Bar(
            y=categories, x=beauty_vals, name='Beauty',
            marker_color=COLORS['beauty'], orientation='h',
            hovertemplate='Beauty: %{x:.1f}' + y_suffix + '<extra></extra>',
        ))
    else:
        fig.add_trace(go.Bar(
            x=categories, y=fashion_vals, name='Fashion',
            marker_color=COLORS['fashion'],
            hovertemplate='Fashion: %{y:.1f}' + y_suffix + '<extra></extra>',
        ))
        fig.add_trace(go.Bar(
            x=categories, y=beauty_vals, name='Beauty',
            marker_color=COLORS['beauty'],
            hovertemplate='Beauty: %{y:.1f}' + y_suffix + '<extra></extra>',
        ))

    fig.update_layout(
        **get_chart_layout(
            height=height, barmode='group', bargap=0.25, bargroupgap=0.1,
            title=dict(text=title, font=dict(size=13), x=0, xanchor='left', y=0.98),
        )
    )
    return fig


# ─── Waterfall Chart ─────────────────────────────────────────────────

def waterfall_chart(labels, values, title, height=340):
    """Creates a waterfall chart for profitability decomposition."""
    measures = []
    for i, label in enumerate(labels):
        if i == 0 or label in ('EBITDA', 'Contribution Profit'):
            measures.append('total')
        else:
            measures.append('relative')

    colors = []
    for i, v in enumerate(values):
        if measures[i] == 'total':
            colors.append(COLORS['fashion'] if values[i] >= 0 else COLORS['negative'])
        elif v >= 0:
            colors.append(COLORS['positive'])
        else:
            colors.append(COLORS['negative'])

    fig = go.Figure(go.Waterfall(
        name='', orientation='v',
        x=labels, y=values, measure=measures,
        connector=dict(line=dict(color=COLORS['grid'], width=1)),
        decreasing=dict(marker=dict(color=COLORS['negative'])),
        increasing=dict(marker=dict(color=COLORS['positive'])),
        totals=dict(marker=dict(color=COLORS['fashion'], line=dict(color=COLORS['fashion'], width=1))),
        textposition='outside',
        text=[f"{v:.1f}%" if abs(v) < 100 else f"₹{v:.0f} Cr" for v in values],
        textfont=dict(size=10, color=COLORS['text_secondary']),
        hovertemplate='%{x}: %{y:.1f}<extra></extra>',
    ))

    fig.update_layout(**get_chart_layout(
        height=height,
        title=dict(text=title, font=dict(size=13), x=0, xanchor='left', y=0.98),
        showlegend=False,
    ))
    return fig


# ─── Distribution Chart ─────────────────────────────────────────────

def distribution_chart(df, col, category_col='category', title='', height=280):
    """Creates a distribution comparison for Fashion vs Beauty."""
    fig = go.Figure()

    for cat, color in [('Fashion', COLORS['fashion']), ('Beauty', COLORS['beauty'])]:
        subset = df[df[category_col] == cat][col].dropna()
        if len(subset) > 0:
            fig.add_trace(go.Histogram(
                x=subset, name=cat, marker_color=color,
                opacity=0.7, nbinsx=15,
                hovertemplate=f'{cat}: %{{x}} (count: %{{y}})<extra></extra>',
            ))

    fig.update_layout(**get_chart_layout(
        height=height, barmode='overlay',
        title=dict(text=title, font=dict(size=13), x=0, xanchor='left', y=0.98),
    ))
    return fig


# ─── Horizontal Bar (single series) ─────────────────────────────────

def horizontal_bar_single(labels, values, title, color=None, height=280, suffix=''):
    """Single-series horizontal bar chart."""
    if color is None:
        color = COLORS['fashion']
    
    fig = go.Figure(go.Bar(
        y=labels, x=values, orientation='h',
        marker_color=color, 
        text=[f'{v:.1f}{suffix}' for v in values],
        textposition='outside',
        textfont=dict(size=10, color=COLORS['text_secondary']),
        hovertemplate='%{y}: %{x:.1f}' + suffix + '<extra></extra>',
    ))

    fig.update_layout(**get_chart_layout(
        height=height, showlegend=False,
        title=dict(text=title, font=dict(size=13), x=0, xanchor='left', y=0.98),
        margin=dict(l=150, r=60, t=40, b=30),
    ))
    return fig


# ─── Stacked Bar Chart ──────────────────────────────────────────────

def stacked_bar(categories, data_dict, title, height=300, y_suffix='%'):
    """
    Creates a stacked bar chart.
    data_dict: {series_name: (values_list, color)}
    """
    fig = go.Figure()
    for name, (vals, color) in data_dict.items():
        fig.add_trace(go.Bar(
            x=categories, y=vals, name=name,
            marker_color=color,
            hovertemplate=f'{name}: %{{y:.1f}}{y_suffix}<extra></extra>',
        ))

    fig.update_layout(**get_chart_layout(
        height=height, barmode='stack',
        title=dict(text=title, font=dict(size=13), x=0, xanchor='left', y=0.98),
    ))
    return fig


# ─── Scatter Plot ────────────────────────────────────────────────────

def scatter_plot(df, x, y, color_col=None, size_col=None, title='',
                 x_title='', y_title='', height=350, hover_data=None):
    """Creates a scatter plot, optionally colored by segment."""
    fig = px.scatter(
        df, x=x, y=y, color=color_col, size=size_col,
        hover_data=hover_data,
        color_discrete_map=SEGMENT_COLORS if color_col else None,
        height=height,
    )

    fig.update_layout(**get_chart_layout(
        height=height,
        title=dict(text=title, font=dict(size=13), x=0, xanchor='left', y=0.98),
        xaxis_title=x_title, yaxis_title=y_title,
    ))
    return fig


# ─── Layout Components ──────────────────────────────────────────────

def page_header(title, subtitle='', overline=''):
    """Creates a page header with title, subtitle, and optional overline."""
    children = []
    if overline:
        children.append(html.Div(overline, className='page-overline'))
    children.append(html.H1(title))
    if subtitle:
        children.append(html.P(subtitle, className='subtitle'))
    return html.Div(children, className='page-header')


def section_header(title, subtitle=''):
    """Creates a section header."""
    children = [html.H2(title, className='section-title')]
    if subtitle:
        children.append(html.P(subtitle, className='section-subtitle'))
    return html.Div(children, className='section')


def insight_panel(insights_list, title='What the data says'):
    """Creates an insight panel with auto-generated data statements."""
    if not insights_list:
        return html.Div()
    return html.Div([
        html.H3(title),
        html.Ul([html.Li(i) for i in insights_list if i]),
    ], className='insight-panel')


def methodology_badge(tier, text):
    """Creates a methodology source badge."""
    badge_class = 'badge-p1p2' if tier in ('P1', 'P2', 'P1/P2') else 'badge-p3'
    return html.Div([
        html.Span(tier, className=f'badge {badge_class}'),
        html.Span(text, className='text'),
    ], className='methodology-banner')


def synthetic_data_banner():
    """Warning banner for synthetic primary research data."""
    return html.Div(
        "Synthetic primary-research data: placeholder for dashboard prototyping",
        className='synthetic-banner'
    )


def chart_card(chart_component, title='', subtitle='', source='', full_width=False):
    """Wraps a chart in a styled card container."""
    children = []
    if title:
        children.append(html.H3(title))
    if subtitle:
        children.append(html.P(subtitle, className='chart-subtitle'))
    children.append(chart_component)
    if source:
        children.append(html.Div(source, className='chart-source'))

    cls = 'chart-card chart-card-full' if full_width else 'chart-card'
    return html.Div(children, className=cls)


def empty_state(message="Data unavailable for this selection"):
    """Empty state placeholder."""
    return html.Div(message, className='empty-state')


def proposition_card(number, statement, evidence):
    """Creates a proposition card with evidence."""
    return html.Div([
        html.H4(f"Proposition {number}"),
        html.P(f'"{statement}"', style={'fontStyle': 'italic', 'marginBottom': '8px'}),
        html.Div("Evidence", className='evidence-label'),
        html.P(evidence, className='evidence'),
    ], className='proposition-card')
