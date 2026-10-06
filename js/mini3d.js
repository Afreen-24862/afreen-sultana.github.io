/* Per-project mini 3D playgrounds — "without it" → "with it" (illustrative) */
(() => {
  if (!window.THREE) return;
  const T = THREE, GREY = 0x8e8e93, G = 0x30d158, B = 0x0a84ff, R = 0xff453a, O = 0xff9f0a, P = 0xbf5af2;
  let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const rp = () => [(rnd() - .5) * 6, .3 + rnd() * 2.2, (rnd() - .5) * 5];
  const rr = () => [rnd() * 3, rnd() * 3, rnd() * 3];
  const grid = (i, cols, gx, gz, y = .2) => [((i % cols) - (cols - 1) / 2) * gx, y, (Math.floor(i / cols) - 1.5) * gz];

  const CFG = {
    p2: { name: 'CampusBot', n: 36, geo: 'box', size: [.5, .7, .03], before: 'Campus answers hide across dozens of circulars and PDFs.', after: 'The bot pulls the right page and cites it for Malla Reddy students.',
      order: i => { const a = i / 36 * Math.PI * 2 * 2, r = 1.5 + (i % 3) * .55; const top = i < 3; return { p: top ? [(i - 1) * .9, 1.7, 1.3] : [Math.cos(a) * r, .5 + (i % 4) * .35, Math.sin(a) * r], c: top ? G : 0xc7c7cc, r: [0, -a + Math.PI / 2, 0], s: top ? 1.35 : 1 }; }, hub: { color: B, y: 1 } },
    p3: { name: 'FaceMark', n: 30, geo: 'sphere', size: [.2], before: 'Manual roll call: slow, and proxies slip through.', after: 'Faces recognised — attendance logs itself.',
      order: i => ({ p: grid(i, 6, .95, .95, .3), c: G, r: [0, 0, 0], s: 1 }), scan: true },
    p4: { name: 'ReelPick', n: 48, geo: 'box', size: [.28, .28, .28], before: 'An endless catalogue where nothing stands out.', after: 'Movies grouped by taste; best picks rise first.',
      order: i => { const g = i % 4, k = Math.floor(i / 4), cols = [B, P, O, G]; const cx = (g - 1.5) * 1.6; return { p: [cx + ((k % 3) - 1) * .4, .25 + Math.floor(k / 3) * .38, ((k * 7) % 3 - 1) * .4], c: cols[g], r: [0, k * .3, 0], s: k === 0 ? 1.7 : 1 }; } },
    p5: { name: 'SentiScope', n: 45, geo: 'sphere', size: [.17], before: 'Thousands of opinions, no clear picture.', after: 'Sorted into positive, neutral and negative at a glance.',
      order: i => { const cls = i % 3 === 0 ? 0 : i % 3 === 1 ? 1 : 2, order = [G, GREY, R], idx = Math.floor(i / 3), cnt = [5, 4, 6]; return { p: [(cls - 1) * 2, .2 + (idx % [5, 4, 6][cls]) * .38, ((idx * 5) % 3 - 1) * .3], c: order[cls], r: [0, 0, 0], s: 1 }; } },
    p6: { name: 'LibraryHub', n: 42, geo: 'box', size: [.14, .5, .34], before: 'Paper registers, lost books, unclear fines.', after: 'Every book catalogued, issued and tracked.',
      order: i => { const row = Math.floor(i / 14), k = i % 14; return { p: [(k - 6.5) * .2, .3 + row * .75, -.2], c: [B, G, O, P][i % 4], r: [0, 0, 0], s: 1 }; }, shelf: true },
    p7: { name: 'ResumeLens', n: 24, geo: 'box', size: [.6, .8, .04], before: 'A pile of resumes to read by hand.', after: 'Ranked by fit — best matches first.',
      order: i => { const sc = 1 - i / 24; const c = new T.Color().setHSL(.33 * sc, .75, .5).getHex(); return { p: [-2.6 + i * .22, .45 + sc * .5, 0], c: i < 3 ? G : c, r: [0, .25, 0], s: i < 3 ? 1.25 : 1 }; } },
    p8: { name: 'TaskFlow', n: 30, geo: 'box', size: [.34, .34, .34], before: 'Deadlines scattered across notes and chats.', after: 'Organised into To do, Doing, Done.',
      order: i => { const col = i % 3, k = Math.floor(i / 3), c = [GREY, B, G]; return { p: [(col - 1) * 1.8, .2 + (k % 6) * .4, (Math.floor(k / 6) - .5) * .5], c: c[col], r: [0, 0, 0], s: 1 }; } }
  };

  let state = null;
  function unmount() { if (!state) return; cancelAnimationFrame(state.raf); state.ro.disconnect(); state.r.dispose(); try { state.r.forceContextLoss(); } catch (e) {} state = null; }

  function mount(el, id) {
    unmount(); const cfg = CFG[id]; if (!cfg) return false;
    // always use a brand-new canvas: a canvas whose context was released cannot get a new one
    const oldCv = el.querySelector('canvas'), cv = document.createElement('canvas'); oldCv.replaceWith(cv);
    let r; for (const opts of [{ antialias: true, alpha: true }, { antialias: false, alpha: true }]) { try { r = new T.WebGLRenderer({ canvas: cv, ...opts }); break; } catch (e) {} }
    if (!r) { const n = document.createElement('p'); n.className = 'gl-fail'; n.innerHTML = 'The 3D view couldn’t start on this device. Try reloading, or turn on hardware acceleration in your browser settings.'; el.appendChild(n); return false; }
    r.setPixelRatio(Math.min(devicePixelRatio, 2));
    const scene = new T.Scene(), cam = new T.PerspectiveCamera(40, 1, .1, 60);
    scene.add(new T.AmbientLight(0xffffff, .8)); const d = new T.DirectionalLight(0xffffff, .9); d.position.set(4, 8, 5); scene.add(d);
    const floor = new T.Mesh(new T.CircleGeometry(5.5, 48), new T.MeshStandardMaterial({ color: 0xf0f0f4, roughness: 1 })); floor.rotation.x = -Math.PI / 2; scene.add(floor);
    if (cfg.shelf) for (let k = 0; k < 3; k++) { const s = new T.Mesh(new T.BoxGeometry(3.2, .05, .5), new T.MeshStandardMaterial({ color: 0xb08968 })); s.position.set(0, .04 + k * .75, -.2); scene.add(s); }
    const geo = cfg.geo === 'sphere' ? new T.SphereGeometry(cfg.size[0], 20, 14) : new T.BoxGeometry(...cfg.size);
    seed = 11 + id.charCodeAt(1);
    const items = Array.from({ length: cfg.n }, (_, i) => {
      const o = cfg.order(i), m = new T.Mesh(geo, new T.MeshStandardMaterial({ color: GREY, roughness: .5 })); scene.add(m);
      const it = { m, a: { p: rp(), r: rr(), c: new T.Color(GREY), s: 1 }, b: { p: o.p, r: o.r, c: new T.Color(o.c), s: o.s }, ph: rnd() * 6 }; return it;
    });
    let hub = null; if (cfg.hub) { hub = new T.Mesh(new T.IcosahedronGeometry(.45, 1), new T.MeshStandardMaterial({ color: cfg.hub.color, emissive: cfg.hub.color, emissiveIntensity: .5 })); hub.position.y = cfg.hub.y; hub.scale.setScalar(.001); scene.add(hub); }
    let beam = null; if (cfg.scan) { beam = new T.Mesh(new T.PlaneGeometry(6, .12), new T.MeshBasicMaterial({ color: G, transparent: true, opacity: .0, side: T.DoubleSide })); beam.rotation.x = -Math.PI / 2; beam.position.y = .5; scene.add(beam); }
    let target = 0, cur = 0, az = .6, drag = false, lx = 0, played = false;
    const btns = el.querySelectorAll('[data-m]'), cap = el.querySelector('.m3d-cap');
    const set = v => { target = v; btns.forEach(b => b.setAttribute('aria-pressed', (+b.dataset.m === v))); cap.textContent = v ? cfg.after : cfg.before; };
    btns.forEach(b => b.onclick = () => set(+b.dataset.m)); set(0);
    const t0 = performance.now(); setTimeout(() => { if (state && !played) set(1); }, 1400);
    btns.forEach(b => b.addEventListener('click', () => played = true));
    el.onpointerdown = e => { if (e.target.closest('button')) return; drag = true; lx = e.clientX; el.setPointerCapture(e.pointerId); };
    el.onpointermove = e => { if (drag) { az -= (e.clientX - lx) * .01; lx = e.clientX; } };
    el.onpointerup = el.onpointercancel = () => drag = false;
    const size = () => { const w = el.clientWidth, h = el.clientHeight; r.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); };
    const ro = new ResizeObserver(size); ro.observe(el); size();
    const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, tmp = new T.Color();
    const reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
    function frame(t) {
      state.raf = requestAnimationFrame(frame);
      cur += (target - cur) * .045; const e = ease(Math.min(1, Math.max(0, cur))), s = (t - t0) * .001;
      const dark = document.documentElement.dataset.theme === 'dark'; floor.material.color.setHex(dark ? 0x2a2a2d : 0xf0f0f4);
      items.forEach((it, i) => {
        const { a, b, m } = it, f = (1 - e) * .12;
        m.position.set(a.p[0] + (b.p[0] - a.p[0]) * e, a.p[1] + (b.p[1] - a.p[1]) * e + Math.sin(s * 1.2 + it.ph) * f, a.p[2] + (b.p[2] - a.p[2]) * e);
        m.rotation.set(a.r[0] + (b.r[0] - a.r[0]) * e, a.r[1] + (b.r[1] - a.r[1]) * e + (1 - e) * s * .3, a.r[2] + (b.r[2] - a.r[2]) * e);
        m.scale.setScalar(a.s + (b.s - a.s) * e);
        let delay = cfg.scan ? Math.max(0, Math.min(1, (e - (b.p[2] + 2) / 8) * 3)) : e; m.material.color.copy(a.c).lerp(b.c, delay);
      });
      if (hub) { hub.scale.setScalar(.001 + e * 1); hub.rotation.y = s; }
      if (beam) { beam.material.opacity = e > .02 && e < .98 ? .6 : 0; beam.position.z = -2.5 + e * 5; }
      if (!drag && !reduce) az += .003;
      cam.position.set(Math.sin(az) * 7.5, 4.6, Math.cos(az) * 7.5); cam.lookAt(0, .8, 0);
      r.render(scene, cam);
    }
    state = { r, ro, raf: 0 }; state.raf = requestAnimationFrame(frame); return true;
  }
  window.Mini3D = { mount, unmount, has: id => !!CFG[id], cfg: CFG };
})();
