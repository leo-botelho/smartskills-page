// Smart Skills Hub — cena 3D do símbolo da marca.
// Modo por página: hero | layers | particles | graph
import * as THREE from 'three';

const CYAN = 0x00D4FF, WHITE = 0xF4F1EB, CARBON = 0x1C2035, VIOLET = 0x8B5CF6;
// Polilinha do símbolo (viewBox 32), centralizada em (18,16)
const PTS = [[22,4],[14,4],[14,16],[22,16],[22,28],[14,28]].map(([x,y]) => new THREE.Vector3(x-18, -(y-16), 0));

export function mountScene(container, mode = 'hero') {
  if (!container) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canvasTest = document.createElement('canvas');
  const gl = canvasTest.getContext('webgl2') || canvasTest.getContext('webgl');
  if (!gl) return; // fica o SVG estático

  const isMobile = innerWidth < 900;
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, isMobile ? 1.5 : 2));
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 200);
  camera.position.set(0, 0, 78);

  // Luzes: principal fria de cima, preenchimento violeta fraco, ambiente
  scene.add(new THREE.AmbientLight(0xbfd8e6, 0.9));
  const key = new THREE.DirectionalLight(0xdff6ff, 2.2); key.position.set(8, 18, 24); scene.add(key);
  const fill = new THREE.DirectionalLight(VIOLET, 0.35); fill.position.set(-14, -8, 10); scene.add(fill);
  const rim = new THREE.DirectionalLight(CYAN, 0.8); rim.position.set(-10, 6, -18); scene.add(rim);

  const group = new THREE.Group(); scene.add(group);

  // Material: metal fosco escuro com reflexo frio
  const bodyMat = new THREE.MeshPhysicalMaterial({ color: 0x2A3450, metalness: 0.55, roughness: 0.38, clearcoat: 0.7, clearcoatRoughness: 0.2, envMapIntensity: 1.4 });
  const edgeMat = new THREE.LineBasicMaterial({ color: WHITE, transparent: true, opacity: 0.85 });
  const nodeMat = new THREE.MeshStandardMaterial({ color: CYAN, emissive: CYAN, emissiveIntensity: 0.75, roughness: 0.35, metalness: 0.05 });

  // Ambiente de reflexo procedural (sem arquivo externo)
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envScene = new THREE.Scene();
  envScene.background = new THREE.Color(0x0E1628);
  const envLight = new THREE.Mesh(new THREE.SphereGeometry(20, 16, 16), new THREE.MeshBasicMaterial({ color: 0x9fdfff, side: THREE.BackSide }));
  envLight.position.set(0, 30, 0); envScene.add(envLight);
  scene.environment = pmrem.fromScene(envScene, 0.04).texture;

  // Segmentos do "S" como caixas (traço 2.2, profundidade 3.2)
  const T = 2.2, D = 3.2;
  for (let i = 0; i < PTS.length - 1; i++) {
    const a = PTS[i], b = PTS[i + 1];
    const len = a.distanceTo(b) + T; // terminais quadrados
    const horiz = Math.abs(a.y - b.y) < 0.001;
    const geo = new THREE.BoxGeometry(horiz ? len : T, horiz ? T : len, D);
    const mesh = new THREE.Mesh(geo, bodyMat);
    mesh.position.copy(a).add(b).multiplyScalar(0.5);
    group.add(mesh);
    group.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo), edgeMat).translateX(mesh.position.x).translateY(mesh.position.y));
  }
  // Nós emissivos nas extremidades
  const nodes = [PTS[0], PTS[PTS.length - 1]].map(p => {
    // Centrada na barra (z = 0) e com raio maior que a meia-diagonal da ponta,
    // para o nó envolver o fim do traço em qualquer ângulo de rotação.
    const m = new THREE.Mesh(new THREE.SphereGeometry(2.9, 32, 32), nodeMat);
    m.position.copy(p); group.add(m);
    const l = new THREE.PointLight(CYAN, 10, 36, 2); l.position.copy(m.position).setZ(m.position.z + 3); group.add(l);
    return m;
  });

  // Modos por página
  const extras = [];
  if (mode === 'layers') {
    const planeMat = new THREE.MeshPhysicalMaterial({ color: 0x0E1628, transparent: true, opacity: 0.55, roughness: 0.5, metalness: 0.3 });
    for (let i = 1; i <= 3; i++) {
      const p = new THREE.Mesh(new THREE.BoxGeometry(30, 30, 0.6), planeMat);
      p.position.set(i * 2.2, -i * 2.2, -i * 4.5); group.add(p);
      group.add(new THREE.LineSegments(new THREE.EdgesGeometry(p.geometry), new THREE.LineBasicMaterial({ color: CYAN, transparent: true, opacity: 0.25 })).translateX(p.position.x).translateY(p.position.y).translateZ(p.position.z));
      extras.push(p);
    }
  }
  let particles, curve;
  if (mode === 'particles') {
    curve = new THREE.CatmullRomCurve3(PTS.map(p => p.clone().setZ(D / 2 + 0.6)), false, 'catmullrom', 0.02);
    const N = 60, pos = new Float32Array(N * 3);
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    particles = new THREE.Points(g, new THREE.PointsMaterial({ color: CYAN, size: 0.9, transparent: true, opacity: 0.9 }));
    particles.userData = { N };
    group.add(particles);
  }
  if (mode === 'graph') {
    const satMat = new THREE.MeshStandardMaterial({ color: 0xF4F1EB, emissive: 0x00D4FF, emissiveIntensity: 0.35, roughness: 0.4 });
    const lineMat = new THREE.LineBasicMaterial({ color: CYAN, transparent: true, opacity: 0.35 });
    const sats = [];
    for (let i = 0; i < 8; i++) {
      const ang = (i / 8) * Math.PI * 2, r = 19 + (i % 2) * 4;
      const s = new THREE.Mesh(new THREE.SphereGeometry(0.9, 16, 16), satMat);
      s.position.set(Math.cos(ang) * r, Math.sin(ang) * r * 0.8, -4 - (i % 3) * 3);
      s.userData = { ang, r, ph: i };
      group.add(s); sats.push(s);
      const target = nodes[i % 2].position;
      const lg = new THREE.BufferGeometry().setFromPoints([s.position, target]);
      const ln = new THREE.Line(lg, lineMat); ln.userData = { s, target }; group.add(ln); extras.push(ln);
    }
    extras.sats = sats;
  }

  // Interação: cursor (desktop) + scroll + rotação lenta
  const mouse = { x: 0, y: 0 };
  if (!isMobile && !reduced) addEventListener('pointermove', e => { mouse.x = (e.clientX / innerWidth - 0.5) * 2; mouse.y = (e.clientY / innerHeight - 0.5) * 2; }, { passive: true });

  function resize() {
    const w = container.clientWidth, h = container.clientHeight || w;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  resize(); addEventListener('resize', resize);

  let visible = true;
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }, { threshold: 0.05 }).observe(container);

  const clock = new THREE.Clock();
  function frame() {
    requestAnimationFrame(frame);
    if (!visible || document.hidden) return;
    const t = clock.getElapsedTime();
    const scroll = Math.min(scrollY / innerHeight, 1);
    const ry = (reduced ? 0.25 : Math.sin(t * 0.35) * 0.35) + mouse.x * 0.35 + scroll * 1.2;
    const rx = (reduced ? -0.15 : Math.cos(t * 0.28) * 0.12) - mouse.y * 0.25 + scroll * 0.3;
    group.rotation.y += (ry - group.rotation.y) * 0.06;
    group.rotation.x += (rx - group.rotation.x) * 0.06;
    group.position.y = reduced ? 0 : Math.sin(t * 0.8) * 0.4;
    nodes.forEach((n, i) => { n.material.emissiveIntensity = 0.7 + Math.sin(t * 2 + i * Math.PI) * 0.25; });
    if (particles) {
      const a = particles.geometry.attributes.position, N = particles.userData.N;
      for (let i = 0; i < N; i++) { const u = ((t * 0.12) + i / N) % 1; const p = curve.getPointAt(u); a.setXYZ(i, p.x, p.y, p.z + Math.sin(u * 40 + t) * 0.25); }
      a.needsUpdate = true;
    }
    if (extras.sats) {
      extras.sats.forEach(s => { const { ang, r, ph } = s.userData; s.position.x = Math.cos(ang + t * 0.15) * r; s.position.y = Math.sin(ang + t * 0.15) * r * 0.8 + Math.sin(t + ph) * 0.6; });
      extras.forEach(ln => { if (ln.userData.s) { ln.geometry.setFromPoints([ln.userData.s.position, ln.userData.target]); } });
    }
    renderer.render(scene, camera);
  }
  frame();
  container.parentElement.classList.add('ready');
}
