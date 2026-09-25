import re

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
with open(app_path, 'r') as f:
    code = f.read()

# I will find tooltip='...' and move it to the end of the line before the closing ) or ,
# Actually, since there are only a few, I can explicitly replace them.

reps = {
    "kpi_card('EBITDA MARGIN', tooltip='EBITDA ÷ Net Sales Value (NSV)',": "kpi_card('EBITDA MARGIN',",
    "prev_gap=_gap_prev('EBITDA Margin %'), higher_is_better=True)": "prev_gap=_gap_prev('EBITDA Margin %'), higher_is_better=True, tooltip='EBITDA ÷ Net Sales Value (NSV)')",

    "kpi_card('CONTRIBUTION MARGIN', tooltip='Gross Profit minus Fulfilment and Marketing, divided by NSV',": "kpi_card('CONTRIBUTION MARGIN',",
    "prev_gap=_gap_prev('Contribution Margin %'), higher_is_better=True)": "prev_gap=_gap_prev('Contribution Margin %'), higher_is_better=True, tooltip='Gross Profit minus Fulfilment and Marketing, divided by NSV')",

    "kpi_card('NSV ÷ GMV (REALISATION)', tooltip='Net Sales Value ÷ Gross Merchandise Value. Measures value lost to cancellations, returns, and discounts.',": "kpi_card('NSV ÷ GMV (REALISATION)',",
    "prev_gap=_gap_prev('Realisation %'), higher_is_better=True)": "prev_gap=_gap_prev('Realisation %'), higher_is_better=True, tooltip='Net Sales Value ÷ Gross Merchandise Value. Measures value lost to cancellations, returns, and discounts.')",

    "kpi_card('LOGISTICS / ORDER', tooltip='Fulfilment Expense ÷ Total Orders',": "kpi_card('LOGISTICS / ORDER',",
    "prev_gap=_gap_prev('Logistics Cost per Order'), higher_is_better=False)": "prev_gap=_gap_prev('Logistics Cost per Order'), higher_is_better=False, tooltip='Fulfilment Expense ÷ Total Orders')",
    
    "kpi_card('MARKETING / ORDER', tooltip='Marketing & Selling Expense ÷ Total Orders',": "kpi_card('MARKETING / ORDER',",
    "prev_gap=_gap_prev('Marketing + S&D per Order'), higher_is_better=False)": "prev_gap=_gap_prev('Marketing + S&D per Order'), higher_is_better=False, tooltip='Marketing & Selling Expense ÷ Total Orders')",

    "kpi_card('CAC PROXY', tooltip='Marketing + S&D Expense ÷ Annual Unique Transacting Customers',": "kpi_card('CAC PROXY',",
    "prev_gap=_gap_prev('CAC Proxy'), higher_is_better=False)": "prev_gap=_gap_prev('CAC Proxy'), higher_is_better=False, tooltip='Marketing + S&D Expense ÷ Annual Unique Transacting Customers')",

    "kpi_card('BREAK-EVEN VOLUME', tooltip='Fixed & Other Expenses ÷ Contribution Profit per Order', _safe(fk.get('Break-even Volume'), 0) / 1e6 if _safe(fk.get('Break-even Volume')) else None,": "kpi_card('BREAK-EVEN VOLUME', _safe(fk.get('Break-even Volume'), 0) / 1e6 if _safe(fk.get('Break-even Volume')) else None,",
    "_safe(bk.get('Break-even Volume'), 0) / 1e6 if _safe(bk.get('Break-even Volume')) else None, formatter=fmt_number, higher_is_better=False)": "_safe(bk.get('Break-even Volume'), 0) / 1e6 if _safe(bk.get('Break-even Volume')) else None, formatter=fmt_number, higher_is_better=False, tooltip='Fixed & Other Expenses ÷ Contribution Profit per Order')",

    "kpi_card('BREAK-EVEN VOLUME', tooltip='Fixed & Other Expenses ÷ Contribution Profit per Order',\\n": "kpi_card('BREAK-EVEN VOLUME',\\n",
    "gap_label='Gap', higher_is_better=False)\\n": "gap_label='Gap', higher_is_better=False, tooltip='Fixed & Other Expenses ÷ Contribution Profit per Order')\\n"
}

for k, v in reps.items():
    code = code.replace(k, v)

# wait, line 851 Break-even volume might be formatted slightly differently.
# I'll just use regex to clean up any remaining `kpi_card('TITLE', tooltip='...', val1, val2)`
code = re.sub(
    r"kpi_card\((['\"][^'\"]+['\"]),\s*tooltip=('[^']+'),\s*([^,]+),\s*([^,]+)(.*?)\)",
    r"kpi_card(\1, \3, \4\5, tooltip=\2)",
    code, flags=re.DOTALL
)

with open(app_path, 'w') as f:
    f.write(code)

