import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

# Using regex to find the string regardless of exact escaping
code = re.sub(
    r'"Nykaa has not matched Beauty[^"]+"',
    '"Nykaa hasn’t been able to match Beauty’s EBITDA margins in Fashion, despite running a similar business model, and operating in the market for eight years."',
    code
)

with open(app_path, 'w') as f:
    f.write(code)

print("Problem statement text updated.")
