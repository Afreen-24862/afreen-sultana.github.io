/* CityAir 3D playground — illustrative simulation (Three.js) */
(() => {
  const stage = document.getElementById('pgStage'), cv = document.getElementById('pgCanvas');
  if (!stage || !window.THREE) return;
  const T = THREE, reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
  let renderer; for (const opts of [{ antialias: true, alpha: true }, { antialias: false, alpha: true }]) { try { renderer = new T.WebGLRenderer({ canvas: cv, ...opts }); break; } catch (e) {} }
  if (!renderer) { const n = document.createElement('p'); n.className = 'gl-fail'; n.innerHTML = 'The 3D view couldn’t start on this device. Try reloading, or turn on hardware acceleration in your browser settings. The sliders still work.'; stage.appendChild(n); return; }
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  const scene = new T.Scene(), cam = new T.PerspectiveCamera(38, 1, .1, 100);
  scene.add(new T.AmbientLight(0xffffff, .75)); const sun = new T.DirectionalLight(0xffffff, .9); sun.position.set(6, 10, 5); scene.add(sun);

  const G = 2.4, N = 3, mat = { b: new T.MeshStandardMaterial({ color: 0xe5e5ea, roughness: .8 }), g: new T.MeshStandardMaterial({ color: 0xf0f0f4, roughness: 1 }), road: new T.MeshStandardMaterial({ color: 0xc9c9cf, roughness: 1 }) };
  const ground = new T.Mesh(new T.PlaneGeometry(22, 22), mat.g); ground.rotation.x = -Math.PI / 2; scene.add(ground);
  const city = new T.Group(); scene.add(city);
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  for (let i = -N; i <= N; i++) for (let j = -N; j <= N; j++) {
    const h = .6 + Math.pow(rnd(), 1.6) * 3.2 * (1 - Math.hypot(i, j) / 6), m = new T.Mesh(new T.BoxGeometry(1.4, h, 1.4), mat.b);
    m.position.set(i * G, h / 2, j * G); city.add(m);
  }
  for (let k = -N - 1; k <= N; k++) for (const ax of [0, 1]) { const r = new T.Mesh(new T.PlaneGeometry(ax ? .55 : 20, ax ? 20 : .55), mat.road); r.rotation.x = -Math.PI / 2; r.position.set(ax ? (k + .5) * G : 0, .01, ax ? 0 : (k + .5) * G); scene.add(r); }

  // cars
  const carMat = new T.MeshStandardMaterial({ color: 0x1d1d1f, roughness: .5 }), cars = [];
  for (let n = 0; n < 22; n++) { const m = new T.Mesh(new T.BoxGeometry(.34, .16, .18), carMat), ax = n % 2, lane = ((n * 3) % (2 * N + 2) - N - 1 + .5) * G; m.userData = { ax, lane, p: rnd() * 18 - 9, s: (.012 + rnd() * .014) * (rnd() > .5 ? 1 : -1) }; m.position.y = .1; scene.add(m); cars.push(m); }

  // trees
  const trees = [], trunk = new T.MeshStandardMaterial({ color: 0x8a6a4a }), leaf = new T.MeshStandardMaterial({ color: 0x34c759, roughness: .9 });
  for (let i = -N - 1; i <= N; i++) for (let j = -N - 1; j <= N; j++) {
    const g = new T.Group(), t = new T.Mesh(new T.CylinderGeometry(.04, .05, .3, 6), trunk), c = new T.Mesh(new T.ConeGeometry(.22, .6, 8), leaf); t.position.y = .15; c.position.y = .55; g.add(t, c);
    g.position.set((i + .5) * G + .45, 0, (j + .5) * G + .45); g.scale.setScalar(.001); scene.add(g); trees.push(g);
  }

  // smog
  const COUNT = 2200, pos = new Float32Array(COUNT * 3), base = new Float32Array(COUNT * 3);
  for (let i = 0; i < COUNT; i++) { base[i * 3] = (rnd() - .5) * 20; base[i * 3 + 1] = .3 + rnd() * 5.5; base[i * 3 + 2] = (rnd() - .5) * 20; }
  pos.set(base);
  const geo = new T.BufferGeometry(); geo.setAttribute('position', new T.BufferAttribute(pos, 3));
  const sp = document.createElement('canvas'); sp.width = sp.height = 64; const sx = sp.getContext('2d'), gr = sx.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.4, 'rgba(255,255,255,.45)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); sx.fillStyle = gr; sx.fillRect(0, 0, 64, 64);
  const smogMat = new T.PointsMaterial({ map: new T.CanvasTexture(sp), size: .9, transparent: true, opacity: .55, depthWrite: false, sizeAttenuation: true, color: 0x30d158 });
  const smog = new T.Points(geo, smogMat); scene.add(smog);

  // state
  const LV = [[50, 'Good', 0x30d158], [100, 'Moderate', 0xffd60a], [150, 'Unhealthy for sensitive groups', 0xff9f0a], [200, 'Unhealthy', 0xff453a], [300, 'Very unhealthy', 0xbf5af2], [Infinity, 'Hazardous', 0xa2123b]];
  const lvl = a => LV.find(l => a <= l[0]);
  const FX = { cars: .22, trees: .18, clean: .12 }, on = { cars: false, trees: false, clean: false };
  const $ = id => document.getElementById(id), range = $('pgRange');
  let base0 = +range.value, shown = base0, az = .8, drag = false, lx = 0, vis = false, t0 = 0;
  const target = () => base0 * (1 - Object.keys(on).reduce((s, k) => s + (on[k] ? FX[k] : 0), 0));
  const color = new T.Color();

  function hud(v) {
    const a = Math.round(v), L = lvl(a), hex = '#' + new T.Color(L[2]).getHexString();
    $('pgAqi').textContent = a; $('pgAqi').style.color = hex; $('pgLvl').textContent = L[1];
    const cut = Math.round((1 - v / base0) * 100); $('pgDelta').textContent = cut > 0 ? `▼ ${cut}% cleaner` : '';
    $('pgHaze').style.background = `radial-gradient(ellipse at 50% 30%, ${hex}, transparent 75%)`; $('pgHaze').style.opacity = Math.min(.5, v / 300 * .6);
  }
  $('pgVal').textContent = base0;
  range.addEventListener('input', () => { window.Explore && Explore.mark('3d'); base0 = +range.value; $('pgVal').textContent = base0; });
  document.querySelectorAll('.pg-t[data-k]').forEach(b => b.addEventListener('click', () => { window.Explore && Explore.mark('3d'); const k = b.dataset.k; on[k] = !on[k]; b.setAttribute('aria-pressed', on[k]); }));
  const live = $('pgLive'); const syncLive = () => { if (window.CITY_AQI != null) { $('pgLiveSub').textContent = `AQI ${window.CITY_AQI} now`; } };
  window.addEventListener('cityaqi', syncLive); syncLive();
  live.addEventListener('click', () => { if (window.CITY_AQI == null) { $('pgLiveSub').textContent = 'scroll to the demo first'; return; } base0 = Math.min(300, window.CITY_AQI); range.value = base0; $('pgVal').textContent = base0; });

  // orbit
  stage.addEventListener('pointerdown', e => { drag = true; lx = e.clientX; stage.setPointerCapture(e.pointerId); stage.classList.add('drag'); });
  stage.addEventListener('pointermove', e => { if (drag) { az -= (e.clientX - lx) * .008; lx = e.clientX; } });
  const up = () => { drag = false; stage.classList.remove('drag'); }; stage.addEventListener('pointerup', up); stage.addEventListener('pointercancel', up);

  function size() { const w = stage.clientWidth, h = stage.clientHeight; renderer.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); }
  new ResizeObserver(size).observe(stage); size();

  function frame(t) {
    if (!vis) return; requestAnimationFrame(frame);
    const dark = document.documentElement.dataset.theme === 'dark';
    mat.b.color.setHex(dark ? 0x3a3a3f : 0xe5e5ea); mat.g.color.setHex(dark ? 0x1c1c1e : 0xf0f0f4); mat.road.color.setHex(dark ? 0x2a2a2d : 0xc9c9cf);
    shown += (target() - shown) * .06; hud(shown);
    const p = Math.min(1, shown / 300);
    // smog
    geo.setDrawRange(0, Math.floor(COUNT * Math.pow(p, .75)));
    smogMat.color.set(lvl(shown)[2]); smogMat.opacity = .18 + p * .5;
    const s = t * .0004; const a = geo.attributes.position.array;
    for (let i = 0; i < COUNT; i++) { a[i * 3] = base[i * 3] + Math.sin(s + i) * .35; a[i * 3 + 1] = base[i * 3 + 1] + Math.sin(s * 1.3 + i * .7) * .2; }
    geo.attributes.position.needsUpdate = true;
    // cars
    const active = on.cars ? 7 : cars.length;
    cars.forEach((c, i) => { const d = c.userData; c.visible = i < active; d.p += d.s; if (d.p > 10) d.p = -10; if (d.p < -10) d.p = 10; c.position.x = d.ax ? d.lane : d.p; c.position.z = d.ax ? d.p : d.lane; c.rotation.y = d.ax ? Math.PI / 2 : 0; });
    // trees
    trees.forEach((tr, i) => { const goal = on.trees ? 1 : .001, cur = tr.scale.x; tr.scale.setScalar(cur + (goal - cur) * (.08 - Math.min(.05, i * .0007))); });
    // camera
    if (!drag && !reduce) az += .0016;
    cam.position.set(Math.sin(az) * 15, 9.5, Math.cos(az) * 15); cam.lookAt(0, 1, 0);
    renderer.render(scene, cam);
  }
  const start = () => { if (!vis) { vis = true; requestAnimationFrame(frame); } };
  if ('IntersectionObserver' in window) new IntersectionObserver(es => { if (es[0].isIntersecting) start(); else vis = false; }, { rootMargin: '100px' }).observe(stage); else start();
  hud(shown);
})();
