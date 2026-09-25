import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

# Replace any existing config={...} with the new export-friendly config
old_config = "config={'displayModeBar': False}"
new_config = "config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d'], 'toImageButtonOptions': {'format': 'png', 'filename': 'nykaa_export'}}"
code = code.replace(old_config, new_config)

# There are also some plain dcc.Graph(figure=xxx) without config.
# I will use a regex to inject config into them.
# Match: dcc.Graph(figure=some_var)
code = re.sub(r"dcc\.Graph\(figure=([a-zA-Z0-9_]+)\)", r"dcc.Graph(figure=\1, " + new_config + ")", code)
# Also Match: dcc.Graph(figure=trend_chart(...), y_suffix='') which is multi-line? No, they might be nested.
# Actually, if I just replace "figure=trend_chart" and so on...
# It's easier to just use components.py to globally set it, but dash doesn't support that.

with open(app_path, 'w') as f:
    f.write(code)

print("Graphs patched.")
