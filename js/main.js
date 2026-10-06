(() => {
const D = window.DATA, $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const fine = matchMedia('(pointer:fine)').matches, reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
const toast = m => { const t = $('#toast'); t.textContent = m; t.classList.add('on'); clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('on'), 2200); };

/* ---------- render content ---------- */
$('#tagline').textContent = D.tagline;
$('#aboutHead').innerHTML = D.aboutHeading.map(l => `<span class="hline">${l}</span>`).join(' ');
$('#aboutParas').innerHTML = D.about.map(p => `<p>${p}</p>`).join('');
$('#facts').innerHTML = D.facts.map(f => `<div><small>${f.k}</small><span>${f.v}</span></div>`).join('');
$('#stats').innerHTML = D.stats.map(s => `<div class="stat"><b data-n="${s.n}" data-s="${s.s}">0</b><span>${s.l}</span></div>`).join('');
$('#socials').innerHTML = [['LinkedIn', D.links.linkedin], ['GitHub', D.links.github], ['LeetCode', D.links.leetcode], ['Resume', D.links.resume]].filter(x => x[1] && x[1] !== '#').map(([n, h]) => `<a href="${h}" target="_blank" rel="noopener">${n} ↗</a>`).join('');
if (D.links.resume && D.links.resume !== '#') $('#resumeBtn').href = D.links.resume; else $('#resumeBtn').style.display = 'none'; $('#mailTxt').textContent = D.email;

// skills — bento grid
const SK_META = { 'GenAI & Agents': ['01', 'Building with LLMs, retrieval and agents.'], 'Machine Learning': ['02', 'Models, data and evaluation.'], 'Full Stack': ['03', 'Interfaces and APIs that ship.'], 'Cloud & DevOps': ['04', 'Deploy, monitor, repeat.'], 'Data & Databases': ['05', 'Storing and shaping data.'], 'CS Fundamentals': ['06', 'The foundation under everything.'] };
$('#skillTabs').style.display = 'none';
$('#skillGrid').className = 'bento';
$('#skillGrid').innerHTML = Object.keys(D.skills).map((c, i) => `<article class="bcard b${i}" style="animation-delay:${i * 70}ms"><small>${SK_META[c] ? SK_META[c][0] : i + 1}</small><h3>${c}</h3><p>${SK_META[c] ? SK_META[c][1] : ''}</p><div class="bchips">${D.skills[c].map(([n]) => `<span>${n}</span>`).join('')}</div></article>`).join('');

// experience
$('#expList').innerHTML = D.experience.map((x, i) => `<button class="exp-item${i ? '' : ' on'}" data-i="${i}">${x.tab}${D.showSampleBadges && x.sample ? '<i class="smp">Sample</i>' : ''}<small>${x.org} · ${x.when}</small></button>`).join('');
$('#expPanels').innerHTML = D.experience.map((x, i) => `<div class="panel${i ? '' : ' on'}"><h3>${x.role}</h3><div class="org">${x.org}</div><div class="meta">${x.when} · ${x.type}</div><div class="pills">${x.tags.map(t => `<span>${t}</span>`).join('')}</div><p class="intro">${x.intro}</p><ul>${x.points.map(p => `<li><b>${p[0]}</b>${p[1]}</li>`).join('')}</ul></div>`).join('');
$('#expList').onclick = e => { const b = e.target.closest('.exp-item'); if (!b) return; $$('.exp-item').forEach(x => x.classList.remove('on')); $$('.panel').forEach(x => x.classList.remove('on')); b.classList.add('on'); $$('.panel')[b.dataset.i].classList.add('on'); };

// education
$('#edu').innerHTML = D.education.map(e => `<div><small>${e.when}</small><b>${e.deg}</b><p>${e.org} — ${e.note}</p></div>`).join('');
$('#ach').innerHTML = D.achievements.map(a => `<li>${a}</li>`).join('');

// projects
const pc = ['All', ...new Set(D.projects.map(p => p.cat))];
$('#projTabs').innerHTML = pc.map((c, i) => `<button class="tab${i ? '' : ' on'}" data-c="${c}">${c}</button>`).join('');
const triedBefore = () => { try { return localStorage.getItem('tried') === '1'; } catch (e) { return false; } };
function showProj(c) {
  $('#projGrid').innerHTML = D.projects.filter(p => c === 'All' || p.cat === c).map(p => `<button class="card${p.featured ? ' feat' : ''}" data-id="${p.id}"><div class="art" style="--h:${p.hue}" data-n="${p.name[0]}"><span>${p.cat} · ${p.year}</span>${p.featured ? '<span class="flag">Flagship</span>' : ''}</div><div class="more">↗</div><div class="card-b"><small>${p.sub.toUpperCase()}</small><h3>${p.name}${D.showSampleBadges && p.sample ? '<i class="smp">Sample</i>' : ''}</h3><p>${p.tag || p.desc}</p><span class="try"><svg width="10" height="12" viewBox="0 0 10 12" fill="currentColor"><path d="M0 0l10 6-10 6z"/></svg>Try it live</span></div></button>`).join('');
  if (!triedBefore()) { const f = $('#projGrid .card'); f && f.classList.add('nudge'); }
  if (window.gsap) gsap.from('#projGrid .card', { y: 40, opacity: 0, duration: .7, stagger: .08, ease: 'power3.out' });
  }
$('#projTabs').onclick = e => { const b = e.target.closest('.tab'); if (!b) return; $$('#projTabs .tab').forEach(t => t.classList.remove('on')); b.classList.add('on'); showProj(b.dataset.c); };
function _unused() { if (!fine) return; $$('.card').forEach(c => { c.onmousemove = e => { const r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; c.style.transform = `perspective(900px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg) translateY(-6px)`; }; c.onmouseleave = () => c.style.transform = ''; }); }
$('#projGrid').onclick = e => {
  const c = e.target.closest('.card'); if (!c) return; const p = D.projects.find(x => x.id === c.dataset.id);
  try { localStorage.setItem('tried', '1'); } catch (er) {} $$('.card.nudge').forEach(x => x.classList.remove('nudge'));
  const m3 = p.id === 'p1' ? '<p class="t-intro">See how the idea works for the whole city, in 3D.</p><button class="btn solid" id="goPg">Open the 3D playground ↓</button>' : (window.Mini3D && Mini3D.has(p.id) ? `<div class="m3d" id="m3d"><canvas></canvas><div class="m3d-ui"><div class="seg"><button data-m="0">Without ${p.name}</button><button data-m="1">With ${p.name}</button></div><p class="m3d-cap"></p></div><span class="m3d-hint">3D · drag to rotate · illustrative</span></div>` : '');
  $('#modalCard').innerHTML = `<div class="art" style="--h:${p.hue}" data-n="${p.name[0]}"><span>${p.cat} · ${p.year}</span><button class="x" id="mx" aria-label="Close">×</button></div><div class="mb"><h3>${p.name} <em>— ${p.sub}</em></h3><p class="mtag">${p.tag || p.desc}</p>
    <div class="mtabs" role="tablist"><button data-t="try" class="on">Try it live</button><button data-t="3d">How it helps · 3D</button><button data-t="case">Case study</button></div>
    <div class="mpane" data-pane="try"></div><div class="mpane" data-pane="3d" hidden>${m3}</div>
    <div class="mpane" data-pane="case" hidden><div class="pills" style="margin-top:6px">${p.stack.map(s => `<span>${s}</span>`).join('')}</div><h4>Problem</h4><p>${p.problem}</p><h4>Solution</h4><p>${p.solution}</p><h4>Impact</h4><p>${p.impact}</p>${p.live !== '#' || p.repo !== '#' ? `<div class="cta">${p.live !== '#' ? `<a class="btn solid" href="${p.live}" target="_blank" rel="noopener">Live demo ↗</a>` : ''}${p.repo !== '#' ? `<a class="btn ghost" href="${p.repo}" target="_blank" rel="noopener">Source code ↗</a>` : ''}</div>` : ''}</div></div>`;
  $('#modal').classList.add('on'); lastFocus = document.activeElement; if (window.lenis) lenis.stop(); document.body.style.overflow = 'hidden'; $('#mx').onclick = closeModal; $('#mx').focus();
  const tryPane = $('.mpane[data-pane=try]'); if (window.TryIt && TryIt.has(p.id)) { TryIt.mount(tryPane, p.id); tryPane.addEventListener('input', () => window.Explore && Explore.mark('tryit')); tryPane.addEventListener('click', e => { if (e.target.closest('button')) window.Explore && Explore.mark('tryit'); }); }
  $$('.mtabs button').forEach(b => b.onclick = () => { $$('.mtabs button').forEach(x => x.classList.toggle('on', x === b)); $$('.mpane').forEach(x => x.hidden = x.dataset.pane !== b.dataset.t); if (window.Mini3D) { Mini3D.unmount(); if (b.dataset.t === '3d' && $('#m3d')) { Mini3D.mount($('#m3d'), p.id); $('#m3d').addEventListener('click', ev => { if (ev.target.closest('[data-m]')) window.Explore && Explore.mark('3d'); }); } } });
  if ($('#goPg')) $('#goPg').onclick = () => { closeModal(); setTimeout(() => window.lenis ? lenis.scrollTo('#playground', { offset: -60 }) : $('#playground').scrollIntoView({ behavior: 'smooth' }), 250); };
};
let lastFocus = null;
const closeModal = () => { if (!$('#modal').classList.contains('on')) return; $('#modal').classList.remove('on'); if (window.Mini3D) Mini3D.unmount(); if (window.lenis) lenis.start(); document.body.style.overflow = ''; if (lastFocus && lastFocus.focus) lastFocus.focus(); };
$('#modal').onclick = e => { if (e.target.id === 'modal') closeModal(); };
if (pc.length <= 2) $('#projTabs').style.display = 'none';
showProj('All');
if ('IntersectionObserver' in window && !triedBefore()) new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { o.disconnect(); setTimeout(() => { if (!triedBefore()) toast('👆 Tap any project — each one is a working demo'); }, 900); } }, { threshold: .5 }).observe($('#projGrid .card'));

/* ---------- terminal typing ---------- */
const term = $('#term'); let termDone = false;
function runTerm() {
  if (termDone) return; termDone = true;
  const lines = D.now.map(n => `<div class="t-cmd"><span class="p">→</span> ${n.cmd} <span class="n">${n.name}</span> <span class="f">${n.flags}</span></div><div class="t-out"><b>${n.title}</b>${n.text}<br><span class="t-st">${n.status}</span></div>`);
  lines.push(`<div class="t-cmd"><span class="p">$</span> open to opportunities<i class="caret"></i></div>`);
  let i = 0; const next = () => { if (i < lines.length) { term.insertAdjacentHTML('beforeend', lines[i++]); if (window.gsap) gsap.from(term.lastElementChild.previousElementSibling || term.lastElementChild, { opacity: 0, x: -10, duration: .5 }); setTimeout(next, 650); } }; next();
}

/* ---------- typed roles ---------- */
(function () { let r = 0, c = 0, del = false; const el = $('#typed');
  (function tick() { const w = D.roles[r]; c += del ? -1 : 1; el.textContent = w.slice(0, c);
    let t = del ? 40 : 85; if (!del && c === w.length) { del = true; t = 1500; } else if (del && c === 0) { del = false; r = (r + 1) % D.roles.length; t = 300; } setTimeout(tick, t); })(); })();

/* ---------- theme / nav / photo / contact ---------- */
const root = document.documentElement; try { const s = localStorage.getItem('theme'); if (s) root.dataset.theme = s; } catch (e) {}
const toggleTheme = () => { const t = root.dataset.theme === 'dark' ? 'light' : 'dark'; root.dataset.theme = t; try { localStorage.setItem('theme', t); } catch (e) {} toast(t + ' mode'); window.Explore && Explore.mark('theme'); };
$('#themeBtn').onclick = toggleTheme;
$('#burger').onclick = () => $('#links').classList.toggle('open');
$$('#links a').forEach(a => a.addEventListener('click', () => $('#links').classList.remove('open')));
if ($('#photo')) $('#photo').onchange = e => { const f = e.target.files[0]; if (!f) return; const r = new FileReader(); r.onload = ev => { $('#photoImg').src = ev.target.result; $('#photoImg').style.display = 'block'; }; r.readAsDataURL(f); };
const copyMail = () => { navigator.clipboard?.writeText(D.email); toast('Email copied ✓'); };
$('#mailBtn').onclick = copyMail;
$('#form').onsubmit = e => { e.preventDefault(); const f = new FormData(e.target); location.href = `mailto:${D.email}?subject=${encodeURIComponent('Portfolio message from ' + f.get('n'))}&body=${encodeURIComponent(f.get('m') + '\n\n— ' + f.get('n') + ' (' + f.get('e') + ')')}`; toast('Opening your mail app…'); };

/* ---------- command palette ---------- */
const go = id => () => { closePal(); window.lenis ? lenis.scrollTo(id) : $(id).scrollIntoView({ behavior: 'smooth' }); };
const cmds = [
  ...[['About', '#about'], ['Skills', '#skills'], ['Experience', '#experience'], ['Projects', '#work'], ['Education', '#education'], ['Contact', '#contact']].map(([n, id]) => [`Go to ${n}`, 'navigate', go(id)]),
  ['Toggle dark / light', 'theme', () => { closePal(); toggleTheme(); }], ['Copy email', 'action', () => { closePal(); copyMail(); }],
  
  ...D.projects.map(p => [`Project: ${p.name}`, p.sub, () => { closePal(); go('#work')(); setTimeout(() => $(`.card[data-id=${p.id}]`)?.click(), 700); }])
];
let sel = 0, shown = cmds;
const renderPal = () => { $('#palList').innerHTML = shown.map((c, i) => `<li class="${i === sel ? 'sel' : ''}" data-i="${i}">${c[0]}<small>${c[1]}</small></li>`).join(''); };
const openPal = () => { window.Explore && Explore.mark('cmd'); $('#palette').classList.add('on'); $('#palIn').value = ''; shown = cmds; sel = 0; renderPal(); setTimeout(() => $('#palIn').focus(), 50); };
const closePal = () => $('#palette').classList.remove('on');
$('#openPalette').onclick = openPal;
$('#palIn').oninput = e => { const q = e.target.value.toLowerCase(); shown = cmds.filter(c => (c[0] + c[1]).toLowerCase().includes(q)); sel = 0; renderPal(); };
$('#palList').onclick = e => { const li = e.target.closest('li'); if (li) shown[li.dataset.i][2](); };
$('#palette').onclick = e => { if (e.target.id === 'palette') closePal(); };
addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); $('#palette').classList.contains('on') ? closePal() : openPal(); return; }
  if (e.key === 'Escape') { closePal(); closeModal(); }
  if ($('#palette').classList.contains('on')) {
    if (e.key === 'ArrowDown') { sel = (sel + 1) % shown.length; renderPal(); e.preventDefault(); }
    if (e.key === 'ArrowUp') { sel = (sel - 1 + shown.length) % shown.length; renderPal(); e.preventDefault(); }
    if (e.key === 'Enter' && shown[sel]) shown[sel][2]();
  }
});

/* ---------- smooth scroll, progress, cursor, magnet ---------- */
try { window.lenis = new Lenis({ duration: 1.2 }); const raf = t => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); lenis.on('scroll', () => window.ScrollTrigger && ScrollTrigger.update()); } catch (e) {}
const nav = $('#nav'), secs = $$('section[id]');
addEventListener('scroll', () => {
  const h = document.documentElement; nav.classList.toggle('stuck', scrollY > 60);
  let cur = ''; secs.forEach(s => { if (scrollY + innerHeight * .4 >= s.offsetTop) cur = s.id; }); $$('#links a').forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + cur));
}, { passive: true });

/* ---------- live air-quality demo (Open-Meteo, no key) ---------- */
(() => {
  const el = $('#aq'); if (!el) return;
  const LV = [
    [50, 'Good', '#30d158', 'Air quality is satisfying and poses little or no risk.', ['Great day to be outdoors — walk, run or cycle.', 'Open windows to let fresh air in.']],
    [100, 'Moderate', '#ffd60a', 'Acceptable, but unusually sensitive people may notice effects.', ['Most people can carry on as normal.', 'If you are sensitive to dust, keep outdoor exercise lighter.']],
    [150, 'Unhealthy for sensitive groups', '#ff9f0a', 'Children, older adults and people with asthma or heart conditions should take care.', ['Sensitive groups: shorten or move strenuous activity indoors.', 'Prefer a mask (N95/FFP2) in heavy traffic.', 'Choose public transport or carpooling to cut your own emissions.']],
    [200, 'Unhealthy', '#ff453a', 'Everyone may begin to feel health effects.', ['Limit prolonged outdoor exertion.', 'Keep windows closed during peak traffic hours.', 'Wear an N95/FFP2 mask outdoors; use an air purifier indoors if you can.']],
    [300, 'Very unhealthy', '#bf5af2', 'Health alert: serious effects are more likely for everyone.', ['Stay indoors and avoid outdoor exercise.', 'Run a purifier and seal gaps if possible.', 'Avoid burning waste, wood or crackers — it makes the air worse.']],
    [Infinity, 'Hazardous', '#a2123b', 'Emergency conditions: the whole population is likely affected.', ['Stay indoors with windows shut.', 'Wear a fitted N95/FFP2 mask if you must go out.', 'Follow local authority advice.']]
  ];
  const lvl = a => LV.find(l => a <= l[0]);
  const P = [['pm2_5', 'PM2.5'], ['pm10', 'PM10'], ['nitrogen_dioxide', 'NO₂'], ['ozone', 'O₃'], ['sulphur_dioxide', 'SO₂'], ['carbon_monoxide', 'CO']];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const draw = (place, j) => {
    const c = j.current, aqi = Math.round(c.us_aqi); window.CITY_AQI = aqi; window.dispatchEvent(new Event('cityaqi')); const  L = lvl(aqi), R = 88, C = 2 * Math.PI * R, pct = Math.min(aqi, 300) / 300;
    const now = new Date(c.time).getTime(), hrs = j.hourly.time.map((t, i) => [new Date(t).getTime(), j.hourly.us_aqi[i]]).filter(x => x[0] >= now && x[1] != null).slice(0, 24);
    const mx = Math.max(...hrs.map(x => x[1]), 50);
    el.innerHTML = `<div class="aq-main">
      <div class="aq-ring"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="${R}" class="trk"/><circle cx="100" cy="100" r="${R}" class="val" id="aqVal" stroke="${L[2]}" stroke-dasharray="${C}" stroke-dashoffset="${C}" data-to="${C * (1 - pct)}"/></svg>
        <div class="aq-num"><b id="aqNum">0</b><span>US AQI</span></div></div>
      <div class="aq-info"><small>${esc(place)}</small><h3 style="color:${L[2]}">${L[1]}</h3><p>${L[3]}</p>
        <ul>${L[4].map(t => `<li>${t}</li>`).join('')}</ul></div></div>
      <div class="aq-pol">${P.map(([k, n]) => `<div><small>${n}</small><b>${c[k] != null ? Math.round(c[k] * 10) / 10 : '–'}</b><span>µg/m³</span></div>`).join('')}</div>
      <div class="aq-fc"><small>NEXT 24 HOURS</small><div class="bars">${hrs.map(([t, v]) => `<i title="${new Date(t).getHours()}:00 — AQI ${Math.round(v)}" style="height:${Math.max(6, v / mx * 100)}%;background:${lvl(v)[2]}"></i>`).join('')}</div></div>`;
    requestAnimationFrame(() => requestAnimationFrame(() => { const v = $('#aqVal'); if (v) v.style.strokeDashoffset = v.dataset.to; }));
    const n = $('#aqNum'); if (!n) return; const t0 = performance.now(); (function tick(t) { if (!n.isConnected) return; const p = Math.min(1, (t - t0) / 1100); n.textContent = Math.round(aqi * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(tick); })(t0);
  };
  const fail = m => el.innerHTML = `<p class="aq-empty">${m}</p>`;
  let reqId = 0;
  const load = async (lat, lon, place) => {
    const my = ++reqId;
    try {
      const r = await fetch(`https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${lat}&longitude=${lon}&current=us_aqi,pm10,pm2_5,nitrogen_dioxide,ozone,sulphur_dioxide,carbon_monoxide&hourly=us_aqi&forecast_days=2&timezone=auto`);
      const j = await r.json(); if (my !== reqId) return; if (!j.current || j.current.us_aqi == null) return fail('No air-quality data for that location yet.'); draw(place, j);
    } catch (e) { fail('Could not reach the data service. Check your connection and try again.'); }
  };
  const search = async q => {
    el.innerHTML = '<p class="aq-empty">Fetching live data…</p>';
    try { const g = await (await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(q)}&count=1`)).json(); const r = g.results && g.results[0]; if (!r) return fail('City not found — try another spelling.'); load(r.latitude, r.longitude, [r.name, r.admin1, r.country].filter(Boolean).join(', ')); } catch (e) { fail('Could not reach the data service.'); }
  };
  $('#aqForm').onsubmit = e => { e.preventDefault(); window.Explore && Explore.mark('air'); const q = $('#aqCity').value.trim(); if (q) search(q); };
  $('#aqLocate').onclick = () => { if (!navigator.geolocation) return fail('Location is not available in this browser.'); el.innerHTML = '<p class="aq-empty">Finding you…</p>'; navigator.geolocation.getCurrentPosition(p => load(p.coords.latitude, p.coords.longitude, 'Your location'), () => fail('Location permission was denied — search a city instead.')); };
  let started = false; const go = () => { if (!started) { started = true; search($('#aqCity').value); } };
  if ('IntersectionObserver' in window) new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { go(); o.disconnect(); } }, { rootMargin: '300px' }).observe(el); else go();
})();

/* ---------- animations ---------- */
function intro() {
  if (!window.gsap || reduce) { $$('.reveal').forEach(e => { e.style.transform = 'none'; e.style.opacity = 1; }); runTerm(); return; }
  gsap.registerPlugin(ScrollTrigger);
  gsap.to('.reveal', { opacity: 1, y: 0, duration: 1, stagger: .12, ease: 'power3.out', delay: .2 });
  gsap.utils.toArray('.h2,.label,.lead,.big,.ed,.paras').forEach(el => gsap.from(el, { y: 50, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%' } }));
  gsap.utils.toArray('.sk,.facts div,.stat,.tl div,.ach li,.exp-item').forEach(el => gsap.from(el, { y: 30, opacity: 0, duration: .8, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 92%' } }));
  // Apple-style scroll choreography (minimal)
  gsap.to('.hero-stage', { opacity: 0, y: -70, scale: .94, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom 25%', scrub: true } });
  gsap.to('.cue', { opacity: 0, scrollTrigger: { trigger: '.hero', start: 'top top', end: '+=160', scrub: true } });
  gsap.fromTo('.portrait', { scale: .9, borderRadius: 48 }, { scale: 1, borderRadius: 28, ease: 'none', scrollTrigger: { trigger: '.portrait', start: 'top 95%', end: 'top 45%', scrub: true } });
  gsap.fromTo('.portrait img', { scale: 1.18 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: '.portrait', start: 'top bottom', end: 'bottom 35%', scrub: true } });
  gsap.utils.toArray('.sec .h2').forEach(h => gsap.fromTo(h, { letterSpacing: '-.02em' }, { letterSpacing: '-.045em', ease: 'none', scrollTrigger: { trigger: h, start: 'top 95%', end: 'top 55%', scrub: true } }));
  ScrollTrigger.create({ trigger: '.term', start: 'top 75%', once: true, onEnter: runTerm });
  ScrollTrigger.create({ trigger: '.stats', start: 'top 85%', once: true, onEnter: () => $$('.stat b').forEach(b => gsap.to({ v: 0 }, { v: +b.dataset.n, duration: 2, ease: 'power2.out', onUpdate() { b.textContent = Math.round(this.targets()[0].v) + b.dataset.s; } })) });
}
addEventListener('load', intro);
setTimeout(() => $$('.reveal').forEach(e => { if (+getComputedStyle(e).opacity < .99 && scrollY < 50) { e.style.opacity = 1; e.style.transform = 'none'; } }), 4500);

})();
