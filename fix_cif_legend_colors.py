from pathlib import Path

path = Path("src/pages/Crystallography/viewer.astro")
if not path.exists():
    raise SystemExit(
        "Could not find src/pages/Crystallography/viewer.astro.\n"
        "Run this script from the root of your Research.github.io project."
    )

text = path.read_text(encoding="utf-8")
original = text

old_css_candidates = [
    ".dot{display:inline-block;flex:0 0 12px;width:12px;height:12px;min-width:12px;min-height:12px;border-radius:50%;border:1px solid color-mix(in srgb,var(--text) 55%,transparent);box-shadow:inset 0 0 0 .5px rgba(255,255,255,.2)}",
    ".dot{width:12px;height:12px;border-radius:50%;border:1px solid #555}",
]

new_css = ".dot{display:inline-flex;flex:0 0 auto;width:18px;height:18px;align-items:center;justify-content:center;font-size:18px;line-height:1;font-family:Arial,sans-serif;text-shadow:0 0 1px rgba(0,0,0,.35)}"

css_done = False
for old_css in old_css_candidates:
    if old_css in text:
        text = text.replace(old_css, new_css, 1)
        css_done = True
        break

if not css_done:
    raise SystemExit("Could not locate the legend .dot CSS. No changes were written.")

old_renderers = [
"""  function renderLegend(){
    const c=$('legendRows');c.innerHTML='';
    for(const e of elements){
      const r=document.createElement('div');r.className='legend-row';
      const d=document.createElement('span');d.className='dot';
      d.style.setProperty('background-color',styles[e].color,'important');
      d.title=e+' — '+styles[e].color;
      r.append(d,document.createTextNode(e));c.append(r);
    }
  }""",
"""  function renderLegend(){const c=$('legendRows');c.innerHTML='';for(const e of elements){const r=document.createElement('div');r.className='legend-row';const d=document.createElement('span');d.className='dot';d.style.background=styles[e].color;r.append(d,document.createTextNode(e));c.append(r)}}"""
]

new_renderer = """  function renderLegend(){
    const c=$('legendRows');
    c.innerHTML='';
    for(const e of elements){
      const r=document.createElement('div');
      r.className='legend-row';

      const d=document.createElement('span');
      d.className='dot';
      d.textContent='●';
      d.style.setProperty('color',styles[e].color,'important');
      d.title=e+' — '+styles[e].color;
      d.setAttribute('aria-hidden','true');

      const label=document.createElement('span');
      label.textContent=e;

      r.append(d,label);
      c.append(r);
    }
  }"""

renderer_done = False
for old in old_renderers:
    if old in text:
        text = text.replace(old, new_renderer, 1)
        renderer_done = True
        break

if not renderer_done:
    raise SystemExit("Could not locate renderLegend(). No changes were written.")

backup = path.with_suffix(".astro.before-legend-dot-fix")
if not backup.exists():
    backup.write_text(original, encoding="utf-8")

path.write_text(text, encoding="utf-8")

print("Legend fix applied.")
print(f"Updated: {path}")
print(f"Backup:  {backup}")
print()
print("The legend now uses a literal colored ● instead of a CSS background circle.")
print("Run: npm run dev")
