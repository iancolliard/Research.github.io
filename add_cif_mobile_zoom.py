from pathlib import Path

path = Path("src/pages/Crystallography/viewer.astro")
if not path.exists():
    raise SystemExit(
        "Could not find src/pages/Crystallography/viewer.astro.\n"
        "Run this script from the root of your Research.github.io project."
    )

text = path.read_text(encoding="utf-8")
original = text

# 1. Add zoom controls CSS.
anchor_css = "#mobileInfoToggle{display:none}"
replacement_css = """#mobileInfoToggle{display:none}
    #mobileZoomControls{display:none}"""

if anchor_css not in text:
    raise SystemExit("Could not find mobile info CSS anchor. No changes written.")
text = text.replace(anchor_css, replacement_css, 1)

mobile_anchor = """      #mobileInfoToggle{display:block;position:absolute;left:8px;top:8px;z-index:35;height:40px;padding:0 12px;background:color-mix(in srgb,var(--panel) 96%,transparent);box-shadow:0 4px 14px rgba(0,0,0,.12);backdrop-filter:blur(8px)}"""

mobile_replacement = mobile_anchor + r"""
      #plot{touch-action:none}
      #mobileZoomControls{
        display:flex;
        position:absolute;
        right:8px;
        top:8px;
        z-index:36;
        gap:6px;
      }
      #mobileZoomControls button{
        width:42px;
        height:42px;
        min-width:42px;
        padding:0;
        font-size:20px;
        font-weight:700;
        background:color-mix(in srgb,var(--panel) 96%,transparent);
        box-shadow:0 4px 14px rgba(0,0,0,.12);
        backdrop-filter:blur(8px);
      }
      #mobileZoomControls #zoomReset{
        width:auto;
        min-width:58px;
        padding:0 10px;
        font-size:12px;
        font-weight:600;
      }"""

if mobile_anchor not in text:
    raise SystemExit("Could not find mobileInfoToggle mobile rule. No changes written.")
text = text.replace(mobile_anchor, mobile_replacement, 1)

# 2. Add zoom controls markup.
viewer_anchor = """  <button id="mobileInfoToggle" type="button" aria-expanded="false" aria-controls="infoPanel">Crystal info</button>
  <div id="infoPanel">Loading crystallographic information…</div>"""

viewer_replacement = """  <button id="mobileInfoToggle" type="button" aria-expanded="false" aria-controls="infoPanel">Crystal info</button>
  <div id="mobileZoomControls" aria-label="3D zoom controls">
    <button id="zoomIn" type="button" aria-label="Zoom in">+</button>
    <button id="zoomOut" type="button" aria-label="Zoom out">−</button>
    <button id="zoomReset" type="button" aria-label="Reset 3D view">Reset</button>
  </div>
  <div id="infoPanel">Loading crystallographic information…</div>"""

if viewer_anchor not in text:
    raise SystemExit("Could not find viewer markup anchor. No changes written.")
text = text.replace(viewer_anchor, viewer_replacement, 1)

# 3. Add camera helpers before applyTheme.
theme_anchor = """  function applyTheme(v){let dark=v==='dark'||(v==='system'&&matchMedia('(prefers-color-scheme:dark)').matches);document.body.classList.toggle('dark',dark);localStorage.setItem('cifViewerTheme',v);render();drawProjection($('projectionMode').value)}"""

camera_helpers = r"""  const defaultCameraEye={x:1.25,y:1.25,z:1.25};
  let currentCameraEye={...defaultCameraEye};

  function setCameraEye(eye){
    currentCameraEye={x:eye.x,y:eye.y,z:eye.z};
    Plotly.relayout('plot',{
      'scene.camera.eye.x':currentCameraEye.x,
      'scene.camera.eye.y':currentCameraEye.y,
      'scene.camera.eye.z':currentCameraEye.z
    });
  }

  function zoomCamera(factor){
    const eye=currentCameraEye||defaultCameraEye;
    setCameraEye({
      x:eye.x*factor,
      y:eye.y*factor,
      z:eye.z*factor
    });
  }

  function resetCamera(){
    setCameraEye({...defaultCameraEye});
  }

""" + theme_anchor

if theme_anchor not in text:
    raise SystemExit("Could not find applyTheme(). No changes written.")
text = text.replace(theme_anchor, camera_helpers, 1)

# 4. Add mobile zoom button handlers and capture camera changes from touch/drag.
handler_anchor = """  $('mobileInfoToggle').onclick=e=>{e.stopPropagation();const open=$('infoPanel').classList.toggle('mobile-open');$('mobileInfoToggle').setAttribute('aria-expanded',String(open));$('mobileInfoToggle').textContent=open?'Close info':'Crystal info';};"""

handler_replacement = handler_anchor + r"""
  $('zoomIn').onclick=e=>{e.stopPropagation();zoomCamera(.82)};
  $('zoomOut').onclick=e=>{e.stopPropagation();zoomCamera(1.22)};
  $('zoomReset').onclick=e=>{e.stopPropagation();resetCamera()};

  const plotEl=$('plot');
  plotEl.on?.('plotly_relayout',ev=>{
    const cam=ev?.['scene.camera'];
    if(cam?.eye && [cam.eye.x,cam.eye.y,cam.eye.z].every(Number.isFinite)){
      currentCameraEye={x:cam.eye.x,y:cam.eye.y,z:cam.eye.z};
    }
  });"""

if handler_anchor not in text:
    raise SystemExit("Could not find mobile info handler. No changes written.")
text = text.replace(handler_anchor, handler_replacement, 1)

backup = path.with_suffix(".astro.before-mobile-zoom")
if not backup.exists():
    backup.write_text(original, encoding="utf-8")

path.write_text(text, encoding="utf-8")

print("Mobile 3D zoom controls added.")
print(f"Updated: {path}")
print(f"Backup:  {backup}")
print()
print("Mobile now has:")
print("  • pinch/touch gestures directed to the 3D plot")
print("  • + zoom in")
print("  • − zoom out")
print("  • Reset camera")
print()
print("Run: npm run dev")
