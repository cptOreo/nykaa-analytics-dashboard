import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

old_str = "html.Div(className='page-body', children=["
new_str = """html.Div(className='page-body', children=[
            insight_panel(
                'THE BUSINESS PROBLEM',
                "Nykaa has not matched Beauty's EBITDA margins in Fashion, despite Fashion being in the market for ~8 years and operating with a broadly similar platform model."
            ),"""

code = code.replace(old_str, new_str)

with open(app_path, 'w') as f:
    f.write(code)

print("Problem statement added.")
