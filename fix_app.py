import re

with open('app.py', 'r') as f:
    app = f.read()

# Make Profitability full-width
profitability_old = """return html.Div(className='editorial-grid', children=[
        html.Div(className='margin-column', children=[
            c.methodology_badge('02', txt.BADGE_DERIVED),
            c.kpi_card("NSV to GP", _safe(fk.get('Gross Margin')), _safe(bk.get('Gross Margin'))),
            c.kpi_card("NSV to CM", _safe(fk.get('Contribution Margin')), _safe(bk.get('Contribution Margin'))),
            c.kpi_card("NSV to EBITDA", _safe(fk.get('EBITDA Margin')), _safe(bk.get('EBITDA Margin'))),
            c.annotation_box("Beauty commands an EBITDA margin above 9%, whilst Fashion loses money after fulfilment and marketing.")
        ]),
        html.Div(className='main-column', children=[
            html.Div("Where the money goes", className='editorial-statement'),
            html.Div("Tracing ₹100 of Net Sales Value down the P&L for FY26.", className='editorial-substatement'),
            html.Div(className='hairline-top', style={'marginTop': '20px'}, children=[
                c.create_100_rupee_flow(
                    f_nsv=1447, b_nsv=8504,
                    f_gp=692, b_gp=3801,
                    f_log=162, b_log=794,
                    f_mkt=382, b_mkt=1092,
                    f_cm=147, b_cm=1916,
                    f_oth=185, b_oth=1097,
                    f_ebitda=-37, b_ebitda=819
                )
            ])
        ])
    ])"""

profitability_new = """return html.Div(className='full-width-column', children=[
        html.Div(children=[
            html.Div("02 PROFITABILITY", style={'fontSize': '9px', 'fontWeight': '800', 'color': 'var(--text-muted)', 'marginBottom': '16px'}),
            html.Div("Where the money goes", className='editorial-statement'),
            html.Div("Tracing ₹100 of Net Sales Value down the P&L for FY26. Beauty commands an EBITDA margin above 9%, whilst Fashion loses money after fulfilment and marketing.", className='editorial-substatement', style={'maxWidth': '1000px', 'fontSize': '20px'}),
        ]),
        html.Div(className='hairline-top', style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '40px'}, children=[
            c.kpi_card("NSV to GP", _safe(fk.get('Gross Margin')), _safe(bk.get('Gross Margin'))),
            c.kpi_card("NSV to CM", _safe(fk.get('Contribution Margin')), _safe(bk.get('Contribution Margin'))),
            c.kpi_card("NSV to EBITDA", _safe(fk.get('EBITDA Margin')), _safe(bk.get('EBITDA Margin')))
        ]),
        html.Div(className='hairline-top', children=[
            c.create_100_rupee_flow(
                f_nsv=1447, b_nsv=8504,
                f_gp=692, b_gp=3801,
                f_log=162, b_log=794,
                f_mkt=382, b_mkt=1092,
                f_cm=147, b_cm=1916,
                f_oth=185, b_oth=1097,
                f_ebitda=-37, b_ebitda=819
            )
        ])
    ])"""

app = app.replace(profitability_old, profitability_new)

# Fix Giant Numbers in Acquisition (Make them secondary)
app = app.replace("className='giant-number fashion'", "className='giant-number-secondary fashion'")
app = app.replace("className='giant-number beauty'", "className='giant-number-secondary beauty'")

# Move synthetic data banner to footer in page 1
# Remove from margin column
app = app.replace("c.synthetic_data_banner(),\n            ", "")
# Append to main-column
app = re.sub(r"(c\.annotation_box\(\"Returns cut Fashion's GMV.*?\]\))", r"\1,\n            html.Div('RESEARCH, SYNTHETIC PRIMARY RESEARCH DATA (PLACEHOLDER FOR PROTOTYPING)', className='editorial-footnote')", app, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(app)
