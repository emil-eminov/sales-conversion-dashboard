# Builds Sales_Dashboard.html: one self-contained file (data + d3 inlined) that opens offline in any browser.
import json, re, sys
page_path, csv_path, d3_path, out_path = sys.argv[1:5]
page = open(page_path).read().replace('<meta name="dash-one-writer">\n', '')
style = re.search(r'<style>(.*?)</style>', page, re.S).group(1)
script = re.search(r'<script>(.*?)</script>', page, re.S).group(1)
markup = re.sub(r'<style>.*?</style>|<script>.*?</script>', '', page, flags=re.S).strip()
csv_js = json.dumps(open(csv_path).read()).replace('</', '<\\/')
d3 = open(d3_path).read()

theme = """
:root {
  --font-anthropic-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --font-anthropic-serif: Georgia, "Times New Roman", serif;
  --color-fg: #1f1e1c; --color-fg-muted: #6b6862; --color-bg: #faf9f5; --color-panel: #ffffff;
  --color-border-line: #e4e1d8; --color-ok: #2e7d4f; --color-warn: #a86400; --color-bad: #c0392b;
  --cds-font-size-caption: 12.5px; --cds-font-size-body: 15px; --cds-font-size-heading: 17px; --cds-font-size-title: 26px;
  --cds-font-weight-medium: 600; --cds-gap-xs: 4px; --cds-gap-sm: 8px; --cds-gap-md: 16px; --cds-gap-lg: 24px; --cds-gap-xl: 32px;
  --cds-pad-xs: 4px; --cds-pad-sm: 8px; --cds-pad-lg: 20px; --cds-radius: 8px;
  --cds-chart-grid: #ece9e1; --cds-chart-reference: #9a968c; --cds-chart-status-critical: #d0453a;
  --cds-surface-popover: #ffffff; --cds-border: #d9d5ca; --cds-shadow-popover: 0 4px 16px rgba(0,0,0,.12);
  --cds-text-secondary: #6b6862; --cds-dur-slow: .3s;
}
@media (prefers-color-scheme: dark) {
  :root {
    --color-fg: #ecebe6; --color-fg-muted: #a5a29a; --color-bg: #1c1b19; --color-panel: #262522;
    --color-border-line: #3a3833; --color-ok: #5cc28a; --color-bad: #ef6b5e;
    --cds-chart-grid: #34322d; --cds-chart-reference: #8a867c; --cds-chart-status-critical: #e5584c;
    --cds-surface-popover: #2e2d29; --cds-border: #45433d; --cds-text-secondary: #a5a29a;
  }
}
html, body { margin: 0; background: var(--color-bg); }
#dash-root { max-width: 1200px; margin: 0 auto; padding: 32px 20px 48px; }
.dash-select { font: inherit; font-size: var(--cds-font-size-caption); padding: 6px 10px; border-radius: var(--cds-radius);
  border: 1px solid var(--color-border-line); background-color: var(--color-panel); color: var(--color-fg); }
"""

shim = """
// Small stand-in for the hosted dashboard runtime: computes each metric from the embedded CSV and draws the page.
window.dash = (() => {
  const store = { leads: d3.csvParse(LEADS_CSV) };
  const draws = {};
  const run = (name) => document.querySelectorAll(`[data-draw="${name}"]`).forEach((el) => draws[name](el));
  return {
    colors: ['#2f6fdb', '#d9822b', '#8a5cc7', '#2e9e8f', '#c2457a', '#7a8b2e', '#5a6b8c', '#b0752f'],
    calc(id, { inputs, fn }) { store[id] = fn(...inputs.map((i) => store[i])); },
    data(id) { return { status: store[id] ? 'ok' : 'missing', data: store[id] || [] }; },
    draw(name, fn) { if (fn) draws[name] = fn; if (draws[name]) run(name); },
    redrawAll() { Object.keys(draws).forEach(run); },
  };
})();
"""

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Historical Conversion Performance</title>
<style>{theme}{style}</style>
</head>
<body>
<div id="dash-root">
{markup}
</div>
<script>{d3}</script>
<script>const LEADS_CSV = {csv_js};</script>
<script>{shim}</script>
<script>{script}
let resizeTimer;
window.addEventListener('resize', () => {{ clearTimeout(resizeTimer); resizeTimer = setTimeout(() => dash.redrawAll(), 150); }});
</script>
</body>
</html>
"""
open(out_path, 'w').write(html)
print('wrote', out_path, len(html), 'bytes')
