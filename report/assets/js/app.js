/* ============================================================
   LLM From Scratch, Portal app logic
   Phụ thuộc: weeks-data.js (PHASES, WEEKS_DATA), quiz-data.js (QUIZ_DATA),
              advanced-data.js (ADVANCED_TOPICS), Chart.js, MathJax
   ============================================================ */
const PHASES = window.PHASES;
const WEEKS  = window.WEEKS_DATA;
const QUIZ   = (window.QUIZ_DATA && window.QUIZ_DATA.weeks) || [];
const ADV    = window.ADVANCED_TOPICS || [];
const PHASE_VAR = {0:'var(--p0)',1:'var(--p1)',2:'var(--p2)',3:'var(--p3)'};
function icon(name, cls=''){ return `<svg class="ic ${cls}" aria-hidden="true"><use href="#i-${name}"/></svg>`; }
const LETTERS = ['A','B','C','D','E','F'];

/* ---------------- helpers ---------------- */
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function quizFor(n){const w=QUIZ.find(x=>x.week===n);return w?w.questions:[];}

/* ---------------- progress state ---------------- */
const LS_KEY = "llm_scratch_progress_v2";
const LS_KEY_V1 = "llm_scratch_progress_v1";
let state = {};
try { state = JSON.parse(localStorage.getItem(LS_KEY) || "{}"); } catch(e){ state = {}; }
/* Lộ trình mở từ 15 lên 18 tuần ngày 2026-09-04: tuần cũ N thành tuần N+3.
   Tiến độ đã tick theo khóa v1 được chuyển sang khóa v2 một lần, rồi bỏ khóa cũ. */
try {
  const old = localStorage.getItem(LS_KEY_V1);
  if (old && !localStorage.getItem(LS_KEY)) {
    const v1 = JSON.parse(old);
    for (const k in v1) { const m = /^w(\d+)_(\d+)$/.exec(k); if (m) state["w" + (+m[1] + 3) + "_" + m[2]] = v1[k]; }
    localStorage.setItem(LS_KEY, JSON.stringify(state));
    localStorage.removeItem(LS_KEY_V1);
  }
} catch(e){}
function keyOf(w,i){ return "w"+w+"_"+i; }
function save(){ try{localStorage.setItem(LS_KEY, JSON.stringify(state));}catch(e){} }

/* ---------------- progress calc ---------------- */
function weekProgress(w){
  const total = w.check.length; let done = 0;
  for(let i=0;i<total;i++){ if(state[keyOf(w.n,i)]) done++; }
  return {done,total,pct: total? Math.round(done/total*100):0};
}
function weekStatus(w){
  const p = weekProgress(w);
  if(p.pct===0) return {cls:'idle',label:'Chưa bắt đầu'};
  if(p.pct===100) return {cls:'done',label:'Hoàn thành'};
  return {cls:'prog',label:'Đang học'};
}


/* ---------------- theory notes (nhúng, render lazy) ---------------- */
const THEORY = window.THEORY_DATA || {};
function renderTheoryBlock(n){
  const t = THEORY[n];
  if(!t) return '';
  return `
    <div class="theory" data-theory="${n}">
      <button class="theory-head" type="button" aria-expanded="false" onclick="toggleTheory(this)">
        ${icon('book','sm')}<span class="theory-title">Ghi chú lý thuyết đầy đủ</span>
        <span class="theory-meta">${t.words.toLocaleString('vi-VN')} từ, nguồn <code>${t.file}</code></span>
        <span class="caret">${icon('chevron')}</span>
      </button>
      <div class="theory-body"><div class="theory-inner prose" data-rendered="0"></div></div>
    </div>`;
}
function rewriteRelativeLinks(root, n){
  const weekDir = `../Week-${String(n).padStart(2,'0')}/`;
  root.querySelectorAll('a[href]').forEach(a=>{
    const h = a.getAttribute('href');
    if(/^(https?:|mailto:|#)/.test(h)) { if(/^https?:/.test(h)) { a.target='_blank'; a.rel='noopener'; } return; }
    a.setAttribute('href', h.startsWith('../') ? h : weekDir + h);
  });
}
function toggleTheory(head){
  const box = head.closest('.theory');
  const body = box.querySelector('.theory-body');
  const inner = box.querySelector('.theory-inner');
  const n = +box.dataset.theory;
  if(inner.dataset.rendered !== '1'){
    const md = (THEORY[n] && THEORY[n].markdown) || '';
    if(window.marked && typeof marked.parse === 'function'){
      inner.innerHTML = marked.parse(md, {gfm:true, breaks:false});
    } else {
      const pre = document.createElement('pre'); pre.textContent = md; inner.appendChild(pre);
    }
    rewriteRelativeLinks(inner, n);
    inner.dataset.rendered = '1';
    typesetMath(inner);
  }
  const open = box.classList.toggle('open');
  head.setAttribute('aria-expanded', open ? 'true' : 'false');
  body.style.maxHeight = open ? 'none' : '0';
  refitWeekBody(box);
}

/* ---------------- render quiz block ---------------- */
function renderQuizBlock(n){
  const all = quizFor(n);
  if(!all.length) return '';
  const qs = [...all.filter(q=>q.level!=='advanced'), ...all.filter(q=>q.level==='advanced')];
  const nAdv = all.filter(q=>q.level==='advanced').length;
  const items = qs.map((q,i)=>{
    const isMcq = q.type==='mcq';
    let choices='';
    if(isMcq){
      choices = `<ul class="qa-choices">${q.choices.map((c,j)=>
        `<li data-ci="${j}"><span class="ltr">${LETTERS[j]}.</span><span>${esc(c)}</span></li>`).join('')}</ul>`;
    }
    let ansHtml;
    if(isMcq){
      ansHtml = `<div class="ans"><b>Đáp án: ${LETTERS[q.answer]}.</b> ${esc(q.choices[q.answer])}</div>`;
    } else {
      ansHtml = `<div class="ans"><b>Trả lời mẫu:</b> ${esc(q.answer)}</div>`;
    }
    const expl = q.explain ? `<div class="expl"><b>Giải thích:</b> ${esc(q.explain)}</div>` : '';
    return `
      <div class="qa${q.level==='advanced'?' adv':''}" data-qa="${n}-${i}">
        <div class="qa-q" onclick="toggleQA(this)">
          <span class="qa-num">${i+1}</span>
          <div class="qa-qtext">
            <div class="qt">${esc(q.q)}</div>
            <div class="qa-type">${isMcq?'Trắc nghiệm':'Tự luận'}${q.level==='advanced'?' <span class="qa-adv">Nâng cao</span>':''}</div>
            ${choices}
          </div>
          <button class="qa-flipbtn" type="button">Xem đáp án</button>
        </div>
        <div class="qa-a"><div class="qa-a-inner">${ansHtml}${expl}</div></div>
      </div>`;
  }).join('');
  return `
    <div class="quiz">
      <h4>${icon('help','sm')}Quiz tự kiểm tra, ${qs.length} câu${nAdv?` (${nAdv} nâng cao)`:''}</h4>
      <div class="quiz-meta">Bấm vào câu hỏi (hoặc nút) để lật đáp án. File gốc: <code>Week-${String(n).padStart(2,'0')}/quiz.md</code> &amp; <code>quiz_solution.md</code>.</div>
      <div class="quiz-actions">
        <button class="btn" type="button" onclick="flipAllQuiz(${n},true)">Hiện tất cả đáp án</button>
        <button class="btn" type="button" onclick="flipAllQuiz(${n},false)">Ẩn tất cả</button>
      </div>
      ${items}
    </div>`;
}

function toggleQA(head){
  const qa = head.closest('.qa');
  const body = qa.querySelector('.qa-a');
  const open = qa.classList.toggle('flip');
  body.style.maxHeight = open ? body.scrollHeight+'px' : '0';
  const btn = qa.querySelector('.qa-flipbtn');
  if(btn) btn.textContent = open ? 'Ẩn đáp án' : 'Xem đáp án';
  // highlight correct mcq choice
  const allq = quizFor(+qa.dataset.qa.split('-')[0]);
  const ordered = [...allq.filter(x=>x.level!=='advanced'), ...allq.filter(x=>x.level==='advanced')];
  const q = ordered[+qa.dataset.qa.split('-')[1]];
  if(q && q.type==='mcq'){
    qa.querySelectorAll('.qa-choices li').forEach(li=>{
      li.classList.toggle('correct', open && (+li.dataset.ci===q.answer));
    });
  }
  // keep parent week body height correct
  refitWeekBody(qa);
}
function flipAllQuiz(n,val){
  document.querySelectorAll(`.qa[data-qa^="${n}-"]`).forEach(qa=>{
    const open = qa.classList.contains('flip');
    if(open!==val){ toggleQA(qa.querySelector('.qa-q')); }
  });
}
function refitWeekBody(node){
  const wk = node.closest('.week');
  if(wk && wk.classList.contains('open')){ const b=wk.querySelector('.wk-body'); b.style.maxHeight='none'; }
}

/* ---------------- render weeks ---------------- */
function renderWeeks(filter='all'){
  const host = document.getElementById('weeks-list');
  host.innerHTML = '';
  WEEKS.filter(w=> filter==='all' || w.phase==+filter).forEach(w=>{
    const p = weekProgress(w), col = PHASE_VAR[w.phase], st = weekStatus(w);
    const el = document.createElement('div');
    el.className = 'week p'+w.phase;
    el.dataset.week = w.n;
    el.innerHTML = `
      <button class="wk-head" type="button" aria-expanded="false" onclick="toggleWeek(this)">
        <div class="wk-num"><small>TUẦN</small><b>${w.n}</b></div>
        <div class="wk-titles">
          <h3>${w.title}</h3>
          <div class="meta"><span>${icon('clock','sm')}${w.dur}</span><span>${icon('cpu','sm')}${w.hw}</span><span>${icon('help','sm')}${quizFor(w.n).length} câu quiz</span></div>
        </div>
        <div class="wk-right">
          <div class="wk-mini">
            <div class="lbl">${p.done}/${p.total}</div>
            <div class="bar"><i data-wbar="${w.n}" style="background:${col}"></i></div>
          </div>
          <span class="badge ${st.cls}" data-wbadge="${w.n}">${st.label}</span>
          <span class="caret">${icon('chevron')}</span>
        </div>
      </button>
      <div class="wk-body">
        <div class="wk-inner">
          <div class="wk-grid">
            <div class="block">
              <h4>${icon('target','sm')}Mục tiêu</h4>
              <ul class="obj-list">${w.obj.map(o=>`<li>${o}</li>`).join('')}</ul>
              <h4 class="gap">${icon('package','sm')}Deliverable</h4>
              <div class="deliver">${w.deliver}</div>
            </div>
            <div class="block">
              <h4>${icon('book','sm')}Nguồn học</h4>
              <div class="src-list">${w.src.map(s=>`<div class="s">${s}</div>`).join('')}</div>
            </div>
          </div>
          <div class="know">
            <h4>${icon('sigma','sm')}Tóm tắt kiến thức</h4>
            ${w.know}
          </div>
          ${renderTheoryBlock(w.n)}
          ${renderQuizBlock(w.n)}
          <div class="checklist">
            <h4>${icon('check-square','sm')}Checklist tiến độ</h4>
            <div class="cl-items">
              ${w.check.map((c,i)=>`
                <label class="cl">
                  <input type="checkbox" data-w="${w.n}" data-i="${i}" ${state[keyOf(w.n,i)]?'checked':''}/>
                  <span>${c}</span>
                </label>`).join('')}
            </div>
            <div class="wk-actions">
              <button class="btn" type="button" onclick="markAll(${w.n},true)">${icon('check','sm')}Đánh dấu tất cả</button>
              <button class="btn" type="button" onclick="markAll(${w.n},false)">${icon('undo','sm')}Bỏ chọn tuần này</button>
            </div>
          </div>
        </div>
      </div>`;
    host.appendChild(el);
  });
  host.querySelectorAll('input[type=checkbox]').forEach(cb=>{
    cb.addEventListener('change', ()=>{
      state[keyOf(+cb.dataset.w,+cb.dataset.i)] = cb.checked;
      save(); refreshAll();
    });
  });
  typesetMath(host);
  setTimeout(updateWeekBars,80);
}
function toggleWeek(head){
  const wk = head.closest('.week');
  const body = wk.querySelector('.wk-body');
  const open = wk.classList.toggle('open');
  head.setAttribute('aria-expanded', open ? 'true' : 'false');
  body.style.maxHeight = open ? body.scrollHeight+'px' : '0';
  if(open){ setTimeout(()=>{ if(wk.classList.contains('open')) body.style.maxHeight='none'; }, 400); }
}
function markAll(wn,val){
  const w = WEEKS.find(x=>x.n===wn);
  w.check.forEach((_,i)=> state[keyOf(wn,i)] = val);
  save();
  document.querySelectorAll(`input[data-w="${wn}"]`).forEach(cb=> cb.checked=val);
  refreshAll();
  const wk = document.querySelector(`.week[data-week="${wn}"]`);
  if(wk && wk.classList.contains('open')){ const b=wk.querySelector('.wk-body'); b.style.maxHeight=b.scrollHeight+'px'; }
}
function updateWeekBars(){
  WEEKS.forEach(w=>{ const p=weekProgress(w); const bar=document.querySelector(`[data-wbar="${w.n}"]`); if(bar) bar.style.width=p.pct+'%'; });
}

/* ---------------- advanced topics ---------------- */
function renderAdvanced(){
  const host = document.getElementById('adv-cards');
  if(!host) return;
  host.innerHTML = '';
  ADV.forEach(t=>{
    const el = document.createElement('div');
    el.className = 'adv-card';
    el.innerHTML = `
      <button class="adv-head" type="button" aria-expanded="false" onclick="toggleAdv(this)">
        <span class="ix2">${t.ix}</span>
        <div class="adv-t">
          <h3>${t.title}</h3>
          <div class="adv-meta"><span class="wk">${t.week}</span><span>${t.desc}</span></div>
        </div>
        <span class="caret">${icon('chevron')}</span>
      </button>
      <div class="adv-body"><div class="adv-inner">${t.body}</div></div>`;
    host.appendChild(el);
  });
  typesetMath(host);
}
function toggleAdv(head){
  const c = head.closest('.adv-card');
  const body = c.querySelector('.adv-body');
  const open = c.classList.toggle('open');
  head.setAttribute('aria-expanded', open ? 'true' : 'false');
  body.style.maxHeight = open ? body.scrollHeight+'px' : '0';
}

/* ---------------- books (kệ sách) ---------------- */
const BOOKS = window.BOOKS_DATA || [];
function renderBooks(filter='all'){
  const host = document.getElementById('book-cards');
  if(!host) return;
  host.innerHTML = '';
  BOOKS.filter(b=>{
    if(filter==='all') return true;
    if(filter==='later') return b.weeks.some(w=>w>3);
    return b.weeks.includes(+filter);
  }).forEach(b=>{
    const el = document.createElement('div');
    el.className = 'book';
    const reads = b.read.map(r=>`<div><b>Tuần ${r.week}:</b> ${r.what}</div>`).join('');
    el.innerHTML = `
      <div class="bk-top"><h3>${b.title}</h3></div>
      <div class="bk-author">${b.author}</div>
      <div class="bk-weeks">${b.weeks.map(w=>`<span>Tuần ${w}</span>`).join('')}</div>
      <div class="bk-lic ${b.verified?'':'warn'}">${icon(b.verified?'shield-check':'alert','sm')}<span><b>${b.verified?'Điều khoản đã kiểm.':'[Chưa xác minh] điều khoản.'}</b> ${b.license}</span></div>
      <div class="bk-read">${reads}</div>
      <a href="${b.url}" target="_blank" rel="noopener">Trang tải chính thức${icon('external','sm')}</a>`;
    host.appendChild(el);
  });
}
const bookFilterEl = document.getElementById('bookFilter');
if(bookFilterEl) bookFilterEl.addEventListener('click',e=>{
  const b=e.target.closest('.fbtn'); if(!b)return;
  bookFilterEl.querySelectorAll('.fbtn').forEach(x=>{x.classList.remove('active');x.setAttribute('aria-pressed','false');});
  b.classList.add('active'); b.setAttribute('aria-pressed','true');
  renderBooks(b.dataset.w);
});

/* ---------------- dashboard ---------------- */
let ringChart=null;
function totals(){ let done=0,total=0; WEEKS.forEach(w=>{ const p=weekProgress(w); done+=p.done; total+=p.total; }); return {done,total,pct: total?Math.round(done/total*100):0}; }
function phaseTotals(pid){ let done=0,total=0; WEEKS.filter(w=>w.phase===pid).forEach(w=>{ const p=weekProgress(w); done+=p.done; total+=p.total; }); return {done,total,pct: total?Math.round(done/total*100):0}; }
function weekCounts(){ let d=0,p=0,i=0; WEEKS.forEach(w=>{ const pr=weekProgress(w); if(pr.pct===100)d++; else if(pr.pct>0)p++; else i++; }); return {d,p,i}; }
function renderRing(){
  const t=totals();
  const ctx=document.getElementById('ringChart');
  if(!ctx) return;
  const cs=getComputedStyle(document.documentElement);
  const accent=cs.getPropertyValue('--accent').trim()||'#2563eb', track=cs.getPropertyValue('--surface-2').trim()||'#f1f4f8';
  const data={datasets:[{data:[t.pct,100-t.pct],backgroundColor:[accent,track],borderWidth:0,cutout:'80%',circumference:360}]};
  const reduced=window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(ringChart){ ringChart.data.datasets[0].data=[t.pct,100-t.pct]; ringChart.update(); }
  else{
    ringChart=new Chart(ctx,{type:'doughnut',data,options:{responsive:false,plugins:{legend:{display:false},tooltip:{enabled:false}},animation:{animateRotate:!reduced,duration:reduced?0:600}}});
  }
  document.getElementById('ringPct').textContent=t.pct+'%';
  document.getElementById('navPct').textContent=t.pct+'%';
  document.getElementById('doneItems').textContent=t.done;
  document.getElementById('totalItems').textContent=t.total;
}
function renderPhaseBars(){
  const host=document.getElementById('phaseBars'); if(!host) return; host.innerHTML='';
  PHASES.forEach(ph=>{
    const pt=phaseTotals(ph.id), c=PHASE_VAR[ph.id];
    const row=document.createElement('div'); row.className='pb-row';
    row.innerHTML=`<div class="pb-top">
      <span class="nm"><span class="tag-dot" style="background:${c}"></span>${ph.no}. ${ph.name}</span>
      <span class="vv">${pt.pct}%, ${pt.done}/${pt.total}</span></div>
      <div class="bar"><i style="background:${c}" data-pbar="${ph.id}"></i></div>`;
    host.appendChild(row);
  });
  setTimeout(()=>{ PHASES.forEach(ph=>{ const pt=phaseTotals(ph.id); const b=document.querySelector(`[data-pbar="${ph.id}"]`); if(b)b.style.width=pt.pct+'%'; }); },60);
}
function renderStats(){ const wc=weekCounts(); const m={stWeeksDone:wc.d,stWeeksProg:wc.p,stWeeksIdle:wc.i}; for(const k in m){const e=document.getElementById(k); if(e)e.textContent=m[k];} }
function renderRoadmap(){
  const host=document.getElementById('roadmap-cards'); if(!host) return; host.innerHTML='';
  PHASES.forEach(ph=>{
    const pt=phaseTotals(ph.id);
    const el=document.createElement('div'); el.className='phase-card '+ph.cls;
    el.innerHTML=`<div class="ph-no">${ph.no}</div><h3>${ph.name}</h3><div class="ph-week">${ph.weeks}</div><p>${ph.desc}</p>
      <div class="ph-prog"><span>Tiến độ</span><span data-phprog="${ph.id}">${pt.pct}%</span></div>
      <div class="bar mt"><i style="background:${PHASE_VAR[ph.id]}" data-phbar="${ph.id}"></i></div>`;
    host.appendChild(el);
  });
  setTimeout(()=>{ PHASES.forEach(ph=>{ const pt=phaseTotals(ph.id); const b=document.querySelector(`[data-phbar="${ph.id}"]`); if(b)b.style.width=pt.pct+'%'; }); },60);
}
function updateBadgesAndBars(){
  WEEKS.forEach(w=>{
    const st=weekStatus(w), p=weekProgress(w);
    const badge=document.querySelector(`[data-wbadge="${w.n}"]`);
    if(badge){ badge.className='badge '+st.cls; badge.textContent=st.label; }
    const lblHost=document.querySelector(`.week[data-week="${w.n}"] .wk-mini .lbl`);
    if(lblHost) lblHost.textContent=`${p.done}/${p.total}`;
  });
  updateWeekBars();
}
function refreshAll(){
  renderRing(); renderPhaseBars(); renderStats(); renderRoadmap(); updateBadgesAndBars();
  PHASES.forEach(ph=>{ const pt=phaseTotals(ph.id); const t=document.querySelector(`[data-phprog="${ph.id}"]`); if(t)t.textContent=pt.pct+'%'; });
}

/* ---------------- MathJax ---------------- */
function typesetMath(el){
  if(window.MathJax && MathJax.startup && MathJax.startup.promise){
    MathJax.startup.promise = MathJax.startup.promise
      .then(()=> MathJax.typesetPromise(el ? [el] : undefined))
      .catch(err=> console.warn('MathJax typeset error:', err));
  } else { setTimeout(()=> typesetMath(el), 150); }
}

/* ---------------- events ---------------- */
const filterEl = document.getElementById('filter');
if(filterEl) filterEl.addEventListener('click',e=>{
  const b=e.target.closest('.fbtn'); if(!b)return;
  filterEl.querySelectorAll('.fbtn').forEach(x=>{x.classList.remove('active');x.setAttribute('aria-pressed','false');});
  b.classList.add('active'); b.setAttribute('aria-pressed','true');
  renderWeeks(b.dataset.f); refreshAll();
});
const resetBtn = document.getElementById('resetBtn');
if(resetBtn) resetBtn.addEventListener('click',()=>{
  if(confirm('Đặt lại toàn bộ tiến độ? Mọi mục đã tick sẽ bị xóa.')){
    state={}; save();
    const active=(filterEl && filterEl.querySelector('.fbtn.active').dataset.f) || 'all';
    renderWeeks(active); refreshAll();
  }
});

/* ---------------- init ---------------- */
renderWeeks('all');
renderAdvanced();
renderBooks('all');
refreshAll();
if(window.matchMedia){ window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', ()=>{ if(ringChart){ ringChart.destroy(); ringChart=null; } renderRing(); }); }
