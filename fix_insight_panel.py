import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

old_code = """insight_panel(
                'THE BUSINESS PROBLEM',
                "Nykaa hasn’t been able to match Beauty’s EBITDA margins in Fashion, despite running a similar business model, and operating in the market for eight years."
            )"""

new_code = """insight_panel(
                ["Nykaa hasn’t been able to match Beauty’s EBITDA margins in Fashion, despite running a similar business model, and operating in the market for eight years."],
                title='THE BUSINESS PROBLEM'
            )"""

code = code.replace(old_code, new_code)

with open(app_path, 'w') as f:
    f.write(code)

print("Fixed the insight_panel parameters.")
