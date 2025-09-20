// src/components/JsmolViewer.jsx
import React, { useEffect, useRef } from 'react';

const JsmolViewer = ({ modelUrl }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (window.Jmol && containerRef.current) {
      const info = {
        width: 800,
        height: 600,
        debug: false,
        addSelectionOptions: false,
        j2sPath: '/j2s', // Path to the JSmol j2s directory
        console: 'none',
      };
      // Initialize the applet on mount
      window.Jmol.getApplet('jmolApplet', info);
    }
  }, []);

  useEffect(() => {
    // Load the new model when the prop changes
    if (window.Jmol && window.Jmol.jmolApplet && modelUrl) {
      window.Jmol.script(window.Jmol.jmolApplet, `load "${modelUrl}"`);
    }
  }, [modelUrl]);

  return <div ref={containerRef} id="jmolApplet" />;
};

export default JsmolViewer;
