import re

comp_path = '/run/media/ravid/New Volume/mrv/dashboard/components.py'
with open(comp_path, 'r') as f:
    content = f.read()

old_label = "html.Div(label, className='kpi-card-label', title=tooltip or ''),"
new_label = """html.Div(
            [label, html.Span(" ⓘ", style={'fontSize': '0.9em', 'opacity': '0.6', 'cursor': 'help'})] if tooltip else label,
            className='kpi-card-label',
            title=tooltip or ''
        ),"""

content = content.replace(old_label, new_label)

with open(comp_path, 'w') as f:
    f.write(content)

print("Tooltip patched.")
