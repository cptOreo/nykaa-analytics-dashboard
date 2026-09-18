import os

app_path = '/run/media/ravid/New Volume/mrv/dashboard/app.py'
comp_path = '/run/media/ravid/New Volume/mrv/dashboard/components.py'

with open(app_path, 'r') as f:
    app_code = f.read()

with open(comp_path, 'r') as f:
    comp_code = f.read()

# 1. Component Replacements
comp_reps = {
    "return '—'": "return '-'",
    "Synthetic primary-research data — placeholder": "Synthetic primary-research data: placeholder"
}
for k, v in comp_reps.items():
    comp_code = comp_code.replace(k, v)

# 2. App Replacements
app_reps = {
    # Em dashes
    " — ": " - ",
    
    # Page 1
    "'Where does Fashion lose economics relative to Beauty?'": "'Why does Fashion make less money than Beauty?'",
    "vs Beauty's {fmt_pct(b_ebitda_val)} - a gap of": "vs Beauty's {fmt_pct(b_ebitda_val)}. That is a gap of",
    "for Beauty - {abs(f_mkt - b_mkt):.1f} pts higher": "for Beauty, which is {abs(f_mkt - b_mkt):.1f} pts higher",
    "Fashion operates at a structural margin deficit compared to Beauty.": "Fashion has a structurally lower margin than Beauty.",
    "The gap primarily opens up below the gross margin line, driven by fulfilment and marketing costs.": "The gap opens up after gross margin, mostly driven by fulfilment and marketing costs.",
    "Fashion's break-even volume is significantly higher due to lower per-order contribution.": "Fashion needs much more volume to break even because it earns less per order.",

    # Page 2
    "'Fashion is not losing at gross margin - the gap emerges downstream.'": "'Fashion holds its own on gross margin. The real gap opens up later.'",
    "margin is the widest gap at {abs(gaps[2]):.1f} pts - Fashion": "margin is the widest gap at {abs(gaps[2]):.1f} pts (Fashion",
    "vs Beauty {b_margins[2]:.1f}%.\",": "vs Beauty {b_margins[2]:.1f}%).\",",

    # Page 3
    "'Comparing growth trajectories and their link to profitability.'": "'How growth impacts the bottom line.'",
    "Growth has not automatically translated into profitability - the scatter shows": "Growth doesn't automatically mean profits. The scatter plot shows",
    
    # Page 4
    "'Customer-level behaviour from survey data.'": "'Survey insights on how people buy.'",
    
    # Page 5
    "'Company-level acquisition economics and customer-level acquisition behaviour.'": "'How much it costs to acquire customers and where they come from.'",

    # Page 6
    "Size/fit and colour mismatch are the dominant Fashion return reasons - consistent with industry-wide apparel challenges.": "Size, fit, and color mismatch drive most Fashion returns, mirroring broader apparel trends.",
    "'Comparing return behaviour and its association with customer economics.'": "'How returns connect to customer spending.'",
    
    # Page 7
    "'Platform preferences, loyalty, and competitive behaviour.'": "'Where else customers shop and how loyal they are.'",

    # Page 8
    "'Break-even analysis and scenario modelling.'": "'Interactive break-even modeling.'",
    "Evidence-based hypotheses from the data - not strategic recommendations.": "Evidence-based hypotheses from the data, not strategic recommendations.",
    "Reducing Marketing + S&D intensity may have a larger contribution-margin effect than improving gross margin, given the current cost structure.": "Cutting marketing costs could boost contribution margins faster than chasing better gross margins.",
    "{_safe(fk.get('Marketing + S&D %'),0):.1f}% of NSV vs Beauty's {_safe(bk.get('Marketing + S&D %'),0):.1f}% - a {abs(_safe(fk.get('Marketing + S&D %'),0) - _safe(bk.get('Marketing + S&D %'),0)):.1f} pt gap. Gross margins are comparable.": "{_safe(fk.get('Marketing + S&D %'),0):.1f}% of NSV compared to Beauty's {_safe(bk.get('Marketing + S&D %'),0):.1f}%. Gross margins are nearly identical.",
    "Fashion's GMV → NSV leakage is a structural headwind that dwarfs gross margin differences.": "Fashion loses a massive chunk of value between GMV and NSV. This matters much more than gross margins.",
    "{_safe(fk.get('Realisation %'),0):.1f}% vs Beauty's {_safe(bk.get('Realisation %'),0):.1f}% - Fashion loses ~{100 - _safe(fk.get('Realisation %'),0):.0f}% of GMV before reaching NSV.": "{_safe(fk.get('Realisation %'),0):.1f}% vs Beauty's {_safe(bk.get('Realisation %'),0):.1f}%. Fashion drops ~{100 - _safe(fk.get('Realisation %'),0):.0f}% of GMV before it even hits net sales.",
    "Logistics cost per order is higher in Fashion, partly because higher AOV items require more complex fulfilment.": "Fashion spends more on logistics per order, likely because higher-value items need more careful handling.",
}

# Apply global fallback for em dashes
app_code = app_code.replace("—", "-")

for k, v in app_reps.items():
    app_code = app_code.replace(k, v)

with open(app_path, 'w') as f:
    f.write(app_code)

with open(comp_path, 'w') as f:
    f.write(comp_code)

print("Slop removed successfully.")
