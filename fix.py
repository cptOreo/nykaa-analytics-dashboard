with open('components.py', 'r') as f:
    content = f.read()
content = content.replace('f"x{row if row > 1 else } domain"', 'f"x{row if row > 1 else \'\'} domain"')
content = content.replace('f"y{row if row > 1 else } domain"', 'f"y{row if row > 1 else \'\'} domain"')
with open('components.py', 'w') as f:
    f.write(content)
