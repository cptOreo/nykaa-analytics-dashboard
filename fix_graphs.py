import re
app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

# Remove the trailing `, config={'displayModeBar': False}` everywhere
code = re.sub(r",\s*config=\{'displayModeBar': False\}\s*", "", code)

with open(app_path, 'w') as f:
    f.write(code)

print("Graphs fixed.")
