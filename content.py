# content.py
# Stop-slop editorial copy, methodology notes, and dynamic text generators.

NAV_ITEMS = [
    ('/', '01', 'THE GAP'),
    ('/where-money-goes', '02', 'PROFITABILITY'),
    ('/growth', '03', 'GROWTH'),
    ('/customer', '04', 'CUSTOMER'),
    ('/returns', '05', 'RETURNS'),
    ('/acquisition', '06', 'ACQUISITION'),
    ('/scenarios', '07', 'SCENARIOS'),
    ('/propositions', '08', 'PROPOSITIONS'),
]

TOOLTIPS = {
    'realisation': "NSV ÷ GMV. Shows the portion of gross merchandise value converting into net sales value.",
    'cpo': "Fulfilment Expense ÷ Orders. A broader fulfilment cost metric than last-mile delivery.",
    'opc': "Orders ÷ annual unique transacting customers. Acts as a purchase frequency proxy.",
    'cac_proxy': "Marketing + S&D ÷ annual unique transacting customers. Proxy only; true Fashion-only new customer acquisition cost is unpublished.",
    'break_even': "Other Expenses ÷ Contribution per Order. A modelled break-even proxy, not an accounting break-even calculation.",
    'cm': "Contribution Profit ÷ NSV. Profit remaining before allocating central overheads.",
    'marketing': "Marketing + S&D ÷ NSV. The commercial cost of generating sales."
}

BADGE_FINANCIAL = "DATA, Company financial data"
BADGE_SYNTHETIC = "RESEARCH, Synthetic primary research data (placeholder for prototyping)"
BADGE_DERIVED = "METHOD, Derived metrics calculated from the displayed financial inputs"
BADGE_MODEL = "METHOD, Scenario model based on contribution per order"

def p1_gap_substatement():
    return "Fashion expanded revenue while maintaining different unit economics from Beauty."

def p1_gap_implication():
    return "The gap surfaces across realisation, selling costs, fulfilment, and repeat behavior."

def p1_dynamic_gap(f_eb, b_eb):
    if f_eb is None or b_eb is None: return "Data missing for this period."
    gap = abs(f_eb - b_eb)
    return f"Fashion's {f_eb:.1f}% EBITDA margin trails Beauty by {gap:.1f} points."

def p2_dynamic_commercial(f_mkt, b_mkt):
    if f_mkt is None or b_mkt is None: return "Data missing."
    return f"Commercial spend takes {f_mkt:.1f}% of Fashion NSV, double the {b_mkt:.1f}% Beauty spends."

def p3_dynamic_growth(year, f_cm, f_mkt):
    if f_cm is None or f_mkt is None: return "Data missing."
    return f"Fashion reached a {f_cm:.1f}% contribution margin in {year} alongside a {f_mkt:.1f}% commercial spend on NSV."

def p4_dynamic_frequency(f_opc, b_opc):
    if f_opc is None or b_opc is None: return "Data missing."
    return f"Beauty customers place {b_opc:.1f} orders per year, compared to {f_opc:.1f} in Fashion."

def p7_dynamic_scenario(cpo, orders, bev):
    return f"The model requires {bev/1e6:.1f} million orders to cover other expenses given a ₹{cpo:,.0f} contribution per order."

PROPOSITIONS = [
    {
        "observation": "Fashion customers place fewer orders than Beauty customers.",
        "question": "Does post-purchase engagement or assortment depth drive repeat purchasing?",
        "direction": "Test interventions targeting replenishment behavior."
    },
    {
        "observation": "Returns reduce net realisation.",
        "question": "Is sizing or discovery behavior driving returns?",
        "direction": "Investigate fit prediction technology and restrict high return brands."
    },
    {
        "observation": "Acquisition proxies show a high commercial cost per transacting customer.",
        "question": "Will organic discovery offset paid acquisition over a multi year horizon?",
        "direction": "Evaluate community led growth against direct response spend limits."
    }
]
