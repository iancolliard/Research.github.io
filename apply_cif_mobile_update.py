from pathlib import Path

path = Path("src/pages/Crystallography/viewer.astro")
if not path.exists():
    raise SystemExit("Run this from the root of Research.github.io; viewer.astro was not found.")

text = path.read_text(encoding="utf-8")
original = text

text = text.replace(
    ":root{--bg:#fff;--panel:#fff;--text:#222;--border:#c8c8c8;--soft:#f5f5f5;--muted:#666}",
    ":root{--bg:#fff;--panel:#fff;--text:#222;--border:#c8c8c8;--soft:#f5f5f5;--muted:#666;--toolbar-h:54px}"
)
text = text.replace("#toolbar{height:54px;display:flex;", "#toolbar{height:var(--toolbar-h);display:flex;")
text = text.replace(
    "#viewerWrap{height:calc(100vh - 54px);position:relative}.plot{width:100%;height:100%}",
    "#viewerWrap{height:calc(100vh - var(--toolbar-h));height:calc(100dvh - var(--toolbar-h));position:relative}.plot{width:100%;height:100%}"
)
text = text.replace(
    "#projectionCanvas{width:100%;height:100%}",
    "#projectionCanvas{width:100%;height:100%}\n    #mobileInfoToggle{display:none}"
)

old_mobile = "@media(max-width:800px){#infoPanel{width:240px;max-height:38vh}.version{display:none}}"
new_mobile = r'''@media(max-width:800px){
      :root{--toolbar-h:58px}
      html,body{height:100dvh;overflow:hidden;overscroll-behavior:none}
      #toolbar{padding:0 8px;gap:6px;overflow-x:auto;overflow-y:visible;scrollbar-width:none;-webkit-overflow-scrolling:touch}
      #toolbar::-webkit-scrollbar{display:none}
      #toolbar>*{flex:0 0 auto}
      .brand{font-size:14px}.version{display:none}
      #toolbar select,#toolbar button{height:42px;min-height:42px;font-size:13px;padding:0 12px}
      .popover{position:fixed;left:8px!important;right:8px!important;top:auto!important;bottom:calc(8px + env(safe-area-inset-bottom));width:auto;min-width:0!important;max-height:min(64dvh,560px);padding:12px;border-radius:16px;box-shadow:0 16px 48px rgba(0,0,0,.34);z-index:10000}
      .actions{position:sticky;top:-12px;background:var(--panel);padding:12px 0 9px;z-index:2}
      .actions button{height:38px;font-size:12px}
      .check-row{min-height:42px;font-size:14px;padding:7px 5px}.check-row input{width:18px;height:18px}
      .range-pair{padding:12px 2px 15px}.range-pair input[type=range]{min-height:34px}
      #mobileInfoToggle{display:block;position:absolute;left:8px;top:8px;z-index:35;height:40px;padding:0 12px;background:color-mix(in srgb,var(--panel) 96%,transparent);box-shadow:0 4px 14px rgba(0,0,0,.12);backdrop-filter:blur(8px)}
      #infoPanel{display:none;left:8px;right:8px;top:56px;width:auto;max-height:min(48dvh,360px);font-size:12px;z-index:34;backdrop-filter:blur(10px)}
      #infoPanel.mobile-open{display:block}
      #projectionPanel{left:8px;bottom:62px;width:132px;height:132px;padding:4px}
      #elementLegend{left:8px;right:8px;bottom:8px;min-width:0;max-height:none;height:46px;padding:6px 9px;display:flex;align-items:center;gap:10px;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;backdrop-filter:blur(8px)}
      #elementLegend::-webkit-scrollbar{display:none}
      #elementLegend .legend-title{margin:0;position:sticky;left:0;background:var(--panel);padding-right:4px;z-index:2}
      #legendRows{display:flex;align-items:center;gap:11px}.legend-row{flex:0 0 auto;padding:0}
      #customDrawer{left:0;right:0;top:auto;bottom:0;width:100%;height:min(76dvh,680px);border-left:0;border-top:1px solid var(--border);border-radius:18px 18px 0 0;padding-bottom:env(safe-area-inset-bottom);transform:translateY(105%);transition:transform .22s ease;box-shadow:0 -12px 36px rgba(0,0,0,.24);z-index:9000}
      #customDrawer.open{right:0;transform:translateY(0)}.drawer-head{min-height:56px}.custom-row{grid-template-columns:48px minmax(120px,1fr) 76px;min-height:54px}
      #modalBack{padding:8px}.modal{width:100%;max-height:calc(100dvh - 16px);border-radius:16px}.modal-head{position:sticky;top:0;background:var(--panel);z-index:4}.modal-head #wyckoffWindow{display:none}.modal-body{padding:8px;overflow-x:auto}table{min-width:620px;font-size:12px}th,td{padding:7px}
      #error{top:12px;max-width:calc(100vw - 24px);width:calc(100vw - 24px)}
    }'''
if old_mobile not in text:
    raise SystemExit("Expected mobile CSS not found; no changes written.")
text = text.replace(old_mobile, new_mobile)

old_viewer = '<div id="viewerWrap">\n  <div id="plot" class="plot"></div>\n  <div id="infoPanel">Loading crystallographic information…</div>'
new_viewer = '<div id="viewerWrap">\n  <div id="plot" class="plot"></div>\n  <button id="mobileInfoToggle" type="button" aria-expanded="false" aria-controls="infoPanel">Crystal info</button>\n  <div id="infoPanel">Loading crystallographic information…</div>'
if old_viewer not in text:
    raise SystemExit("Viewer markup not found; no changes written.")
text = text.replace(old_viewer, new_viewer)

old_render = "  function render(){const dark=document.body.classList.contains('dark');Plotly.react('plot',traces(),{title:{text:titleParam+' — '+({ballstick:'Ball & stick',wireframe:'Wireframe',polyhedral:'Polyhedral'}[mode]),x:.5,font:{color:dark?'#eee':'#222'}},paper_bgcolor:dark?'#17191d':'#fff',plot_bgcolor:dark?'#17191d':'#fff',font:{color:dark?'#eee':'#222'},scene:{bgcolor:dark?'#17191d':'#fff',aspectmode:'data',xaxis:axis('x (Å)',dark),yaxis:axis('y (Å)',dark),zaxis:axis('z (Å)',dark)},margin:{l:330,r:10,b:10,t:60}}, {responsive:true,displaylogo:false});}"
new_render = """  function isMobile(){return matchMedia('(max-width:800px)').matches}
  function render(){
    const dark=document.body.classList.contains('dark'),mobile=isMobile();
    Plotly.react('plot',traces(),{title:{text:titleParam+' — '+({ballstick:'Ball & stick',wireframe:'Wireframe',polyhedral:'Polyhedral'}[mode]),x:.5,font:{color:dark?'#eee':'#222',size:mobile?14:17}},paper_bgcolor:dark?'#17191d':'#fff',plot_bgcolor:dark?'#17191d':'#fff',font:{color:dark?'#eee':'#222'},scene:{bgcolor:dark?'#17191d':'#fff',aspectmode:'data',xaxis:axis('x (Å)',dark),yaxis:axis('y (Å)',dark),zaxis:axis('z (Å)',dark)},margin:mobile?{l:4,r:4,b:48,t:48}:{l:330,r:10,b:10,t:60}}, {responsive:true,displaylogo:false,displayModeBar:!mobile,scrollZoom:true});
  }"""
if old_render not in text:
    raise SystemExit("Plotly render function not found; no changes written.")
text = text.replace(old_render, new_render)

old_menu = "  document.querySelectorAll('[data-menu]').forEach(b=>b.onclick=e=>{e.stopPropagation();const m=$(b.dataset.menu);document.querySelectorAll('.popover').forEach(p=>{if(p!==m)p.classList.remove('open')});m.classList.toggle('open')});document.querySelectorAll('.popover').forEach(p=>p.onclick=e=>e.stopPropagation());document.addEventListener('click',()=>document.querySelectorAll('.popover').forEach(p=>p.classList.remove('open')));"
new_menu = old_menu + """
  $('mobileInfoToggle').onclick=e=>{e.stopPropagation();const open=$('infoPanel').classList.toggle('mobile-open');$('mobileInfoToggle').setAttribute('aria-expanded',String(open));$('mobileInfoToggle').textContent=open?'Close info':'Crystal info';};"""
if old_menu not in text:
    raise SystemExit("Menu handlers not found; no changes written.")
text = text.replace(old_menu, new_menu)

old_tail = "  const saved=localStorage.getItem('cifViewerTheme')||'system';$('themeMode').value=saved;$('themeMode').onchange=e=>applyTheme(e.target.value);matchMedia('(prefers-color-scheme:dark)').addEventListener?.('change',()=>{if($('themeMode').value==='system')applyTheme('system')});\n  applyTheme(saved);drawProjection('c');"
new_tail = """  const saved=localStorage.getItem('cifViewerTheme')||'system';$('themeMode').value=saved;$('themeMode').onchange=e=>applyTheme(e.target.value);matchMedia('(prefers-color-scheme:dark)').addEventListener?.('change',()=>{if($('themeMode').value==='system')applyTheme('system')});
  let resizeTimer;addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{if(!isMobile()){$('infoPanel').classList.remove('mobile-open');$('mobileInfoToggle').setAttribute('aria-expanded','false');$('mobileInfoToggle').textContent='Crystal info';}render();drawProjection($('projectionMode').value);},120)});
  applyTheme(saved);drawProjection('c');"""
if old_tail not in text:
    raise SystemExit("Theme initialization not found; no changes written.")
text = text.replace(old_tail, new_tail)

backup = path.with_suffix('.astro.before-mobile')
if not backup.exists():
    backup.write_text(original, encoding='utf-8')
path.write_text(text, encoding='utf-8')
print('Updated:', path)
print('Backup: ', backup)
print('Now run: npm run dev')
