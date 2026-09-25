import re

with open('/run/media/ravid/New Volume/mrv/dashboard/components.py', 'r') as f:
    code = f.read()

# 1. get_chart_layout: Remove axis lines, make entirely minimal
new_layout = """def get_chart_layout(**kwargs):
    layout = dict(
        font=dict(family="Inter, sans-serif", color=COLORS['charcoal']),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0), # tighter margins
        xaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=True, tickfont=dict(weight='bold')),
        yaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False), # hide Y axis entirely
        showlegend=False, # kill legends globally
    )
    layout.update(kwargs)
    return layout"""
code = re.sub(r"def get_chart_layout\(\*\*kwargs\):.*?return layout", new_layout, code, flags=re.DOTALL)

# 2. create_100_rupee_flow: Make it an elegant editorial table/bar hybrid
new_flow = """def create_100_rupee_flow(f_nsv, b_nsv, f_gp, b_gp, f_log, b_log, f_mkt, b_mkt, f_cm, b_cm, f_oth, b_oth, f_ebitda, b_ebitda):
    def _scale(val, nsv_base):
        return max(0, min(100, (val / nsv_base) * 100)) if nsv_base else 0
        
    def _step(label, f_v, b_v):
        f_pct = _scale(f_v, f_nsv)
        b_pct = _scale(b_v, b_nsv)
        return html.Div(style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '16px'}, children=[
            html.Div(label, style={'width': '160px', 'fontSize': '12px', 'fontWeight': '800', 'textTransform': 'uppercase'}),
            
            html.Div(style={'flex': 1, 'paddingRight': '40px'}, children=[
                # Fashion row
                html.Div(style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '4px'}, children=[
                    html.Div(f"{f_pct:.1f}%", style={'width': '40px', 'fontSize': '11px', 'fontWeight': '700', 'color': COLORS['fashion'], 'textAlign': 'right', 'marginRight': '12px'}),
                    html.Div(style={'flex': 1, 'height': '6px', 'background': 'rgba(0,0,0,0.04)'}, children=[
                        html.Div(style={'width': f"{f_pct}%" if f_v >=0 else f"{-f_pct}%", 'height': '100%', 'background': COLORS['fashion'] if f_v >=0 else COLORS['negative']})
                    ])
                ]),
                # Beauty row
                html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                    html.Div(f"{b_pct:.1f}%", style={'width': '40px', 'fontSize': '11px', 'fontWeight': '700', 'color': COLORS['beauty'], 'textAlign': 'right', 'marginRight': '12px'}),
                    html.Div(style={'flex': 1, 'height': '6px', 'background': 'rgba(0,0,0,0.04)'}, children=[
                        html.Div(style={'width': f"{b_pct}%" if b_v >=0 else f"{-b_pct}%", 'height': '100%', 'background': COLORS['beauty'] if b_v >=0 else COLORS['negative']})
                    ])
                ])
            ])
        ])

    return html.Div(style={'margin': '40px 0'}, children=[
        _step('Gross Profit', f_gp, b_gp),
        _step('- Fulfilment', f_log, b_log),
        _step('- Marketing & S&D', f_mkt, b_mkt),
        _step('Contribution', f_cm, b_cm),
        _step('- Other Expenses', f_oth, b_oth),
        _step('EBITDA', f_ebitda, b_ebitda),
    ])"""
code = re.sub(r"def create_100_rupee_flow.*?return html.Div\([^)]+\)\]\)", new_flow, code, flags=re.DOTALL)

# 3. gap_plot: Remove redundant legend code (already handled by get_chart_layout override)
# Make the line extremely thin (1px) and dots elegant
code = code.replace("width=4", "width=1") # thinner connection line
code = code.replace("size=16", "size=12") # balanced marker sizes
code = code.replace("size=12, weight='bold'", "size=11, weight='bold'") 

# 4. trend_chart: Remove gridlines completely, add direct text labeling to endpoints
# Wait, trend_chart currently has yaxis=dict(showgrid=True...)
# Let's override it cleanly
new_trend = """def trend_chart(x_labels, y_fashion, y_beauty, title, y_suffix='', annotate_gap=False):
    fig = go.Figure()
    
    # Text labels for start and end only to reduce clutter
    f_text = [f"{v:.1f}{y_suffix}" if i in (0, len(y_fashion)-1) else "" for i, v in enumerate(y_fashion)]
    b_text = [f"{v:.1f}{y_suffix}" if i in (0, len(y_beauty)-1) else "" for i, v in enumerate(y_beauty)]
    
    fig.add_trace(go.Scatter(
        x=x_labels, y=y_fashion, name='Fashion',
        mode='lines+markers+text', line=dict(color=COLORS['fashion'], width=3),
        marker=dict(size=8), text=f_text, textposition="top center", textfont=dict(color=COLORS['fashion'], weight='bold')
    ))
    fig.add_trace(go.Scatter(
        x=x_labels, y=y_beauty, name='Beauty',
        mode='lines+markers+text', line=dict(color=COLORS['beauty'], width=3),
        marker=dict(size=8), text=b_text, textposition="bottom center", textfont=dict(color=COLORS['beauty'], weight='bold')
    ))

    if annotate_gap and y_fashion[-1] is not None and y_beauty[-1] is not None:
        gap = y_fashion[-1] - y_beauty[-1]
        fig.add_annotation(
            x=x_labels[-1], y=(y_fashion[-1] + y_beauty[-1])/2,
            text=f"{'▲' if gap>0 else '▼'} {abs(gap):.1f} Gap",
            showarrow=False, xshift=45,
            font=dict(size=12, color=COLORS['charcoal'], weight='bold')
        )

    fig.update_layout(**get_chart_layout(
        title=dict(text=title, font=dict(size=16, weight='bold')),
        height=320,
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False), # Kill Y axis
        margin=dict(r=80, l=10, t=40, b=20) # leave room for gap annotation
    ))
    return fig"""
code = re.sub(r"def trend_chart.*?return fig", new_trend, code, flags=re.DOTALL)

with open('/run/media/ravid/New Volume/mrv/dashboard/components.py', 'w') as f:
    f.write(code)

print("Components updated.")
