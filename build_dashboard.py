import json

# Parse contributors
with open('C:/Users/DARA-PC/contributors.txt', 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
js_rows = []
for line in lines[14:]:
    line = line.strip()
    if not line or line.startswith('Ref num') or line.startswith('Date') or line.startswith('==='):
        continue
    parts = line.split('|')
    if len(parts) < 7:
        continue
    try:
        amount = int(parts[6].strip()) if parts[6].strip() else 0
        participation = parts[7].strip() if len(parts) > 7 else ''
        row = {
            'seq': parts[0].strip(),
            'name': parts[1].strip(),
            'gender': parts[2].strip(),
            'position': parts[4].strip(),
            'section': parts[5].strip(),
            'amount': amount,
            'participation': participation
        }
        js_rows.append(json.dumps(row, ensure_ascii=False))
    except:
        pass

# Section totals
section_totals = {}
for r in js_rows:
    obj = json.loads(r)
    s = obj['section']
    section_totals[s] = section_totals.get(s, 0) + obj['amount']
sorted_sections = sorted(section_totals.items(), key=lambda x: -x[1])

data_js = 'const ALL = [\n  ' + ',\n  '.join(js_rows) + '\n];\n\n'
section_js = 'const SECTION_TOTALS = ' + json.dumps(dict(sorted_sections), ensure_ascii=False) + ';\n'

# Write the data JS file
with open('C:/Users/DARA-PC/dashboard_data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)
    f.write(section_js)

print(f"Written dashboard_data.js with {len(js_rows)} rows")
print(f"Data size: {len(data_js)} chars")
