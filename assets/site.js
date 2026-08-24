// Smart Skills Hub — comportamento compartilhado
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Reveal ao rolar
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } }), { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Menu mobile
const burger = document.querySelector('.nav-hamburger'), mobile = document.querySelector('.nav-mobile');
if (burger && mobile) burger.addEventListener('click', () => { const open = mobile.classList.toggle('open'); burger.setAttribute('aria-expanded', String(open)); });

// Chat simulado (mesma sequência da LP)
const chat = document.getElementById('chat');
if (chat) {
  const seq = [['m1',800],['t1',1600],['t1',2600,true],['m2',2600],['m3',4000],['t2',4800],['t2',5800,true],['m4',5800],['m5',7200],['t3',8000],['t3',9200,true],['m6',9200]];
  const run = () => {
    seq.forEach(([id,delay,hide]) => setTimeout(() => {
      const el = document.getElementById(id); if (!el) return;
      if (hide) { el.style.display = 'none'; return; }
      el.style.display = id.startsWith('t') ? 'flex' : 'block';
      requestAnimationFrame(() => setTimeout(() => el.classList.add('show'), 30));
      chat.scrollTop = chat.scrollHeight;
    }, delay));
    setTimeout(() => { seq.forEach(([id]) => { const el = document.getElementById(id); if (el) { el.style.display = 'none'; el.classList.remove('show'); } }); setTimeout(run, 1200); }, 12000);
  };
  if (reduced) { seq.forEach(([id,,hide]) => { const el = document.getElementById(id); if (el && !hide && !id.startsWith('t')) { el.style.display = 'block'; el.classList.add('show'); } }); }
  else setTimeout(run, 800);
}

// Filtros de cases
const filters = document.querySelectorAll('.filter');
if (filters.length) filters.forEach(f => f.addEventListener('click', () => {
  filters.forEach(x => x.classList.remove('active')); f.classList.add('active');
  const k = f.dataset.filter;
  document.querySelectorAll('[data-cat]').forEach(c => { c.style.display = (k === 'all' || c.dataset.cat.includes(k)) ? '' : 'none'; });
}));

// Página intermediária: mensagem por origem + evento de conversão
const waBtn = document.getElementById('wa-open');
if (waBtn) {
  const msgs = {
    home: 'Olá. Vi o site da Smart Skills Hub e quero entender qual frente resolve o meu caso.',
    plataformas: 'Olá. Quero conversar sobre o desenvolvimento de um sistema ou aplicativo para a minha empresa.',
    agentes: 'Olá. Quero ver uma demonstração do agente de IA para o meu segmento.',
    automacoes: 'Olá. Tenho um processo repetitivo que quero automatizar.',
    cases: 'Olá. Vi os cases no site e quero saber como ficaria no meu segmento.',
    sobre: 'Olá. Quero falar com a equipe da Smart Skills Hub.',
    linkedin: 'Olá. Vim pelo LinkedIn e quero uma demonstração.',
    instagram: 'Olá. Vim pelo Instagram e quero uma demonstração.',
    ads: 'Olá. Vi o anúncio e quero uma demonstração.'
  };
  const origem = new URLSearchParams(location.search).get('origem') || 'home';
  waBtn.href = 'https://wa.me/5521971919691?text=' + encodeURIComponent(msgs[origem] || msgs.home);
  waBtn.addEventListener('click', () => {
    if (typeof window.ssTrack === 'function') window.ssTrack('whatsapp_click', { origem, destino: 'wa.me' });
    if (typeof gtag === 'function') gtag('event', 'whatsapp_click', { origem });
    if (typeof fbq === 'function') fbq('track', 'Contact', { origem });
    if (window.dataLayer) window.dataLayer.push({ event: 'whatsapp_click', origem });
  });
}
