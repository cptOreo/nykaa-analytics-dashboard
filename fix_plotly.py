import re

with open('components.py', 'r') as f:
    content = f.read()

# Add hoverinfo='skip' to trend_chart
content = content.replace("mode='lines+markers+text'", "mode='lines+markers+text', hoverinfo='skip'")

# Replace gap annotation arrows
content = content.replace("f\"{'▲' if gap>0 else '▼'} {abs(gap):.1f} Gap\"", "f\"+{abs(gap):.1f}pts\" if gap>0 else f\"-{abs(gap):.1f}pts\"")

# Add config={'displayModeBar': False} to chart_card
# chart_card takes a chart_component which is already a dcc.Graph... wait, chart_card takes dcc.Graph. 
# We need to modify app.py where dcc.Graph is called.

with open('components.py', 'w') as f:
    f.write(content)

with open('app.py', 'r') as f:
    app_content = f.read()

app_content = app_content.replace("dcc.Graph(", "dcc.Graph(config={'displayModeBar': False}, ")
# Also remove the Returns table header
app_content = re.sub(r"html\.Thead.*?,\s*html\.Tbody", "html.Tbody", app_content, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(app_content)
