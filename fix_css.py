with open('assets/styles.css', 'r') as f:
    css = f.read()

# Masthead redesign
css = css.replace('.editorial-nav { height: var(--nav-height); background-color: var(--bg-color); border-bottom: 1px solid var(--border-color); display: flex; align-items: center; padding: 0 40px; z-index: 1000; flex-shrink: 0; }', 
                  '.editorial-nav { padding: 32px 40px 16px 40px; background-color: var(--bg-color); border-bottom: 2px solid var(--border-color); display: flex; align-items: flex-end; z-index: 1000; flex-shrink: 0; }')
css = css.replace('.nav-brand { font-family: \'Inter\', sans-serif; font-weight: 900; font-size: 14px; letter-spacing: -0.5px; margin-right: 40px; }',
                  '.nav-brand { font-family: \'Playfair Display\', serif; font-weight: 900; font-size: 48px; line-height: 0.8; letter-spacing: -2px; margin-right: 60px; text-transform: uppercase; }')

# Annotation Redesign (Remove pink border, add pilcrow behavior using ::before if we want, or just rely on italic)
css = css.replace('.annotation-box { font-family: \'Playfair Display\', serif; font-size: 18px; font-style: italic; line-height: 1.3; color: var(--text-charcoal); padding-left: 16px; border-left: 3px solid var(--nykaa-pink); }',
                  '.annotation-box { font-family: \'Playfair Display\', serif; font-size: 20px; font-style: italic; line-height: 1.3; color: var(--text-charcoal); }')

# Scale the giant numbers
css = css.replace('.giant-number { font-size: 72px; font-weight: 900; line-height: 0.9; letter-spacing: -2px; }',
                  '.giant-number { font-size: 80px; font-weight: 900; line-height: 0.9; letter-spacing: -3px; }\n.giant-number-secondary { font-size: 48px; font-weight: 900; line-height: 0.9; letter-spacing: -1.5px; }\n.giant-number-tertiary { font-size: 32px; font-weight: 900; line-height: 0.9; letter-spacing: -1px; }')

# Varying grid layouts
css += "\n.full-width-column { display: flex; flex-direction: column; gap: 40px; max-width: 1400px; margin: 0 auto; padding: 40px; }\n"

# Footnote style
css += "\n.editorial-footnote { font-family: 'Inter', sans-serif; font-size: 9px; font-weight: 600; text-transform: uppercase; color: var(--text-muted); border-top: 1px solid var(--border-light); padding-top: 8px; margin-top: auto; }\n"

with open('assets/styles.css', 'w') as f:
    f.write(css)
