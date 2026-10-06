/* Interactive "Try it live" mini-demos — all run in the browser, no backend */
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const STOP = new Set('a an the and or of to in on for is are was were be been it its this that with as at by from what when how do does can i you we they my your our their will should would there any which who whom about into than then so if not no yes also have has had'.split(' '));
  const tok = s => (s.toLowerCase().match(/[a-z0-9+#.]+/g) || []).map(w => w.replace(/^[.]+|[.]+$/g, '')).filter(w => w && !STOP.has(w));
  const D = {};

  /* 1 — CityAir: ask questions about Hyderabad's live air */
  D.p1 = el => {
    el.innerHTML = `<p class="t-intro">Ask CityAir about <b>Hyderabad’s air right now</b>. It reads live data and answers in plain language.</p>
      <div class="t-live" id="t1live">Fetching live Hyderabad air quality…</div>
      <div class="chips" id="t1chips">${['Can I go for a run?', 'Do I need a mask?', 'Is it safe for kids?', 'Should I open the windows?', 'How can I help reduce pollution?'].map(q => `<button>${q}</button>`).join('')}</div>
      <div class="chat" id="t1chat"></div>
      <form class="t-row" id="t1f"><input id="t1q" placeholder="Ask anything about the air…" autocomplete="off"><button class="btn solid">Ask</button></form>`;
    let aqi = null, pm = null;
    const L = a => a <= 50 ? ['Good', '#30d158'] : a <= 100 ? ['Moderate', '#ffd60a'] : a <= 150 ? ['Unhealthy for sensitive groups', '#ff9f0a'] : a <= 200 ? ['Unhealthy', '#ff453a'] : a <= 300 ? ['Very unhealthy', '#bf5af2'] : ['Hazardous', '#a2123b'];
    fetch('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=17.385&longitude=78.4867&current=us_aqi,pm2_5&timezone=auto').then(r => r.json()).then(j => { aqi = Math.round(j.current.us_aqi); pm = j.current.pm2_5; const l = L(aqi); $('#t1live').innerHTML = `<b style="color:${l[1]}">AQI ${aqi}</b> · ${l[0]} · PM2.5 ${pm} µg/m³ <small>live · Hyderabad</small>`; say('Can I go for a run?'); }).catch(() => { $('#t1live').textContent = 'Live data unavailable — answers will be general.'; });
    const ans = q => {
      const s = q.toLowerCase(), a = aqi, l = a != null ? L(a)[0].toLowerCase() : null, now = a != null ? `Right now Hyderabad’s AQI is ${a} (${l}). ` : '';
      const bad = a != null && a > 100, worse = a != null && a > 150;
      if (/run|jog|exercis|gym|walk|cycl|sport|play/.test(s)) return now + (a == null ? 'Check the AQI first: below 100 is fine for most people.' : worse ? 'Skip hard outdoor exercise today — move it indoors or to a cleaner hour.' : bad ? 'Light activity is okay, but go easy if you are sensitive to dust or have asthma.' : 'It’s a good time for outdoor exercise. Enjoy it!');
      if (/mask|n95|ffp/.test(s)) return now + (worse ? 'Yes — wear a fitted N95/FFP2 mask outdoors, especially near traffic.' : bad ? 'A mask is a good idea near heavy traffic if you are sensitive; most people can go without.' : 'You don’t need one right now.');
      if (/kid|child|baby|school|elder|old/.test(s)) return now + (worse ? 'Keep children and older adults indoors for strenuous play and limit time outside.' : bad ? 'Short outdoor time is okay, but avoid long strenuous play for young children.' : 'Safe for outdoor play.');
      if (/window|ventilat|fresh/.test(s)) return now + (bad ? 'Keep windows mostly closed during traffic peaks (morning and evening); air the room briefly at quieter hours.' : 'Open them up — fresh air is good.');
      if (/asthma|breath|cough|allerg|health|lung/.test(s)) return now + (bad ? 'People with asthma or heart conditions should reduce time outdoors and keep their medication handy. (General info, not medical advice.)' : 'Conditions are comfortable for most people with breathing issues. (General info, not medical advice.)');
      if (/reduc|help|pollut|improv|tree|vehicle|transport|burn|do/.test(s)) return 'Small actions add up: use public transport, metro or carpool; avoid burning waste or crackers; keep your vehicle serviced; plant and protect trees; and switch off engines at signals.';
      if (/aqi|air|today|quality|now|how/.test(s)) return a != null ? now + 'PM2.5 is ' + pm + ' µg/m³. Ask me about running, masks, kids or windows.' : 'I couldn’t load live data right now — try again in a moment.';
      return now + 'I can help with running, masks, kids, windows, health, or how to reduce pollution. Try one of the suggestions above.';
    };
    const say = (q) => { const c = $('#t1chat'); c.insertAdjacentHTML('beforeend', `<div class="me">${esc(q)}</div><div class="bot">${esc(ans(q))}</div>`); c.scrollTop = c.scrollHeight; };
    $('#t1chips').onclick = e => { if (e.target.tagName === 'BUTTON') say(e.target.textContent); };
    $('#t1f').onsubmit = e => { e.preventDefault(); const v = $('#t1q').value.trim(); if (v) { say(v); $('#t1q').value = ''; } };
  };

  /* 2 — CampusBot: retrieval over any text you paste */
  D.p2 = el => {
    const sample = `Students must maintain at least 75% attendance to be eligible for semester examinations.\nThe library is open from 8:30 AM to 5:30 PM on working days.\nHostel students must return to the hostel before 6:30 PM.\nThe internal assessment marks are awarded for mid-term exams, assignments and lab records.\nScholarship applications must be submitted to the office before the notified last date.\nStudents can collect bonafide certificates from the administrative office after submitting a written request.`;
    el.innerHTML = `<p class="t-intro">Paste any college notice or handbook, then ask a question. CampusBot finds the best passage and cites it — or says it can’t find it.</p>
      <label class="t-lab">Document <small>(sample text — replace with your own)</small></label><textarea id="t2doc" rows="5">${sample}</textarea>
      <form class="t-row" id="t2f"><input id="t2q" placeholder="e.g. What attendance do I need for exams?" autocomplete="off"><button class="btn solid">Ask</button></form>
      <div class="chips" id="t2c">${['What attendance do I need?', 'When is the library open?', 'How do I get a bonafide certificate?'].map(q => `<button>${q}</button>`).join('')}</div>
      <div class="chat" id="t2chat"></div>`;
    const ask = q => {
      const sents = $('#t2doc').value.split(/(?<=[.!?])\s+|\n+/).map(s => s.trim()).filter(s => s.length > 8), qt = tok(q);
      const df = {}; sents.forEach(s => new Set(tok(s)).forEach(w => df[w] = (df[w] || 0) + 1));
      const sc = sents.map((s, i) => { const t = new Set(tok(s)); let v = 0; qt.forEach(w => { if (t.has(w)) v += Math.log(1 + sents.length / df[w]); else if ([...t].some(x => x.length > 3 && (x.startsWith(w.slice(0, 4)) && w.length > 3))) v += .6; }); return { s, i, v }; }).sort((a, b) => b.v - a.v);
      const top = sc[0], c = $('#t2chat'); let out;
      if (!top || top.v < 1.2) out = `<div class="bot">I couldn’t find that in the document, so I won’t guess. Try rephrasing or add the relevant notice.</div>`;
      else out = `<div class="bot">${esc(top.s)}<small class="src">Source · passage ${top.i + 1} of ${sents.length} · confidence ${Math.min(99, Math.round(top.v / (qt.length * 1.6 + .01) * 100))}%</small></div>`;
      c.insertAdjacentHTML('beforeend', `<div class="me">${esc(q)}</div>` + out); c.scrollTop = c.scrollHeight;
    };
    $('#t2c').onclick = e => { if (e.target.tagName === 'BUTTON') ask(e.target.textContent); };
    $('#t2f').onsubmit = e => { e.preventDefault(); const v = $('#t2q').value.trim(); if (v) { ask(v); $('#t2q').value = ''; } };
    ask('What attendance do I need?');
  };

  /* 3 — FaceMark: scan a class, review, export */
  D.p3 = el => {
    const N = 24; const st = Array(N).fill(null);
    el.innerHTML = `<p class="t-intro">Simulated classroom of ${N}. Run a scan to mark attendance automatically, then tap any seat to correct it.</p>
      <div class="seats" id="t3s">${st.map((_, i) => `<button data-i="${i}"><i></i>S${i + 1}</button>`).join('')}</div>
      <div class="t-row"><button class="btn solid" id="t3scan">Scan class</button><button class="btn ghost" id="t3csv">Download CSV</button><span class="t-stat" id="t3stat">Not scanned yet</span></div>`;
    const draw = () => { $$('#t3s button').forEach((b, i) => { b.dataset.s = st[i] == null ? '' : st[i] ? 'p' : 'a'; }); const p = st.filter(x => x).length, d = st.filter(x => x != null).length; $('#t3stat').innerHTML = d ? `<b>${p}/${N}</b> present · ${Math.round(p / N * 100)}%` : 'Not scanned yet'; };
    $('#t3scan').onclick = async () => { $('#t3scan').disabled = true; for (let i = 0; i < N; i++) { st[i] = Math.random() > .1; draw(); await new Promise(r => setTimeout(r, 70)); } $('#t3scan').disabled = false; };
    $('#t3s').onclick = e => { const b = e.target.closest('button'); if (!b) return; const i = +b.dataset.i; st[i] = !st[i]; draw(); };
    $('#t3csv').onclick = () => { const csv = 'Seat,Status\n' + st.map((s, i) => `S${i + 1},${s == null ? 'Not scanned' : s ? 'Present' : 'Absent'}`).join('\n'); const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' })); a.download = 'attendance.csv'; a.click(); };
  };

  /* 4 — ReelPick: like movies, get content-based recommendations */
  D.p4 = el => {
    const M = [['Inception', 'sci-fi thriller'], ['The Dark Knight', 'action crime thriller'], ['Interstellar', 'sci-fi drama adventure'], ['3 Idiots', 'comedy drama'], ['Dangal', 'drama sport'], ['Zindagi Na Milegi Dobara', 'comedy drama adventure'], ['Baahubali', 'action fantasy drama'], ['Dune', 'sci-fi adventure drama'], ['Parasite', 'thriller drama'], ['Spirited Away', 'fantasy animation adventure'], ['Coco', 'animation music family'], ['Avengers: Endgame', 'action sci-fi adventure'], ['Barfi', 'comedy romance drama'], ['Kantara', 'thriller fantasy action'], ['Chhichhore', 'comedy drama'], ['Tumbbad', 'fantasy thriller']];
    const liked = new Set();
    el.innerHTML = `<p class="t-intro">Tap the movies you like. ReelPick compares genres and ranks what to watch next.</p><div class="movies" id="t4m">${M.map((m, i) => `<button data-i="${i}">${m[0]}</button>`).join('')}</div><div class="recs" id="t4r"><p class="t-hint">Pick at least one movie…</p></div>`;
    const vec = g => { const v = {}; g.split(' ').forEach(x => v[x] = 1); return v; }, cos = (a, b) => { let d = 0, na = 0, nb = 0; for (const k in a) { na += a[k] ** 2; if (b[k]) d += a[k] * b[k]; } for (const k in b) nb += b[k] ** 2; return d / (Math.sqrt(na * nb) || 1); };
    const run = () => { if (!liked.size) { $('#t4r').innerHTML = '<p class="t-hint">Pick at least one movie…</p>'; return; } const prof = {}; liked.forEach(i => M[i][1].split(' ').forEach(g => prof[g] = (prof[g] || 0) + 1)); const r = M.map((m, i) => ({ m, i, s: cos(prof, vec(m[1])) })).filter(x => !liked.has(x.i)).sort((a, b) => b.s - a.s).slice(0, 4); $('#t4r').innerHTML = `<h5>Because you liked ${[...liked].map(i => M[i][0]).slice(0, 2).join(', ')}${liked.size > 2 ? '…' : ''}</h5>` + r.map(x => `<div class="rec"><b>${x.m[0]}</b><small>${x.m[1]}</small><div class="meter"><i style="width:${Math.round(x.s * 100)}%"></i></div><em>${Math.round(x.s * 100)}% match</em></div>`).join(''); };
    $('#t4m').onclick = e => { const b = e.target.closest('button'); if (!b) return; const i = +b.dataset.i; liked.has(i) ? liked.delete(i) : liked.add(i); b.setAttribute('aria-pressed', liked.has(i)); run(); };
    liked.add(0); $('#t4m button').setAttribute('aria-pressed', true); run();
  };

  /* 5 — SentiScope: score any text */
  D.p5 = el => {
    const POS = 'good great excellent amazing awesome love loved loving best fantastic happy wonderful perfect helpful nice brilliant superb enjoy enjoyed recommend smooth fast easy beautiful clean friendly fun'.split(' '), NEG = 'bad terrible awful worst hate hated poor slow boring disappointing disappointed broken useless horrible waste rude dirty difficult confusing buggy crash expensive annoying'.split(' ');
    el.innerHTML = `<p class="t-intro">Type or paste any review. SentiScope scores the mood and highlights the words that drove it.</p>
      <textarea id="t5t" rows="3" placeholder="Type a review…">The lectures were great and the lab staff were very helpful, but the wifi is not good and the canteen is slow.</textarea>
      <div class="chips" id="t5c">${['Absolutely loved this app, super easy and fast!', 'Terrible experience, the support was rude and useless.', 'It is okay. Nothing special.'].map(q => `<button>${q}</button>`).join('')}</div>
      <div class="sent"><div class="sbar"><i id="t5i"></i></div><div class="slab"><span>Negative</span><b id="t5l">—</b><span>Positive</span></div></div><p class="hl" id="t5h"></p>`;
    const run = () => {
      const words = $('#t5t').value.match(/[A-Za-z']+|[^A-Za-z']+/g) || []; let score = 0, n = 0, neg = false, boost = 1; const out = [];
      words.forEach((w, i) => { const l = w.toLowerCase(); if (!/[a-z]/.test(l)) { out.push(esc(w)); return; } let v = POS.includes(l) ? 1 : NEG.includes(l) ? -1 : 0;
        if (/^(not|no|never|hardly|isn't|wasn't|don't|didn't)$/.test(l)) { neg = true; out.push(esc(w)); return; } if (/^(very|really|super|extremely|so|absolutely)$/.test(l)) { boost = 1.5; out.push(esc(w)); return; }
        if (v) { if (neg) v = -v; v *= boost; score += v; n++; out.push(`<mark class="${v > 0 ? 'pos' : 'neg'}">${esc(w)}</mark>`); neg = false; boost = 1; } else { out.push(esc(w)); if (/[.,;!?]/.test(w)) neg = false; } });
      $('#t5h').innerHTML = out.join(''); const s = n ? Math.max(-1, Math.min(1, score / Math.max(1.5, n))) : 0, pct = (s + 1) / 2 * 100; $('#t5i').style.left = pct + '%';
      const lab = !n ? 'Neutral' : s > .25 ? 'Positive' : s < -.25 ? 'Negative' : 'Mixed / neutral'; $('#t5l').textContent = lab + (n ? ` (${s > 0 ? '+' : ''}${s.toFixed(2)})` : ''); $('#t5l').style.color = s > .25 ? '#30d158' : s < -.25 ? '#ff453a' : '';
    };
    $('#t5t').oninput = run; $('#t5c').onclick = e => { if (e.target.tagName === 'BUTTON') { $('#t5t').value = e.target.textContent; run(); } }; run();
  };

  /* 6 — LibraryHub: issue, return, fines */
  D.p6 = el => {
    const books = [['Introduction to Algorithms', 'CS'], ['Database System Concepts', 'DBMS'], ['Operating System Concepts', 'OS'], ['Computer Networks', 'CN'], ['Clean Code', 'SE'], ['Artificial Intelligence: A Modern Approach', 'AI'], ['Let Us C', 'C'], ['Head First Java', 'Java']].map(b => ({ t: b[0], c: b[1], d: null }));
    let day = 0;
    el.innerHTML = `<p class="t-intro">Search, issue and return books. Move the day slider to see overdue fines <small>(demo rules: 14-day loan, ₹2 per late day)</small>.</p>
      <div class="t-row"><input id="t6q" placeholder="Search the catalogue…"></div>
      <label class="t-lab">Today is day <b id="t6d">0</b></label><input type="range" id="t6r" min="0" max="40" value="0" class="rng">
      <div class="books" id="t6b"></div>`;
    const draw = () => { const q = $('#t6q').value.toLowerCase(); $('#t6b').innerHTML = books.map((b, i) => ({ b, i })).filter(x => (x.b.t + x.b.c).toLowerCase().includes(q)).map(({ b, i }) => { const due = b.d == null ? null : b.d + 14, late = b.d == null ? 0 : Math.max(0, day - due); return `<div class="book" data-s="${b.d == null ? 'in' : late ? 'late' : 'out'}"><div><b>${b.t}</b><small>${b.c} · ${b.d == null ? 'Available' : late ? `Overdue ${late} day${late > 1 ? 's' : ''} · fine ₹${late * 2}` : `Due day ${due}`}</small></div><button data-i="${i}" class="btn ${b.d == null ? 'solid' : 'ghost'}">${b.d == null ? 'Issue' : 'Return'}</button></div>`; }).join('') || '<p class="t-hint">No matching books.</p>'; };
    $('#t6q').oninput = draw; $('#t6r').oninput = e => { day = +e.target.value; $('#t6d').textContent = day; draw(); };
    $('#t6b').onclick = e => { const b = e.target.closest('button'); if (!b) return; const k = books[+b.dataset.i]; if (k.d == null) k.d = day; else { const late = Math.max(0, day - (k.d + 14)); k.d = null; if (late) toastMsg(`Returned with a fine of ₹${late * 2}`); else toastMsg('Returned — no fine'); } draw(); }; draw();
  };

  /* 7 — ResumeLens: match a resume to a job */
  D.p7 = el => {
    const jd = `We are hiring a Junior AI Engineer. You will build LLM applications with Python, FastAPI and RAG pipelines, work with PostgreSQL and Docker, and write clean, tested code using Git. Knowledge of machine learning, REST APIs and AWS is a plus.`;
    const cv = `Final-year B.Tech CSE student. Built an LLM assistant in Python using embeddings and FAISS. Developed REST APIs with Flask. Experience with MySQL, Git and GitHub. Solid grounding in machine learning and data structures.`;
    el.innerHTML = `<p class="t-intro">Paste a job description and a resume. ResumeLens scores the fit and shows which skills match or are missing.</p>
      <div class="two"><div><label class="t-lab">Job description</label><textarea id="t7j" rows="6">${jd}</textarea></div><div><label class="t-lab">Resume</label><textarea id="t7c" rows="6">${cv}</textarea></div></div>
      <div class="score"><div class="ring"><b id="t7s">0</b><span>% fit</span></div><div class="kw"><h5>Matched</h5><div id="t7m" class="kws"></div><h5>Missing</h5><div id="t7x" class="kws"></div></div></div>`;
    const SYN = { js: 'javascript', ml: 'machine', ai: 'ai', llms: 'llm', apis: 'api', k8s: 'kubernetes', postgres: 'postgresql', reactjs: 'react', nodejs: 'node', ' rest': 'rest' };
    const norm = w => SYN[w] || (w.length > 4 && /s$/.test(w) && !/(ss|us|is)$/.test(w) ? w.slice(0, -1) : w);
    const run = () => { const jt = [...new Set(tok($('#t7j').value).map(norm))].filter(w => w.length > 1 && !/^(hiring|junior|will|plus|write|work|knowledge|experience|using|clean|build|looking|strong|team)$/.test(w)); const ct = new Set(tok($('#t7c').value).map(norm)); const m = jt.filter(w => ct.has(w)), x = jt.filter(w => !ct.has(w)); const pct = jt.length ? Math.round(m.length / jt.length * 100) : 0;
      $('#t7s').textContent = pct; $('.ring').style.setProperty('--p', pct); $('.ring').style.setProperty('--c', pct > 66 ? '#30d158' : pct > 33 ? '#ff9f0a' : '#ff453a');
      $('#t7m').innerHTML = m.map(w => `<span class="ok">${esc(w)}</span>`).join('') || '<em>none yet</em>'; $('#t7x').innerHTML = x.slice(0, 14).map(w => `<span class="no">${esc(w)}</span>`).join('') || '<em>nothing missing 🎉</em>'; };
    $('#t7j').oninput = $('#t7c').oninput = run; run();
  };

  /* 8 — TaskFlow: a working kanban */
  D.p8 = el => {
    let tasks; try { tasks = JSON.parse(localStorage.getItem('tf-tasks') || 'null'); } catch (e) {}
    tasks = tasks || [{ t: 'Finish DSA practice set', s: 0 }, { t: 'Revise DBMS normalisation', s: 1 }, { t: 'Submit lab record', s: 2 }];
    el.innerHTML = `<p class="t-intro">A real mini task board. Add a task, tap a card to move it forward, × to delete. It remembers your tasks on this device.</p>
      <form class="t-row" id="t8f"><input id="t8i" placeholder="Add a task…" autocomplete="off"><button class="btn solid">Add</button></form>
      <div class="kan" id="t8k">${['To do', 'Doing', 'Done'].map((c, i) => `<div class="col" data-c="${i}"><h5>${c} <em></em></h5><div class="cards"></div></div>`).join('')}</div>`;
    const save = () => { try { localStorage.setItem('tf-tasks', JSON.stringify(tasks)); } catch (e) {} };
    const draw = () => { $$('#t8k .col').forEach(col => { const c = +col.dataset.c, l = tasks.map((t, i) => ({ t, i })).filter(x => x.t.s === c); $('em', col).textContent = l.length; $('.cards', col).innerHTML = l.map(x => `<div class="tk" data-i="${x.i}"><span>${esc(x.t.t)}</span><button class="del" data-del="${x.i}" aria-label="Delete">×</button></div>`).join('') || '<p class="t-hint">Empty</p>'; }); };
    $('#t8f').onsubmit = e => { e.preventDefault(); const v = $('#t8i').value.trim(); if (v) { tasks.push({ t: v, s: 0 }); $('#t8i').value = ''; save(); draw(); } };
    $('#t8k').onclick = e => { const d = e.target.closest('[data-del]'); if (d) { tasks.splice(+d.dataset.del, 1); save(); draw(); return; } const t = e.target.closest('.tk'); if (t) { const k = tasks[+t.dataset.i]; k.s = (k.s + 1) % 3; save(); draw(); } }; draw();
  };


  /* 9 — Student Performance: interactive prediction (illustrative fixed-weight model) */
  D.p9 = el => {
    const F = [['study', 'Study hours / day', 0, 10, .5, 4, v => Math.min(v, 8) * 3, 24], ['att', 'Attendance %', 40, 100, 1, 80, v => (v - 40) * .2, 12], ['prev', 'Previous marks %', 30, 100, 1, 65, v => v * .4, 40], ['sleep', 'Sleep hours', 4, 10, .5, 7, v => 5 - Math.abs(v - 7.5) * 2, 5], ['asg', 'Assignments submitted %', 0, 100, 1, 70, v => v * .12, 12]];
    el.innerHTML = `<p class="t-intro">Adjust a student’s habits and see the predicted score update. <small>(Illustrative model with fixed weights — the real project trains a Scikit-learn model on academic data.)</small></p>
      <div class="pred"><div class="pred-in">${F.map(f => `<label class="pr"><span>${f[1]} <b id="v_${f[0]}">${f[5]}</b></span><input type="range" class="rng" id="r_${f[0]}" min="${f[2]}" max="${f[3]}" step="${f[4]}" value="${f[5]}"></label>`).join('')}</div>
      <div class="pred-out"><div class="ring" id="t9ring"><b id="t9s">0</b><span>predicted</span></div><h4 id="t9band"></h4><p id="t9tip" class="t-hint"></p><div id="t9bars" class="cbars"></div></div></div>`;
    const run = () => {
      const val = {}; F.forEach(f => { val[f[0]] = +$('#r_' + f[0]).value; $('#v_' + f[0]).textContent = val[f[0]]; });
      const parts = F.map(f => ({ k: f[1], c: Math.max(0, f[6](val[f[0]])), m: f[7] })); const score = Math.max(0, Math.min(100, 7 + parts.reduce((a, p) => a + p.c, 0)));
      const band = score >= 75 ? ['Distinction', '#30d158'] : score >= 60 ? ['First class', '#64d2ff'] : score >= 40 ? ['Pass', '#ff9f0a'] : ['At risk', '#ff453a'];
      $('#t9s').textContent = Math.round(score); $('#t9ring').style.setProperty('--p', score); $('#t9ring').style.setProperty('--c', band[1]); $('#t9band').textContent = band[0]; $('#t9band').style.color = band[1];
      const lever = parts.map(p => ({ ...p, gap: p.m - p.c })).sort((a, b) => b.gap - a.gap)[0]; $('#t9tip').textContent = `Biggest room to improve: ${lever.k.toLowerCase()}.`;
      $('#t9bars').innerHTML = parts.map(p => `<div><small>${p.k}</small><div class="meter"><i style="width:${Math.round(p.c / p.m * 100)}%"></i></div></div>`).join('');
    };
    $$('.pred input', el).forEach(i => i.oninput = run); run();
  };

  /* 10 — CI/CD pipeline: run it, break the tests, watch the quality gate */
  D.p10 = el => {
    const S = ['Commit', 'Build', 'Test', 'Containerize', 'Deploy']; let ver = 0, busy = false;
    el.innerHTML = `<p class="t-intro">Push a change through a build → test → containerize → deploy pipeline. Break a test and watch the quality gate stop the release.</p>
      <div class="pipe" id="t10p">${S.map((s, i) => `<div class="stage" data-s="idle"><i>${i + 1}</i><b>${s}</b><small>waiting</small></div>`).join('')}</div>
      <div class="t-row"><button class="btn solid" id="t10run">Run pipeline</button><label class="tog"><input type="checkbox" id="t10fail"> Introduce a failing test</label></div>
      <pre class="log" id="t10log">$ ready — click “Run pipeline”</pre>`;
    const MSG = ['git push origin main', 'npm run build — compiled successfully', 'running 24 tests…', 'docker build -t app:latest .', 'deploying to production…'];
    $('#t10run').onclick = async () => {
      if (busy) return; busy = true; const fail = $('#t10fail').checked, st = $$('.stage', el), log = $('#t10log'); log.textContent = ''; st.forEach(s => { s.dataset.s = 'idle'; $('small', s).textContent = 'waiting'; });
      const say = l => { log.textContent += l + '\n'; log.scrollTop = log.scrollHeight; }; const w = ms => new Promise(r => setTimeout(r, ms));
      for (let i = 0; i < S.length; i++) {
        st[i].dataset.s = 'run'; $('small', st[i]).textContent = 'running…'; say('$ ' + MSG[i]); await w(750);
        if (fail && i === 2) { st[i].dataset.s = 'fail'; $('small', st[i]).textContent = 'failed'; say('✗ 2 tests failed (auth.spec, cart.spec)'); say('⛔ Quality gate blocked the release — nothing was deployed.'); for (let k = i + 1; k < S.length; k++) { st[k].dataset.s = 'skip'; $('small', st[k]).textContent = 'skipped'; } busy = false; return; }
        st[i].dataset.s = 'ok'; $('small', st[i]).textContent = 'passed'; say('✓ ' + S[i] + ' passed');
      }
      ver++; say(`🚀 Released v1.0.${ver} to production`); busy = false;
    };
  };

  /* 11 — Forward Deployed Engineering: pain points → tasks → handover notes */
  D.p11 = el => {
    const P = { 'Manual data entry': ['Build a form + validation and import script', 'Forms / CSV import'], 'Slow approvals': ['Add an approval workflow with email/chat notifications', 'Notifications API'], 'Scattered spreadsheets': ['Consolidate sheets into one source of truth', 'Spreadsheet / DB sync'], 'No status visibility': ['Create a live status dashboard', 'Reporting API'], 'Repeated customer emails': ['Automate templated replies for common requests', 'Email API'] };
    const sel = new Set(['Manual data entry', 'Slow approvals']);
    el.innerHTML = `<p class="t-intro">Pick the client’s pain points. See them become technical tasks, a solution flow and handover notes.</p>
      <div class="movies" id="t11c">${Object.keys(P).map(k => `<button aria-pressed="${sel.has(k)}">${k}</button>`).join('')}</div>
      <div class="flow" id="t11f"></div><label class="t-lab">Handover notes <small>(auto-generated)</small></label><textarea id="t11n" rows="7" readonly></textarea><button class="btn ghost" id="t11cp">Copy notes</button>`;
    const run = () => { const k = [...sel]; $('#t11f').innerHTML = k.length ? k.map((x, i) => `<div class="fstep"><span>${i + 1}</span><div><b>${x}</b><small>→ ${P[x][0]} · <em>${P[x][1]}</em></small></div></div>`).join('') : '<p class="t-hint">Select at least one pain point…</p>';
      $('#t11n').value = k.length ? `HANDOVER NOTES — Client Workflow Automation\n\nGoal: remove manual effort and improve visibility.\n\nWhat was built:\n${k.map((x, i) => `${i + 1}. ${P[x][0]}`).join('\n')}\n\nIntegrations: ${[...new Set(k.map(x => P[x][1]))].join(', ')}\n\nHow to support: check logs first, then the workflow settings. Escalate with the steps to reproduce.\nNext steps: gather feedback after 2 weeks and prioritise improvements.` : ''; };
    $('#t11c').onclick = e => { const b = e.target.closest('button'); if (!b) return; const n = b.textContent; sel.has(n) ? sel.delete(n) : sel.add(n); b.setAttribute('aria-pressed', sel.has(n)); run(); };
    $('#t11cp').onclick = () => { navigator.clipboard?.writeText($('#t11n').value); toastMsg('Notes copied ✓'); }; run();
  };

  /* 12 — Responsive portfolio: drag the screen width */
  D.p12 = el => {
    el.innerHTML = `<p class="t-intro">Drag the slider to resize the screen. The layout adapts — this is how the portfolio you’re viewing behaves.</p>
      <label class="t-lab">Screen width: <b id="t12w">640</b>px · <span id="t12d">Tablet</span></label><input type="range" class="rng" id="t12r" min="300" max="900" value="640">
      <div class="rs-wrap"><div class="rs" id="t12f" style="width:640px"><div class="rs-nav"><b>Afreen</b><span class="rs-links"><i>About</i><i>Work</i><i>Contact</i></span><span class="rs-burger">☰</span></div>
        <div class="rs-hero"><h4>Hello, I’m Afreen</h4><p>AI/ML · Software · DevOps</p></div><div class="rs-grid"><div></div><div></div><div></div><div></div></div></div></div>`;
    $('#t12r').oninput = e => { const w = +e.target.value; $('#t12f').style.width = w + 'px'; $('#t12w').textContent = w; $('#t12d').textContent = w < 520 ? 'Phone' : w < 780 ? 'Tablet' : 'Desktop'; };
  };

  const toastMsg = m => { const t = $('#toast'); if (!t) return; t.textContent = m; t.classList.add('on'); clearTimeout(toastMsg.t); toastMsg.t = setTimeout(() => t.classList.remove('on'), 2200); };
  window.TryIt = { mount: (el, id) => D[id] && D[id](el), has: id => !!D[id] };

  /* ---------- Explore checklist (keeps visitors exploring) ---------- */
  const ITEMS = [['tryit', 'Try a project demo', 'Open any project in Selected work'], ['3d', 'Play with the 3D city', 'Clear the smog in the playground'], ['air', 'Check a city’s air', 'Search any city in the live demo'], ['theme', 'Switch light / dark', 'Tap the ◐ button in the top bar'], ['cmd', 'Open the command palette', 'Press Ctrl / ⌘ + K']];
  let done = {}; try { done = JSON.parse(localStorage.getItem('explore') || '{}'); } catch (e) {}
  const pill = document.createElement('div'); pill.className = 'explore'; pill.innerHTML = '<button class="ex-pill" aria-expanded="false"><span class="ex-ring"></span><b>Explore</b><i id="exN"></i></button><div class="ex-panel" hidden><h4>Explore this portfolio</h4><ul></ul><div class="ex-win" hidden><p>🎉 You’ve seen it all. Let’s build something together.</p><button class="btn solid" id="exMail">Copy email</button></div></div>';
  document.body.appendChild(pill);
  const render = () => { const n = ITEMS.filter(i => done[i[0]]).length; $('#exN').textContent = `${n}/${ITEMS.length}`; pill.style.setProperty('--p', n / ITEMS.length); $('ul', pill).innerHTML = ITEMS.map(i => `<li class="${done[i[0]] ? 'ok' : ''}"><span>${done[i[0]] ? '✓' : ''}</span><div><b>${i[1]}</b><small>${i[2]}</small></div></li>`).join(''); $('.ex-win', pill).hidden = n < ITEMS.length; pill.classList.toggle('full', n === ITEMS.length); };
  window.Explore = { mark: k => { $$('.ex-bubble').forEach(b => b.remove()); if (done[k]) return; done[k] = 1; try { localStorage.setItem('explore', JSON.stringify(done)); } catch (e) {} render(); const n = ITEMS.filter(i => done[i[0]]).length; toastMsg(n === ITEMS.length ? '🎉 Explorer complete!' : `Explore ${n}/${ITEMS.length} ✓`); if (n === ITEMS.length) { pill.classList.add('open'); $('.ex-panel', pill).hidden = false; } } };
  $('.ex-pill', pill).onclick = () => { const o = pill.classList.toggle('open'); $('.ex-panel', pill).hidden = !o; $('.ex-pill', pill).setAttribute('aria-expanded', o); };
  $('#exMail', pill).onclick = () => { navigator.clipboard?.writeText((window.DATA && DATA.email) || ''); toastMsg('Email copied ✓'); };
  render();
  // gentle one-time idle nudge
  let nudged = false; try { nudged = sessionStorage.getItem('nudged') === '1'; } catch (e) {}
  if (!nudged) setTimeout(() => {
    if (Object.keys(done).length || $('#modal').classList.contains('on')) return;
    const b = document.createElement('div'); b.className = 'ex-bubble'; b.innerHTML = '<span>👋 Try a live demo — it takes 10 seconds.</span><button>Show me</button><i aria-label="Dismiss">×</i>'; pill.appendChild(b); try { sessionStorage.setItem('nudged', '1'); } catch (e) {}
    $('button', b).onclick = () => { b.remove(); window.lenis ? lenis.scrollTo('#work', { offset: -40 }) : $('#work').scrollIntoView({ behavior: 'smooth' }); };
    $('i', b).onclick = () => b.remove(); setTimeout(() => b.remove(), 14000);
  }, 14000);
})();
