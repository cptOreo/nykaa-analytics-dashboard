import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

url_callbacks = """
import urllib.parse

@callback(
    Output('url', 'search'),
    Input('year-filter', 'value'),
    State('url', 'search')
)
def update_url_search(year, current_search):
    if not year:
        return dash.no_update
        
    current_params = urllib.parse.parse_qs(current_search.lstrip('?')) if current_search else {}
    if current_params.get('year', [None])[0] == year:
        return dash.no_update
        
    current_params['year'] = [year]
    return '?' + urllib.parse.urlencode(current_params, doseq=True)

@callback(
    Output('year-filter', 'value'),
    Input('url', 'search'),
    State('year-filter', 'value')
)
def load_state_from_url(search, current_year):
    if not search:
        return dash.no_update
    params = urllib.parse.parse_qs(search.lstrip('?'))
    url_year = params.get('year', [None])[0]
    
    if url_year and url_year != current_year and url_year in ['FY22','FY23','FY24','FY25','FY26']:
        return url_year
        
    return dash.no_update

@callback(Output('page-content', 'children'),"""

code = code.replace("@callback(Output('page-content', 'children'),", url_callbacks)

with open(app_path, 'w') as f:
    f.write(code)

print("URL state synced.")
