# content.py
# NYKAA EDITORIAL DATA JOURNALISM COPY SYSTEM

def get_hero_copy(f_nsv, year, f_ebitda, b_ebitda):
    """Dynamic copy for Section 1: The Gap"""
    gap = b_ebitda - f_ebitda
    return {
        'title': "FASHION IS GROWING. THE ECONOMICS ARE DIFFERENT.",
        'subtitle': "Fashion has expanded meaningfully, but its economics remain structurally different from Beauty.",
        'body': f"Fashion keeps less of every ₹100 of NSV. Despite scaling to ₹{f_nsv:,.0f} Cr in {year}, Fashion's EBITDA margin sits {gap*100:.1f} points below Beauty. The gap starts before EBITDA — and widens as fulfilment and commercial costs accumulate."
    }

def get_kpi_copy():
    """Microcopy for KPI cards"""
    return {
        'EBITDA Margin %': {'title': "EBITDA margin", 'subtitle': "What survives after all operations"},
        'Contribution Margin %': {'title': "Contribution margin", 'subtitle': "₹ retained per ₹100 of NSV before other expenses"},
        'Realisation %': {'title': "Realisation", 'subtitle': "How much GMV becomes NSV"},
        'Gross Margin %': {'title': "Gross margin", 'subtitle': "What remains after product cost"},
        'Marketing + S&D %': {'title': "Commercial spend", 'subtitle': "Marketing + selling costs as % of NSV"},
        'Fulfilment %': {'title': "Fulfilment burden", 'subtitle': "Cost to get the order through the system"},
        'Orders per Customer': {'title': "Orders per customer", 'subtitle': "Average annual order frequency"},
        'NSV CAGR': {'title': "Growth trajectory", 'subtitle': "3-year compound annual growth rate of NSV"},
        
        'CAC Proxy': {'title': "CAC proxy", 'subtitle': "Marketing + S&D ÷ transacting customers (blended)"},
        'Logistics Cost per Order': {'title': "Cost per order", 'subtitle': "Fulfilment cost per order"},
        'Contribution per Order': {'title': "Order contribution", 'subtitle': "Profit retained per transaction"},
        'Break-even Volume': {'title': "Break-even orders", 'subtitle': "Modelled orders needed to cover other expenses"},
        'Owned Brand Share %': {'title': "Owned brand share", 'subtitle': "Private-label GMV ÷ Total GMV"}
    }

def get_section_headers():
    return {
        1: ("01 — PROBLEM STATEMENT", "The fundamental margin divergence"),
        2: ("02 — INDUSTRY KPIs", "Following ₹100 of Net Sales Value"),
        3: ("03 — MARKETING KPIs", "Customer economics and order frequency"),
        4: ("04 — ANALYSIS", "Why Fashion's EBITDA is lower"),
        5: ("05 — PROPOSITIONS", "What the numbers point to")
    }

def get_analysis_copy():
    return {
        'waterfall_title': "THE PROFIT GAP DOESN'T START AT EBITDA",
        'waterfall_sub': "By the time Fashion reaches EBITDA, the gap has already opened across realisation, fulfilment, and commercial spend.",
        'cost_title': "WHERE DOES ₹100 OF NSV GO?",
        'cost_sub': "Start with ₹100 of net sales value. Follow what remains after gross profit, fulfilment and commercial spend.",
        'scatter_title': "GROWTH IS REAL. THE QUESTION IS WHAT IT IS WORTH.",
        'scatter_sub': "Comparing NSV growth against contribution margin across segments.",
        'owned_title': "THE OWNED-BRAND RETREAT",
        'owned_sub': "Fashion's private-label GMV declined while Beauty's surged, weakening margin control.",
        'scenario_title': "HOW MANY ORDERS DOES IT TAKE TO BREAK EVEN?",
        'scenario_sub': "The answer changes when contribution per order changes. (Scenario Model)"
    }
