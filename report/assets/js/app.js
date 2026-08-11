/* ============================================================
   LLM From Scratch — Portal app logic
   Phụ thuộc: weeks-data.js (PHASES, WEEKS_DATA), quiz-data.js (QUIZ_DATA),
              advanced-data.js (ADVANCED_TOPICS), Chart.js, MathJax
   ============================================================ */
const PHASES = window.PHASES;
const WEEKS  = window.WEEKS_DATA;
const QUIZ   = (window.QUIZ_DATA && window.QUIZ_DATA.weeks) || [];
const ADV    = window.ADVANCED_TOPICS || [];
const PHASE_COLOR = {1:{a:'#7c83ff',b:'#a855f7'},2:{a:'#2dd4bf',b:'#22d3ee'},3:{a:'#fbbf24',b:'#fb923c'}};
const LETTERS = ['A','B','C','D','E','F'];

/* ---------------- helpers ---------------- */
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function quizFor(n){const w=QUIZ.find(x=>x.week===n);return w?w.questions:[];}

/* ---------------- progress state ---------------- */
const LS_KEY = "llm_scratch_progress_v1";
let state = {};
try { state = JSON.parse(localStorage.getItem(LS_KEY) || "{}"); } catch(e){ state = {}; }
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

/* ---------------- render quiz block ---------------- */
function renderQuizBlock(n){
  const qs = quizFor(n);
  if(!qs.length) return '';
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
      <div class="qa" data-qa="${n}-${i}">
        <div class="qa-q" onclick="toggleQA(this)">
          <span class="qa-num">${i+1}</span>
          <div class="qa-qtext">
            <div class="qt">${esc(q.q)}</div>
            <div class="qa-type">${isMcq?'Trắc nghiệm':'Tự luận'}</div>
            ${choices}
          </div>
          <button class="qa-flipbtn" type="button">Xem đáp án</button>
        </div>
        <div class="qa-a"><div class="qa-a-inner">${ansHtml}${expl}</div></div>
      </div>`;
  }).join('');
  return `
    <div class="quiz">
      <h4><span class="ic" style="background:rgba(124,131,255,.18);color:var(--p1)">?</span>Quiz tự kiểm tra — ${qs.length} câu</h4>
      <div class="quiz-meta">Bấm vào câu hỏi (hoặc nút) để lật đáp án. File gốc: <code>Week-${String(n).padStart(2,'0')}/quiz.md</code> &amp; <code>quiz_solution.md</code>.</div>
      <div class="quiz-actions">
        <button onclick="flipAllQuiz(${n},true)">Hiện tất cả đáp án</button>
        <button onclick="flipAllQuiz(${n},false)">Ẩn tất cả</button>
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
  const q = quizFor(+qa.dataset.qa.split('-')[0])[+qa.dataset.qa.split('-')[1]];
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
  if(wk && wk.classList.contains('open')){ const b=wk.querySelector('.wk-body'); b.style.maxHeight=b.scrollHeight+'px'; }
}

/* ---------------- render weeks ---------------- */
function renderWeeks(filter='all'){
  const host = document.getElementById('weeks');
  host.innerHTML = '';
  WEEKS.filter(w=> filter==='all' || w.phase==+filter).forEach(w=>{
    const p = weekProgress(w), col = PHASE_COLOR[w.phase], st = weekStatus(w);
    const el = document.createElement('div');
    el.className = 'week p'+w.phase+' reveal';
    el.dataset.week = w.n;
    el.innerHTML = `
      <div class="wk-head" onclick="toggleWeek(this)">
        <div class="wk-num"><small>TUẦN</small><b>${w.n}</b></div>
        <div class="wk-titles">
          <h3>${w.title}</h3>
          <div class="meta"><span>⏱️ ${w.dur}</span><span>🖥️ ${w.hw}</span><span>❓ ${quizFor(w.n).length} câu quiz</span></div>
        </div>
        <div class="wk-right">
          <div class="wk-mini">
            <div class="lbl">${p.done}/${p.total}</div>
            <div class="bar"><i data-wbar="${w.n}" style="background:linear-gradient(90deg,${col.a},${col.b})"></i></div>
          </div>
          <span class="badge ${st.cls}" data-wbadge="${w.n}">${st.label}</span>
          <span class="caret">▾</span>
        </div>
      </div>
      <div class="wk-body">
        <div class="wk-inner">
          <div class="wk-grid">
            <div class="block">
              <h4><span class="ic" style="background:rgba(124,131,255,.18);color:var(--p1)">◎</span>Mục tiêu</h4>
              <ul class="obj-list">${w.obj.map(o=>`<li>${o}</li>`).join('')}</ul>
              <h4 style="margin-top:20px"><span class="ic" style="background:rgba(124,131,255,.18);color:var(--p1)">⬇</span>Deliverable</h4>
              <div class="deliver">${w.deliver}</div>
            </div>
            <div class="block">
              <h4><span class="ic" style="background:rgba(45,212,191,.18);color:var(--p2)">📖</span>Nguồn học</h4>
              <div class="src-list">${w.src.map(s=>`<div class="s">${s}</div>`).join('')}</div>
            </div>
          </div>
          <div class="know">
            <h4><span class="ic" style="background:rgba(45,212,191,.18);color:var(--p2)">∑</span>Tóm tắt kiến thức tổng hợp</h4>
            ${w.know}
          </div>
          ${renderQuizBlock(w.n)}
          <div class="checklist">
            <h4><span class="ic" style="background:rgba(251,191,36,.18);color:var(--p3)">✓</span>Checklist tiến độ — ${w.title}</h4>
            <div class="cl-items">
              ${w.check.map((c,i)=>`
                <label class="cl">
                  <input type="checkbox" data-w="${w.n}" data-i="${i}" ${state[keyOf(w.n,i)]?'checked':''}/>
                  <span>${c}</span>
                </label>`).join('')}
            </div>
            <div class="wk-actions">
              <button onclick="markAll(${w.n},true)">✓ Đánh dấu tất cả</button>
              <button onclick="markAll(${w.n},false)">↺ Bỏ chọn tuần này</button>
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
  observeReveal();
  typesetMath(host);
  setTimeout(updateWeekBars,80);
}
function toggleWeek(head){
  const wk = head.closest('.week');
  const body = wk.querySelector('.wk-body');
  const open = wk.classList.toggle('open');
  body.style.maxHeight = open ? body.scrollHeight+'px' : '0';
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
    el.className = 'adv-card reveal';
    el.innerHTML = `
      <div class="adv-head" onclick="toggleAdv(this)">
        <span class="ix2">${t.ix}</span>
        <div class="adv-t">
          <h3>${t.title}</h3>
          <div class="adv-meta"><span class="wk">${t.week}</span><span>${t.desc}</span></div>
        </div>
        <span class="caret">▾</span>
      </div>
      <div class="adv-body"><div class="adv-inner">${t.body}</div></div>`;
    host.appendChild(el);
  });
  observeReveal();
  typesetMath(host);
}
function toggleAdv(head){
  const c = head.closest('.adv-card');
  const body = c.querySelector('.adv-body');
  const open = c.classList.toggle('open');
  body.style.maxHeight = open ? body.scrollHeight+'px' : '0';
}

/* ---------------- dashboard ---------------- */
let ringChart=null;
function totals(){ let done=0,total=0; WEEKS.forEach(w=>{ const p=weekProgress(w); done+=p.done; total+=p.total; }); return {done,total,pct: total?Math.round(done/total*100):0}; }
function phaseTotals(pid){ let done=0,total=0; WEEKS.filter(w=>w.phase===pid).forEach(w=>{ const p=weekProgress(w); done+=p.done; total+=p.total; }); return {done,total,pct: total?Math.round(done/total*100):0}; }
function weekCounts(){ let d=0,p=0,i=0; WEEKS.forEach(w=>{ const pr=weekProgress(w); if(pr.pct===100)d++; else if(pr.pct>0)p++; else i++; }); return {d,p,i}; }
function renderRing(){
  const t=totals();
  const ctx=document.getElementById('ringChart');
  if(!ctx) return;
  const data={datasets:[{data:[t.pct,100-t.pct],backgroundColor:['rgba(45,212,191,1)','rgba(255,255,255,0.06)'],borderWidth:0,cutout:'78%',circumference:360}]};
  if(ringChart){ ringChart.data.datasets[0].data=[t.pct,100-t.pct]; ringChart.update(); }
  else{
    const grad=ctx.getContext('2d').createLinearGradient(0,0,200,200);
    grad.addColorStop(0,'#2dd4bf'); grad.addColorStop(1,'#22d3ee');
    data.datasets[0].backgroundColor=[grad,'rgba(255,255,255,0.06)'];
    ringChart=new Chart(ctx,{type:'doughnut',data,options:{responsive:false,plugins:{legend:{display:false},tooltip:{enabled:false}},animation:{animateRotate:true,duration:1400}}});
  }
  document.getElementById('ringPct').textContent=t.pct+'%';
  document.getElementById('navPct').textContent=t.pct+'%';
  document.getElementById('doneItems').textContent=t.done;
  document.getElementById('totalItems').textContent=t.total;
}
function renderPhaseBars(){
  const host=document.getElementById('phaseBars'); if(!host) return; host.innerHTML='';
  PHASES.forEach(ph=>{
    const pt=phaseTotals(ph.id), c=PHASE_COLOR[ph.id];
    const row=document.createElement('div'); row.className='pb-row';
    row.innerHTML=`<div class="pb-top">
      <span class="nm"><span class="tag-dot" style="background:linear-gradient(135deg,${c.a},${c.b})"></span>${ph.no} · ${ph.name}</span>
      <span class="vv">${pt.pct}% · ${pt.done}/${pt.total}</span></div>
      <div class="bar"><i style="background:linear-gradient(90deg,${c.a},${c.b})" data-pbar="${ph.id}"></i></div>`;
    host.appendChild(row);
  });
  setTimeout(()=>{ PHASES.forEach(ph=>{ const pt=phaseTotals(ph.id); const b=document.querySelector(`[data-pbar="${ph.id}"]`); if(b)b.style.width=pt.pct+'%'; }); },60);
}
function renderStats(){ const wc=weekCounts(); const m={stWeeksDone:wc.d,stWeeksProg:wc.p,stWeeksIdle:wc.i}; for(const k in m){const e=document.getElementById(k); if(e)e.textContent=m[k];} }
function renderRoadmap(){
  const host=document.getElementById('roadmap-cards'); if(!host) return; host.innerHTML='';
  PHASES.forEach(ph=>{
    const pt=phaseTotals(ph.id);
    const el=document.createElement('div'); el.className='phase-card '+ph.cls+' reveal';
    el.innerHTML=`<div class="ph-no">${ph.no}</div><h3>${ph.name}</h3><div class="ph-week">${ph.weeks}</div><p>${ph.desc}</p>
      <div class="ph-prog"><span>Tiến độ</span><span data-phprog="${ph.id}">${pt.pct}%</span></div>
      <div class="bar" style="margin-top:6px"><i style="background:linear-gradient(90deg,${PHASE_COLOR[ph.id].a},${PHASE_COLOR[ph.id].b})" data-phbar="${ph.id}"></i></div>`;
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

/* ---------------- reveal ---------------- */
let io;
function observeReveal(){
  if(!io){ io=new IntersectionObserver(es=>{ es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} }); },{threshold:.10}); }
  document.querySelectorAll('.reveal:not(.in)').forEach(el=>io.observe(el));
}

/* ---------------- events ---------------- */
const filterEl = document.getElementById('filter');
if(filterEl) filterEl.addEventListener('click',e=>{
  const b=e.target.closest('.fbtn'); if(!b)return;
  document.querySelectorAll('.fbtn').forEach(x=>x.classList.remove('active'));
  b.classList.add('active');
  renderWeeks(b.dataset.f); refreshAll();
});
const resetBtn = document.getElementById('resetBtn');
if(resetBtn) resetBtn.addEventListener('click',()=>{
  if(confirm('Đặt lại toàn bộ tiến độ? Mọi mục đã tick sẽ bị xóa.')){
    state={}; save();
    const active=document.querySelector('.fbtn.active').dataset.f;
    renderWeeks(active); refreshAll();
  }
});

/* ---------------- init ---------------- */
renderWeeks('all');
renderAdvanced();
refreshAll();
observeReveal();
