import re
app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

config_str = "config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d'], 'toImageButtonOptions': {'format': 'png', 'filename': 'nykaa_export'}}, figure="
code = re.sub(r"dcc\.Graph\(\s*figure=([a-zA-Z0-9_]+)\s*\)", r"dcc.Graph(figure=\1, config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d'], 'toImageButtonOptions': {'format': 'png', 'filename': 'nykaa_export'}})", code)
code = re.sub(r"dcc\.Graph\(\n\s*figure=", r"dcc.Graph(\n" + config_str, code)

with open(app_path, 'w') as f:
    f.write(code)

