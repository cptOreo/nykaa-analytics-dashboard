import re

with open('app.py', 'r') as f:
    content = f.read()

new_func = """def build_page_returns(df):
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
            c.synthetic_data_banner(),
            c.annotation_box("Fashion's higher return rate correlates with a wider cost burden. Size and fit drive 40% of returns.")
        ]),
        html.Div(className='main-column', children=[
            html.Div("Returns extend the order lifecycle", className='editorial-statement'),
            html.Div("Order economics continue post-checkout for the Fashion segment.", className='editorial-substatement'),
            html.Div(className='hairline-top', children=[
                html.Table(className='returns-table', style={'width': '100%'}, children=[
                    html.Thead(html.Tr([html.Th("RANK", style={'width': '40px'}), html.Th("FASHION RETURN REASON"), html.Th("SHARE", style={'textAlign': 'right', 'paddingRight': '0'})])),
                    html.Tbody(rows)
                ])
            ])
        ])
    ])"""

# Replace the old function
# Using regex to match from def build_page_returns(df): to the end of the function (before # ─── 06 ACQUISITION)
pattern = re.compile(r"def build_page_returns\(df\):.*?# ─── 06 ACQUISITION ───", re.DOTALL)
content = pattern.sub(new_func + "\n\n# ─── 06 ACQUISITION ───", content)

with open('app.py', 'w') as f:
    f.write(content)
