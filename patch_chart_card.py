import re

comp_path = '/run/media/ravid/New Volume/mrv/dashboard/components.py'
with open(comp_path, 'r') as f:
    code = f.read()

old_func = "def chart_card(chart_component, title='', subtitle='', source='', full_width=False):\\n    \"\"\"Wraps a chart in a styled card container.\"\"\"\\n    children = []"
new_func = """def chart_card(chart_component, title='', subtitle='', source='', full_width=False):
    \"\"\"Wraps a chart in a styled card container.\"\"\"
    # Inject Export capability
    export_config = {
        'displayModeBar': True, 'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'toImageButtonOptions': {'format': 'png', 'filename': 'nykaa_chart_export'}
    }
    if hasattr(chart_component, 'config'):
        if isinstance(chart_component.config, dict):
            chart_component.config.update(export_config)
        else:
            chart_component.config = export_config
    else:
        chart_component.config = export_config

    children = []"""

code = code.replace(old_func, new_func)

with open(comp_path, 'w') as f:
    f.write(code)

print("Export capability injected via chart_card.")
