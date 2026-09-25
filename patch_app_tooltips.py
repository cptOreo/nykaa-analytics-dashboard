import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

reps = {
    "kpi_card('EBITDA MARGIN',": "kpi_card('EBITDA MARGIN', tooltip='EBITDA ÷ Net Sales Value (NSV)',",
    "kpi_card('CONTRIBUTION MARGIN',": "kpi_card('CONTRIBUTION MARGIN', tooltip='Gross Profit minus Fulfilment and Marketing, divided by NSV',",
    "kpi_card('NSV ÷ GMV (REALISATION)',": "kpi_card('NSV ÷ GMV (REALISATION)', tooltip='Net Sales Value ÷ Gross Merchandise Value. Measures value lost to cancellations, returns, and discounts.',",
    "kpi_card('CAC PROXY',": "kpi_card('CAC PROXY', tooltip='Marketing + S&D Expense ÷ Annual Unique Transacting Customers',",
    "kpi_card('LOGISTICS / ORDER',": "kpi_card('LOGISTICS / ORDER', tooltip='Fulfilment Expense ÷ Total Orders',",
    "kpi_card('MARKETING / ORDER',": "kpi_card('MARKETING / ORDER', tooltip='Marketing & Selling Expense ÷ Total Orders',",
    "kpi_card('BREAK-EVEN VOLUME',": "kpi_card('BREAK-EVEN VOLUME', tooltip='Fixed & Other Expenses ÷ Contribution Profit per Order',",
}

for k, v in reps.items():
    code = code.replace(k, v)

with open(app_path, 'w') as f:
    f.write(code)

print("Tooltips added.")
