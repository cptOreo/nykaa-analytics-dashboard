import plotly.graph_objects as go
import pandas as pd
from components import COLORS, fmt_pct

def create_gap_plot(labels, fashion_vals, beauty_vals, title, formatter=fmt_pct):
    fig = go.Figure()
    
    for i, (label, f_val, b_val) in enumerate(zip(labels, fashion_vals, beauty_vals)):
        if pd.isna(f_val) or pd.isna(b_val): continue
        min_val, max_val = min(f_val, b_val), max(f_val, b_val)
        
        fig.add_trace(go.Scatter(x=[min_val, max_val], y=[i, i], mode='lines', line=dict(color='#E5E5E5', width=2), showlegend=False, hoverinfo='skip'))
        
        fig.add_trace(go.Scatter(x=[f_val], y=[i], mode='markers+text', name='Fashion', marker=dict(color=COLORS['fashion'], size=8), text=[formatter(f_val)], textposition='top center', textfont=dict(color=COLORS['fashion'], size=10, weight='bold'), showlegend=False))
        fig.add_trace(go.Scatter(x=[b_val], y=[i], mode='markers+text', name='Beauty', marker=dict(color=COLORS['beauty'], size=8), text=[formatter(b_val)], textposition='bottom center', textfont=dict(color=COLORS['beauty'], size=10, weight='bold'), showlegend=False))

    fig.update_layout(
        title=dict(text=title, font=dict(size=10, weight='bold', color=COLORS['muted']), x=0, y=0.9),
        height=max(120, len(labels) * 50 + 60),
        margin=dict(l=0, r=40, t=40, b=0),
        yaxis=dict(tickmode='array', tickvals=list(range(len(labels))), ticktext=labels, autorange="reversed", tickfont=dict(size=10, weight='bold', color=COLORS['charcoal']), showgrid=False, zeroline=False),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

fig = create_gap_plot(['Return Rate', 'Repeat Purchase', 'Repurchase Intent (1-5)'], [26.6, 70.0, 3.86], [17.4, 89.0, 4.12], "BEHAVIOURAL GAPS")
fig.write_html('test_plot.html')
