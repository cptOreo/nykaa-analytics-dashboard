import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

old_block = """    return html.Div([
        page_header(
            'Understanding the Profitability Gap',
            'Why does Fashion make less money than Beauty?',
            'NYKAA FASHION × BEAUTY',
        ),
        html.Div(className='page-body', children=[
            html.Div(className='nykaa-edge-line'),"""

new_block = """    return html.Div([
        page_header(
            'Understanding the Profitability Gap',
            'Why does Fashion make less money than Beauty?',
            'NYKAA FASHION × BEAUTY',
        ),
        html.Div(className='page-body', children=[
            insight_panel(
                'THE BUSINESS PROBLEM',
                "Nykaa has not matched Beauty's EBITDA margins in Fashion, despite Fashion being in the market for ~8 years and operating with a broadly similar platform model."
            ),
            html.Div(className='nykaa-edge-line', style={'marginTop': '24px'}),"""

code = code.replace(old_block, new_block)

with open(app_path, 'w') as f:
    f.write(code)

print("Problem statement added to Page 1.")
