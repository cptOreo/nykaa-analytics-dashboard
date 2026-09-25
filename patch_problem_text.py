import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

old_text = '"Nykaa has not matched Beauty\\'s EBITDA margins in Fashion, despite Fashion being in the market for ~8 years and operating with a broadly similar platform model."'
new_text = '"Nykaa hasn’t been able to match Beauty’s EBITDA margins in Fashion, despite running a similar business model, and operating in the market for eight years."'

code = code.replace(old_text, new_text)

with open(app_path, 'w') as f:
    f.write(code)

print("Problem statement text updated.")
