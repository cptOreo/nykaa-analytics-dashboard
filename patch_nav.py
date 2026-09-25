import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    content = f.read()

new_callback = """
@callback(
    [Output(f'nav-{href.strip("/") or "home"}', 'className') for href, _, _ in NAV_ITEMS],
    Input('url', 'pathname')
)
def update_active_links(pathname):
    if pathname is None:
        pathname = '/'
    
    classes = []
    for href, _, _ in NAV_ITEMS:
        # Match exact path, or root
        if pathname == href:
            classes.append('nav-link active')
        else:
            classes.append('nav-link')
    return classes

@callback(Output('page-content', 'children'),"""

content = content.replace("@callback(Output('page-content', 'children'),", new_callback)

with open(app_path, 'w') as f:
    f.write(content)

print("Nav patched successfully.")
