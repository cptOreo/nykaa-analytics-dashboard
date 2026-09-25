import re

with open('/run/media/ravid/New Volume/mrv/dashboard/components.py', 'r') as f:
    code = f.read()

# Replace the labels in create_100_rupee_flow
old_flow_section = """    return html.Div(style={'margin': '40px 0'}, children=[
        _step('Gross Profit', 'what remains after product cost', f_gp, b_gp),
        _step('Fulfilment', 'the cost to get the order through', f_log, b_log),
        _step('Commercial Spend', 'the cost of selling it', f_mkt, b_mkt),
        _step('Contribution', 'what remains before other expenses', f_cm, b_cm),
        _step('Other Expenses', 'everything still sitting above EBITDA', f_oth, b_oth),
        _step('EBITDA', 'what survives', f_ebitda, b_ebitda),
    ])"""

new_flow_section = """    return html.Div(style={'margin': '40px 0'}, children=[
        _step('Gross Profit', 'Capital after product cost', f_gp, b_gp),
        _step('Fulfilment', 'Cost of processing the order', f_log, b_log),
        _step('Commercial Spend', 'Cost of selling', f_mkt, b_mkt),
        _step('Contribution', 'Capital before other expenses', f_cm, b_cm),
        _step('Other Expenses', 'Overhead costs above EBITDA', f_oth, b_oth),
        _step('EBITDA', 'Capital surviving', f_ebitda, b_ebitda),
    ])"""

code = code.replace(old_flow_section, new_flow_section)

with open('/run/media/ravid/New Volume/mrv/dashboard/components.py', 'w') as f:
    f.write(code)

print("components copy updated for stop-slop")
