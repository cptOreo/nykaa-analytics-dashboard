with open('assets/styles.css', 'r') as f:
    css = f.read()

css = css.replace('.Select-control { border: none !important; border-bottom: 1px solid var(--border-color) !important; background: transparent !important; font-weight: 700 !important; font-size: 13px !important; color: var(--text-charcoal) !important; cursor: pointer; min-height: 30px !important; height: 30px !important; }',
                  '.Select-control { border: none !important; border-bottom: 2px solid var(--border-color) !important; background: transparent !important; font-weight: 900 !important; font-size: 14px !important; color: var(--text-charcoal) !important; cursor: pointer; min-height: 24px !important; height: 24px !important; box-shadow: none !important; border-radius: 0 !important; }')
css += "\n.Select-arrow { display: none !important; }\n"
css += ".Select-value-label { color: var(--text-charcoal) !important; }\n"

with open('assets/styles.css', 'w') as f:
    f.write(css)
