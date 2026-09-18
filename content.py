# content.py
# Editorial copy, methodology notes, and dynamic text generators.

NAV_ITEMS = [
    ('/', '01', 'THE GAP'),
    ('/where-money-goes', '02', 'WHERE THE MONEY GOES'),
    ('/growth', '03', 'THE PROFITABILITY ENGINE'),
    ('/customer', '04', 'THE CUSTOMER'),
    ('/returns', '05', 'THE RETURN JOURNEY'),
    ('/acquisition', '06', 'THE ACQUISITION LOOP'),
    ('/scenarios', '07', 'WHAT HAPPENS IF?'),
    ('/propositions', '08', 'WHERE TO LOOK NEXT'),
]

TOOLTIPS = {
    'realisation': "NSV ÷ GMV.\nShows how much gross merchandise value converts into net sales value.",
    'cpo': "Fulfilment Expense ÷ Orders.\nA broader fulfilment-cost measure, not pure last-mile delivery cost.",
    'opc': "Orders ÷ annual unique transacting customers.\nUsed here as a purchase-frequency proxy.",
    'cac_proxy': "Marketing + S&D ÷ annual unique transacting customers.\nProxy only; true Fashion-only new customer acquisition cost is not publicly disclosed.",
    'break_even': "Other Expenses ÷ Contribution per Order.\nA modelled break-even proxy, not an accounting break-even calculation.",
    'cm': "Contribution Profit ÷ NSV.\nWhat remains before allocating central overheads.",
    'marketing': "Marketing + S&D ÷ NSV.\nThe commercial cost of generating sales."
}

BADGE_FINANCIAL = "DATA — Company financial data"
BADGE_SYNTHETIC = "RESEARCH — Synthetic primary-research data (placeholder for prototyping)"
BADGE_DERIVED = "METHOD — Derived metrics calculated from the displayed financial inputs"
BADGE_MODEL = "METHOD — Scenario model based on contribution per order"

def p1_dynamic_gap(f_eb, b_eb):
    if f_eb is None or b_eb is None: return "Data missing for this period."
    gap = abs(f_eb - b_eb)
    return f"Fashion's EBITDA margin is {f_eb:.1f}%, {gap:.1f} points below Beauty."

def p2_dynamic_commercial(f_mkt, b_mkt):
    if f_mkt is None or b_mkt is None: return "Data missing."
    return f"Commercial spend absorbs {f_mkt:.1f}% of NSV—roughly twice Beauty's share."

def p3_dynamic_growth(year, f_cm, f_mkt):
    if f_cm is None or f_mkt is None: return "Data missing."
    return f"In {year}, Fashion's contribution margin reached {f_cm:.1f}%, but commercial spend absorbed {f_mkt:.1f}% of NSV."

def p4_dynamic_frequency(f_opc, b_opc):
    if f_opc is None or b_opc is None: return "Data missing."
    return f"Beauty gets {b_opc:.1f} orders from each customer annually, while Fashion sits at {f_opc:.1f}."

def p7_dynamic_scenario(cpo, orders, bev):
    return f"At ₹{cpo:,.0f} contribution per order, the model requires {bev/1e6:.1f}M orders to cover other expenses."

PROPOSITIONS = [
    {
        "observation": "Fashion's orders per customer remain structurally below Beauty.",
        "question": "What would move fashion customers from occasional to repeat purchasing?",
        "direction": "Test interventions around post-purchase engagement, assortment depth, and replenishment behaviour."
    },
    {
        "observation": "Return rates systematically suppress net realisation.",
        "question": "Which portion of returns is driven by fixable sizing versus inherent discovery behaviour?",
        "direction": "Investigate fit-prediction technology and strict curation of high-return brands."
    },
    {
        "observation": "Acquisition proxies indicate a high commercial cost per transacting customer.",
        "question": "Can organic discovery offset paid acquisition over a multi-year horizon?",
        "direction": "Evaluate community-led growth and content loops against direct-response spend limits."
    }
]

def p1_gap_substatement():
    return "Fashion has expanded meaningfully, but its economics remain structurally different from Beauty."

def p1_gap_implication():
    return "The gap becomes visible in realisation, selling costs, fulfilment and repeat behaviour."
