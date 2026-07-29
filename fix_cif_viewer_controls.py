from pathlib import Path

path = Path("src/pages/Crystallography/viewer.astro")
if not path.exists():
    raise SystemExit(
        "Could not find src/pages/Crystallography/viewer.astro.\n"
        "Run this script from the root of your Research.github.io project."
    )

text = path.read_text(encoding="utf-8")
original = text

replacements = []

# 1) Legend swatches: prevent flex shrinking/collapsing and make color visible in all browsers.
replacements.append((
    ".dot{width:12px;height:12px;border-radius:50%;border:1px solid #555}",
    ".dot{display:inline-block;flex:0 0 12px;width:12px;height:12px;min-width:12px;min-height:12px;border-radius:50%;border:1px solid color-mix(in srgb,var(--text) 55%,transparent);box-shadow:inset 0 0 0 .5px rgba(255,255,255,.2)}"
))

# 2) More robust per-element atom sizing for every rendered atom marker.
old_atoms = """    for(const e of elements){if(!visibleAtoms.has(e))continue;const aa=atoms.filter(a=>a.elem===e),sz=(mode==='wireframe'?.35:mode==='polyhedral'?.42:1)*styles[e].scale*(12+6*(RADII[e]||.75));T.push({type:'scatter3d',mode:'markers',x:aa.map(a=>a.xyz[0]),y:aa.map(a=>a.xyz[1]),z:aa.map(a=>a.xyz[2]),marker:{size:sz,color:styles[e].color,line:{width:1,color:'#333'}},text:aa.map(a=>`<b>${a.label}</b><br>${e}<br>${a.xyz.map(v=>v.toFixed(4)).join(', ')} Å`),hovertemplate:'%{text}<extra></extra>',showlegend:false});const ii=imgs.filter(a=>a.elem===e);if(ii.length)T.push({type:'scatter3d',mode:'markers',x:ii.map(a=>a.xyz[0]),y:ii.map(a=>a.xyz[1]),z:ii.map(a=>a.xyz[2]),marker:{size:sz,color:styles[e].color,opacity:.7,line:{width:1.2,color:'#333'}},text:ii.map(a=>`<b>${a.label}</b> (periodic image)`),hovertemplate:'%{text}<extra></extra>',showlegend:false})}"""

new_atoms = """    const atomMarkerSize=e=>{
      const modeScale=mode==='wireframe'?.35:mode==='polyhedral'?.42:1;
      const base=12+6*(RADII[e]||.75);
      const scale=Number(styles[e]?.scale ?? 1);
      return Math.max(2,modeScale*scale*base);
    };
    for(const e of elements){
      if(!visibleAtoms.has(e))continue;
      const aa=atoms.filter(a=>a.elem===e);
      const sz=atomMarkerSize(e);
      T.push({
        type:'scatter3d',mode:'markers',
        x:aa.map(a=>a.xyz[0]),y:aa.map(a=>a.xyz[1]),z:aa.map(a=>a.xyz[2]),
        marker:{size:sz,sizemode:'diameter',color:styles[e].color,line:{width:1,color:'#333'}},
        text:aa.map(a=>`<b>${a.label}</b><br>${e}<br>${a.xyz.map(v=>v.toFixed(4)).join(', ')} Å`),
        hovertemplate:'%{text}<extra></extra>',showlegend:false
      });
      const ii=imgs.filter(a=>a.elem===e);
      if(ii.length)T.push({
        type:'scatter3d',mode:'markers',
        x:ii.map(a=>a.xyz[0]),y:ii.map(a=>a.xyz[1]),z:ii.map(a=>a.xyz[2]),
        marker:{size:sz,sizemode:'diameter',color:styles[e].color,opacity:.7,line:{width:1.2,color:'#333'}},
        text:ii.map(a=>`<b>${a.label}</b> (periodic image)`),
        hovertemplate:'%{text}<extra></extra>',showlegend:false
      });
    }"""
replacements.append((old_atoms, new_atoms))

# 3) Make customization slider more responsive and ensure its value is committed.
old_custom = """  function renderCustom(){const c=$('customRows');c.innerHTML='';for(const e of elements){const r=document.createElement('div');r.className='custom-row',co=document.createElement('input'),sl=document.createElement('input'),tx=document.createElement('div');co.type='color';co.value=styles[e].color;sl.type='range';sl.min=.3;sl.max=2;sl.step=.05;sl.value=styles[e].scale;tx.className='small';const u=()=>tx.textContent=e+' ×'+Number(sl.value).toFixed(2);co.oninput=()=>{styles[e].color=co.value;renderLegend();render()};sl.oninput=()=>{styles[e].scale=+sl.value;u();render()};u();r.append(co,sl,tx);c.append(r)}}"""

new_custom = """  function renderCustom(){
    const c=$('customRows');c.innerHTML='';
    for(const e of elements){
      const r=document.createElement('div'),
            co=document.createElement('input'),
            sl=document.createElement('input'),
            tx=document.createElement('div');
      r.className='custom-row';
      co.type='color';co.value=styles[e].color;co.setAttribute('aria-label',e+' color');
      sl.type='range';sl.min=.2;sl.max=3;sl.step=.05;sl.value=styles[e].scale;sl.setAttribute('aria-label',e+' atom size');
      tx.className='small';
      const updateLabel=()=>tx.textContent=e+' ×'+Number(styles[e].scale).toFixed(2);
      co.addEventListener('input',()=>{styles[e].color=co.value;renderLegend();render()});
      const updateSize=()=>{styles[e].scale=Number(sl.value);updateLabel();render()};
      sl.addEventListener('input',updateSize);
      sl.addEventListener('change',updateSize);
      updateLabel();
      r.append(co,sl,tx);c.append(r);
    }
  }"""
replacements.append((old_custom, new_custom))

# 4) Replace menu handling. On mobile, portaling popovers to <body> keeps them out of
# the horizontally-scrolling toolbar's clipping/scroll context.
old_menu = """  document.querySelectorAll('[data-menu]').forEach(b=>b.onclick=e=>{e.stopPropagation();const m=$(b.dataset.menu);document.querySelectorAll('.popover').forEach(p=>{if(p!==m)p.classList.remove('open')});m.classList.toggle('open')});document.querySelectorAll('.popover').forEach(p=>p.onclick=e=>e.stopPropagation());document.addEventListener('click',()=>document.querySelectorAll('.popover').forEach(p=>p.classList.remove('open')));"""

new_menu = """  const menuHomes=new Map();
  document.querySelectorAll('.popover').forEach(p=>{
    menuHomes.set(p,{parent:p.parentNode,next:p.nextSibling});
    p.addEventListener('click',e=>e.stopPropagation());
    p.addEventListener('pointerdown',e=>e.stopPropagation());
  });
  function closeMenus(){
    document.querySelectorAll('.popover').forEach(p=>{
      p.classList.remove('open');
      const home=menuHomes.get(p);
      if(home && p.parentNode===document.body){
        home.parent.insertBefore(p,home.next);
      }
    });
  }
  document.querySelectorAll('[data-menu]').forEach(b=>{
    b.type='button';
    b.addEventListener('click',e=>{
      e.preventDefault();
      e.stopPropagation();
      const m=$(b.dataset.menu);
      const wasOpen=m.classList.contains('open');
      closeMenus();
      if(wasOpen)return;
      if(isMobile())document.body.appendChild(m);
      m.classList.add('open');
    });
  });
  document.addEventListener('click',closeMenus);
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenus()});"""
replacements.append((old_menu, new_menu))

for old, new in replacements:
    if old not in text:
        raise SystemExit(
            "One expected code section was not found.\n"
            "Your viewer.astro may differ from the version this fixer expects.\n"
            "No file was written."
        )
    text = text.replace(old, new, 1)

# Also make dynamic legend color assignment explicit and browser-proof.
old_legend = """  function renderLegend(){const c=$('legendRows');c.innerHTML='';for(const e of elements){const r=document.createElement('div');r.className='legend-row';const d=document.createElement('span');d.className='dot';d.style.background=styles[e].color;r.append(d,document.createTextNode(e));c.append(r)}}"""
new_legend = """  function renderLegend(){
    const c=$('legendRows');c.innerHTML='';
    for(const e of elements){
      const r=document.createElement('div');r.className='legend-row';
      const d=document.createElement('span');d.className='dot';
      d.style.setProperty('background-color',styles[e].color,'important');
      d.title=e+' — '+styles[e].color;
      r.append(d,document.createTextNode(e));c.append(r);
    }
  }"""
if old_legend not in text:
    raise SystemExit("Legend renderer was not found. No file was written.")
text = text.replace(old_legend, new_legend, 1)

# Update resize handler so an open mobile menu is cleanly restored on orientation/desktop changes.
old_resize = """  let resizeTimer;addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{if(!isMobile()){$('infoPanel').classList.remove('mobile-open');$('mobileInfoToggle').setAttribute('aria-expanded','false');$('mobileInfoToggle').textContent='Crystal info';}render();drawProjection($('projectionMode').value);},120)});"""
new_resize = """  let resizeTimer;addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{closeMenus();if(!isMobile()){$('infoPanel').classList.remove('mobile-open');$('mobileInfoToggle').setAttribute('aria-expanded','false');$('mobileInfoToggle').textContent='Crystal info';}render();drawProjection($('projectionMode').value);},120)});"""
if old_resize not in text:
    raise SystemExit("Resize handler was not found. No file was written.")
text = text.replace(old_resize, new_resize, 1)

backup = path.with_suffix(".astro.before-ui-fix")
if not backup.exists():
    backup.write_text(original, encoding="utf-8")

path.write_text(text, encoding="utf-8")

print("CIF viewer UI fixes applied.")
print(f"Updated: {path}")
print(f"Backup:  {backup}")
print()
print("Fixed:")
print("  • element legend color swatches")
print("  • per-element atom-size sliders, including periodic-image atoms")
print("  • dropdown/popover reliability on desktop and mobile")
print("  • Escape-to-close and resize/orientation cleanup")
print()
print("Now run: npm run dev")
