import re

with open('/run/media/ravid/New Volume/mrv/dashboard/components.py', 'r') as f:
    code = f.read()

# Update kpi_card signature and layout
old_kpi = r"def kpi_card\(label, f_val, b_val, formatter=fmt_pct, tooltip=None\):.*?return html\.Div\(children, className='kpi-item'\)"

new_kpi = """def kpi_card(label, f_val, b_val, formatter=fmt_pct, tooltip=None, subtitle=None):
    fd = formatter(f_val)
    bd = formatter(b_val)
    gap = None
    if f_val is not None and b_val is not None:
        try: gap = f_val - b_val
        except: gap = None
    
    label_el = [html.Span(label)]
    if tooltip:
        label_el.append(html.Span("ⓘ", className='tooltip-icon', title=tooltip))

    children = [
        html.Div(label_el, className='kpi-label'),
    ]
    if subtitle:
        children.append(html.Div(subtitle, style={'fontSize': '11px', 'color': 'var(--text-muted)', 'marginBottom': '12px', 'lineHeight': '1.3'}))
        
    children.extend([
        html.Div([
            html.Span('FASHION', className='kpi-seg fashion'),
            html.Span(fd, className='kpi-val')
        ], className='kpi-row'),
        html.Div([
            html.Span('BEAUTY', className='kpi-seg beauty'),
            html.Span(bd, className='kpi-val')
        ], className='kpi-row')
    ])
    if gap is not None:
        children.append(html.Div(f"{'▼' if gap < 0 else '▲'} {abs(gap):.1f} Gap", className='kpi-gap'))
    
    return html.Div(children, className='kpi-item')"""

code = re.sub(old_kpi, new_kpi, code, flags=re.DOTALL)

# Update synthetic_data_banner
code = code.replace("def synthetic_data_banner():\n    return html.Div(\"SYNTHETIC PRIMARY-RESEARCH DATA (PLACEHOLDER)\", className='synthetic-warning')", 
                    "def synthetic_data_banner():\n    return html.Div(\"RESEARCH — Synthetic primary-research data (placeholder for prototyping)\", className='chart-source')")

with open('/run/media/ravid/New Volume/mrv/dashboard/components.py', 'w') as f:
    f.write(code)

print("components copy updated")
