import { useState, useEffect, useRef } from "react";

export default function CifViewer({ cifs }) {
  const [selected, setSelected] = useState(cifs[0]);
  const viewerRef = useRef(null);

  useEffect(() => {
    if (viewerRef.current && selected && window.$3Dmol) {
      fetch(`Research.github.io/assets/cifs/${selected}`)
        .then(res => res.text())
        .then(cifData => {
          viewerRef.current.innerHTML = "";
          const viewer = window.$3Dmol.createViewer(viewerRef.current, { backgroundColor: "white" });
          viewer.addModel(cifData, "cif");
          viewer.setStyle({}, {stick: {}, sphere: {scale:0.3}});
          viewer.zoomTo();
          viewer.render();
        });
    }
  }, [selected]);

  return (
    <div>
      <ul>
        {cifs.map(file => (
          <li key={file}>
            <button type="button" onClick={() => setSelected(file)}>
              {file}
            </button>
          </li>
        ))}
      </ul>
      <div ref={viewerRef} style={{ width: "500px", height: "400px" }} />
    </div>
  );
}