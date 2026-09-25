with open('/run/media/ravid/New Volume/mrv/dashboard/app.py', 'r') as f:
    code = f.read()

# Remove all instances of the main block
import re
code = re.sub(r"if __name__ == '__main__':\s+app.run\(host=[\"']0\.0\.0\.0[\"'], port=8050, debug=False\)", "", code)
code = re.sub(r"if __name__ == '__main__':\s+app.run_server\(debug=False, port=8050\)", "", code)

# Append it to the very end
code += "\n\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=8050, debug=False)\n"

with open('/run/media/ravid/New Volume/mrv/dashboard/app.py', 'w') as f:
    f.write(code)

print("Fixed main block location")
