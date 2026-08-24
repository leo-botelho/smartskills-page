# Gera as páginas do site a partir de um layout comum. Rodar: python build.py
import os
from urllib.parse import quote
OUT = os.path.dirname(os.path.abspath(__file__))
PHONE = "(21) 97191-9691"; WA = "https://wa.me/5521971919691"; MAIL = "adm@smartskillshub.com.br"
FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;600&family=Instrument+Serif:ital@0;1&display=swap"

SYMBOL = '<svg width="32" height="32" viewBox="0 0 32 32" fill="none" role="img" aria-label="Smart Skills Hub"><polyline points="22,4 14,4 14,16 22,16 22,28 14,28" stroke="#F4F1EB" stroke-width="2.2" fill="none" stroke-linecap="square"/><circle cx="14" cy="28" r="2.5" fill="#00D4FF"/><circle cx="22" cy="4" r="2.5" fill="#00D4FF"/></svg>'
WA_ICON = '<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>'
ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
MAIL_ICON = '<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
IG_ICON = '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="5"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
FB_ICON = '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>'
ICONS = {
 'clock': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#00D4FF" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
 'chat': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="1.8" stroke-linecap="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
 'layers': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#00D4FF" stroke-width="1.8" stroke-linecap="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
 'flow': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="1.8" stroke-linecap="round"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/></svg>',
 'grid': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>',
 'check': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="1.8" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
 'cal': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#00D4FF" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
 'doc': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="1.8" stroke-linecap="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
 'phone': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="1.8" stroke-linecap="round"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12" y2="18.01"/></svg>',
 'cpu': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="1.8" stroke-linecap="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3"/></svg>',
 'link': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#00D4FF" stroke-width="1.8" stroke-linecap="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
 'card': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#00D4FF" stroke-width="1.8" stroke-linecap="round"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>',
 'users': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="1.8" stroke-linecap="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
 'bed': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="1.8" stroke-linecap="round"><path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/></svg>',
 'sheet': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/></svg>',
 'mail': '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="1.8" stroke-linecap="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
}
NAV = [('plataformas.html','Plataformas'),('agentes-de-ia.html','Agentes de IA'),('automacoes.html','Automações'),('cases.html','Cases'),('sobre.html','Sobre')]

# Mensagem por origem: o agente recebe o contexto de onde a pessoa veio.
MSG_WA = {
    'home': 'Olá. Vi o site da Smart Skills Hub e quero entender qual frente resolve o meu caso.',
    'plataformas': 'Olá. Quero conversar sobre o desenvolvimento de um sistema ou aplicativo para a minha empresa.',
    'agentes': 'Olá. Quero ver uma demonstração do agente de IA para o meu segmento.',
    'automacoes': 'Olá. Tenho um processo repetitivo que quero automatizar.',
    'cases': 'Olá. Vi os cases no site e quero saber como ficaria no meu segmento.',
    'sobre': 'Olá. Quero falar com a equipe da Smart Skills Hub.',
}

def wa(origem):
    # Link direto do WhatsApp. O clique segue medido: o track.js dispara
    # whatsapp_click com os UTMs da página antes da navegação.
    return WA + '?text=' + quote(MSG_WA.get(origem, MSG_WA['home']))

def scene(mode, caption=None):   # caption não é mais exibida
    return f'''<div class="hero-visual"><div class="scene" data-mode="{mode}"><div class="scene-fallback" aria-hidden="true">{SYMBOL.replace('width="32" height="32"','')}</div><div class="scene-mount" aria-hidden="true"></div></div></div>'''

CHAT = '''<div class="hero-visual"><div class="phone-frame" aria-label="Demonstração do agente de IA respondendo no WhatsApp">
<div class="phone-header"><div class="phone-avatar">SS</div><div class="phone-info"><p>Clínica Sorrir</p><span>● online agora</span></div></div>
<div class="phone-body" id="chat">
<div class="msg user chat-msg" id="m1">Boa tarde! Qual o valor de uma limpeza?<div class="msg-time">18:34</div></div>
<div class="typing chat-msg" id="t1" style="display:none"><span></span><span></span><span></span></div>
<div class="msg agent chat-msg" id="m2" style="display:none"><div class="agent-name">Agente IA · Smart Skills Hub</div>Olá! Boa tarde 😊 Nossa limpeza dental custa R$ 180. Você possui plano odontológico?<div class="msg-time">18:34</div></div>
<div class="msg user chat-msg" id="m3" style="display:none">Tenho Amil<div class="msg-time">18:35</div></div>
<div class="typing chat-msg" id="t2" style="display:none"><span></span><span></span><span></span></div>
<div class="msg agent chat-msg" id="m4" style="display:none"><div class="agent-name">Agente IA · Smart Skills Hub</div>Perfeito! Aceitamos Amil com cobertura total. Qual o melhor dia para você esta semana?<div class="msg-time">18:35</div></div>
<div class="msg user chat-msg" id="m5" style="display:none">Quinta-feira à tarde<div class="msg-time">18:35</div></div>
<div class="typing chat-msg" id="t3" style="display:none"><span></span><span></span><span></span></div>
<div class="msg agent chat-msg" id="m6" style="display:none"><div class="agent-name">Agente IA · Smart Skills Hub</div>Quinta tenho disponibilidade às 14h ou 16h30. Qual prefere? Já deixo registrado aqui 📅<div class="msg-time">18:36</div></div>
</div></div></div>'''

def hero(tag, title, sub, origem, visual, secondary=('#como','Ver como funciona'), cls=''):
    return f'''<section class="hero {cls}" aria-labelledby="hero-heading" style="padding-bottom:0"><div class="hero-grid-bg"></div>
<div class="hero-content"><div class="hero-tag">{tag}</div><h1 class="hero-title" id="hero-heading">{title}</h1><p class="hero-sub">{sub}</p>
<div class="hero-actions"><a href="{wa(origem)}" class="btn-primary" target="_blank" rel="noopener noreferrer">{WA_ICON}Falar com especialista</a><a href="{secondary[0]}" class="btn-secondary">{secondary[1]} {ARROW}</a></div></div>{visual}</section>'''

def section(label, title, sub, body, bg='bg-deep', sid=''):
    idattr = f' id="{sid}"' if sid else ''
    subhtml = f'<p class="section-sub reveal">{sub}</p>' if sub else ''
    return f'<section class="{bg}"{idattr}><div class="section-label reveal">{label}</div><div class="section-rule"></div><h2 class="section-title reveal">{title}</h2>{subhtml}{body}</section>'

def card(span, icon, label, title, desc, foot='', extra=''):
    col = {'clock':'cyan','cal':'cyan','layers':'cyan','link':'cyan','card':'cyan','chat':'violet','doc':'violet','phone':'violet','users':'violet','mail':'violet','flow':'amber','grid':'amber','bed':'amber','check':'green','cpu':'green','sheet':'green'}[icon]
    ic = f'<div class="card-icon {col}">{ICONS[icon]}</div>'
    return f'<div class="bento-card span-{span}"><div>{ic}<div class="card-label">{label}</div><div class="card-title">{title}</div><div class="card-desc">{desc}</div>{extra}</div>{foot}</div>'

def steps(items, note=''):
    s = ''.join(f'<div class="step reveal reveal-delay-{i}"><div class="step-num">0{i+1}</div><div class="step-title">{t}</div><div class="step-desc">{d}</div></div>' for i,(t,d) in enumerate(items))
    return f'<div class="steps">{s}</div>' + (f'<p class="steps-note reveal">→ {note}</p>' if note else '')

def gcard(kicker, title, text, roi='', featured=False, badge='', cat=''):
    return f'<div class="gcard{" featured" if featured else ""}" data-cat="{cat}">{f"<span class=gcard-badge>{badge}</span>" if badge else ""}<div class="gcard-kicker">{kicker}</div><div class="gcard-title">{title}</div><div class="gcard-text">{text}</div>{f"<div class=gcard-roi>→ {roi}</div>" if roi else ""}</div>'

def faq(items):
    return '<div class="faq reveal">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items) + '</div>'

def cta(title, text, origem):
    return f'''<section class="cta-final"><div class="section-label reveal" style="text-align:center">Próximo passo</div><h2 class="reveal">{title}</h2><p class="reveal">{text}</p>
<div class="cta-actions reveal"><a href="{wa(origem)}" class="btn-primary" target="_blank" rel="noopener noreferrer">{WA_ICON}Falar no WhatsApp</a><a href="mailto:{MAIL}" class="btn-outline">{MAIL_ICON}Enviar e-mail</a></div></section>'''

def page(fname, title, desc, body, mode=None, current=None, minimal=False):
    links = ''.join(f'<li><a href="{h}"{" aria-current=page" if h==current else ""}>{t}</a></li>' for h,t in NAV)
    mlinks = ''.join(f'<a href="{h}">{t}</a>' for h,t in NAV) + f'<a href="{wa("home")}" target="_blank" rel="noopener noreferrer" style="color:var(--cyan)">Falar com especialista</a>'
    nav = '' if minimal else f'''<nav class="site-nav" aria-label="Navegação principal"><a class="nav-logo" href="index.html">{SYMBOL}<div class="nav-logo-text">SMART<span>SKILLS</span></div></a>
<ul class="nav-links">{links}</ul><a href="{wa('home')}" class="nav-cta" target="_blank" rel="noopener noreferrer">Falar com especialista</a>
<button class="nav-hamburger" aria-label="Abrir menu" aria-expanded="false"><span></span><span></span><span></span></button></nav><div class="nav-mobile">{mlinks}</div>'''
    footer = '' if minimal else f'''<footer><div class="footer-brand"><a class="nav-logo" href="index.html">{SYMBOL.replace('width="32" height="32"','width="28" height="28"')}<div class="nav-logo-text" style="font-size:1rem">SMART<span>SKILLS</span></div></a><p>Plataformas, agentes de IA e automações para empresas de serviços.</p></div>
<div class="footer-col"><h4>Serviços</h4><ul><li><a href="plataformas.html">Plataformas e Aplicativos</a></li><li><a href="agentes-de-ia.html">Agentes de IA</a></li><li><a href="automacoes.html">Automações</a></li></ul></div>
<div class="footer-col"><h4>Empresa</h4><ul><li><a href="cases.html">Cases</a></li><li><a href="sobre.html">Sobre</a></li><li><a href="privacidade.html">Privacidade</a></li><li><a href="termos.html">Termos</a></li><li><a href="exclusao-dados.html">Exclusão de dados</a></li></ul></div>
<div class="footer-col"><h4>Contato</h4><ul><li><a href="{WA}" target="_blank" rel="noopener noreferrer">{WA_ICON.replace('16','14')}{PHONE}</a></li><li><a href="mailto:{MAIL}">{MAIL_ICON.replace('16','14')}{MAIL}</a></li><li><a href="https://www.instagram.com/smartskills.hub" target="_blank" rel="noopener noreferrer">{IG_ICON.replace('18','14')}@smartskills.hub</a></li><li><a href="https://facebook.com/smartskillshubrj" target="_blank" rel="noopener noreferrer">{FB_ICON.replace('18','14')}smartskillshubrj</a></li></ul></div></footer>
<div class="footer-bottom"><p>© 2026 Smart Skills Hub. Todos os direitos reservados.</p><div class="footer-socials"><a href="https://www.instagram.com/smartskills.hub" target="_blank" rel="noopener noreferrer" aria-label="Instagram">{IG_ICON}</a><a href="https://facebook.com/smartskillshubrj" target="_blank" rel="noopener noreferrer" aria-label="Facebook">{FB_ICON}</a><a href="{WA}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">{WA_ICON.replace('16','18')}</a></div></div>
<a class="wa-float" href="{wa('home')}" target="_blank" rel="noopener noreferrer" aria-label="Falar no WhatsApp"><div class="wa-float-label">Falar no WhatsApp</div>{WA_ICON.replace('width="16" height="16" ','')}</a>'''
    three = f'''<script type="importmap">{{"imports":{{"three":"https://unpkg.com/three@0.170.0/build/three.module.js"}}}}</script>
<script type="module">import {{ mountScene }} from './assets/scene.js'; const m=document.querySelector('.scene-mount'); if(m) mountScene(m, '{mode}');</script>''' if mode else ''
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#08090F">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="https://smartskillshub.com.br/{'' if fname=='index.html' else fname}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfessionalService","name":"Smart Skills Hub","description":"Plataformas, agentes de IA e automações para empresas de serviços.","url":"https://smartskillshub.com.br","telephone":"+5521971919691","email":"{MAIL}","address":{{"@type":"PostalAddress","addressCountry":"BR"}},"sameAs":["https://www.instagram.com/smartskills.hub","https://facebook.com/smartskillshubrj"]}}</script>
</head>
<body>
<a href="#conteudo-principal" class="skip-link">Ir para o conteúdo principal</a>
{nav}
<main id="conteudo-principal">{body}</main>
{footer}
<script src="assets/track.js" defer></script>
<script src="assets/site.js" defer></script>
{three}
</body>
</html>'''
    open(os.path.join(OUT, fname), 'w', encoding='utf-8').write(html); print(fname)

# ───────────────────────── HOME ─────────────────────────
home = hero('Tecnologia para empresas de serviços',
 'Sua empresa atende, agenda, cobra e opera.<br><em>Sem precisar contratar para crescer.</em>',
 'Construímos a plataforma, implantamos o agente de IA no WhatsApp e ligamos as automações que tiram o trabalho manual da sua equipe. A mesma equipe de engenharia faz os três.',
 'home', scene('hero','Símbolo Smart Skills Hub · cena interativa'), ('#servicos','Ver as três frentes'), cls='hero-3d')
home += '''<section class="proof" aria-label="Prova"><div class="proof-grid">
<div class="proof-item reveal"><div class="proof-num">Em produção</div><div class="proof-label">Plataformas próprias e de clientes rodando hoje</div></div>
<div class="proof-item reveal reveal-delay-1"><div class="proof-num">20 min</div><div class="proof-label">Demonstração ao vivo, sem script</div></div>
<div class="proof-item reveal reveal-delay-2"><div class="proof-num">Hub próprio</div><div class="proof-label">WhatsApp API, n8n e Mautic operados por nós</div></div>
<div class="proof-item reveal reveal-delay-3"><div class="proof-num">Uma equipe</div><div class="proof-label">Quem constrói o sistema implanta o agente</div></div></div></section>'''
home += section('Serviços','Três frentes. <em>Uma equipe de engenharia.</em>','Cada frente resolve um problema de operação. Juntas, elas fazem o atendimento virar o gatilho de tudo o que acontece depois.',
 '<div class="bento reveal">'
 + card(4,'layers','Produto digital sob medida','O sistema que a sua operação precisava e nenhum software de prateleira entrega','SaaS, aplicativo, painel interno ou portal do cliente. Do diagnóstico ao deploy, com IA embarcada quando faz sentido para o processo.', '<div><div class="card-highlight">→ Construímos produtos, não só automações.</div><a class="card-link" href="plataformas.html">Conhecer plataformas '+ARROW+'</a></div>')
 + card(4,'chat','Atendimento 24 horas no WhatsApp','Seu cliente manda mensagem. O agente responde, qualifica, agenda e cobra','Treinado com a base da sua empresa. Entende texto, áudio, documento e imagem. Executa ações reais no seu sistema, não só responde.', '<div><div class="card-highlight">→ Veja o agente funcionando ao vivo.</div><a class="card-link" href="agentes-de-ia.html">Conhecer agentes de IA '+ARROW+'</a></div>')
 + card(4,'flow','Processos no piloto automático','Cobrança, CRM, notificação e planilha sem ninguém da equipe digitando','Fluxos em n8n e APIs conectando o que a sua empresa já usa. O que hoje é copiar e colar vira rotina que roda sozinha.', '<div><div class="card-highlight">→ O atendimento vira o gatilho da operação.</div><a class="card-link" href="automacoes.html">Conhecer automações '+ARROW+'</a></div>')
 + '</div>', sid='servicos')
home += section('Demonstração','O agente <em>respondendo de verdade</em>','Antes de explicar, mostramos. A conversa ao lado é o padrão do que o agente faz em uma clínica: responde valor, confere convênio e agenda.',
 f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center" class="demo-grid">{CHAT}<div class="reveal"><div class="card-label">O que acontece nessa conversa</div><ul style="list-style:none;display:flex;flex-direction:column;gap:1rem;margin-top:1rem"><li class="card-desc">→ <b style="color:var(--white)">18:34</b> O paciente pergunta o valor. O agente responde e já pergunta sobre convênio.</li><li class="card-desc">→ <b style="color:var(--white)">18:35</b> Confere a cobertura e pede o melhor dia.</li><li class="card-desc">→ <b style="color:var(--white)">18:36</b> Oferece dois horários reais da agenda e registra.</li><li class="card-desc">→ Se o paciente pedir para falar com alguém, a conversa é transferida para a equipe.</li></ul><a class="btn-secondary" href="agentes-de-ia.html" style="margin-top:2rem">Ver tudo que o agente faz {ARROW}</a></div></div><style>@media(max-width:900px){{.demo-grid{{grid-template-columns:1fr!important}}}}</style>', bg='bg-navy')
home += section('Segmentos','Feito para empresa de serviço <em>que perde cliente fora do horário</em>','Clínicas, pousadas, salões, franquias e escritórios têm o mesmo problema: o cliente manda mensagem às 21h e a resposta sai no dia seguinte.',
 '<div class="seg-pills reveal">' + ''.join(f'<span class="seg-pill">{s}</span>' for s in ['Clínicas odontológicas','Clínicas veterinárias','Salões e estética','Saúde e bem-estar','Hospedagem e pousadas','Serviços locais e franquias','Escritórios contábeis','Infoprodutores e e-commerce']) + '</div>')
home += section('Método','Mapeamos antes de construir. <em>Testamos antes de entregar.</em>','A maioria pula a primeira etapa e entrega automação que não funciona na prática.',
 steps([('Diagnóstico','Levantamos o processo como ele acontece hoje: quem faz, em que sistema, onde trava. Isso vira o escopo e a base de conhecimento.'),('Construção e integrações','Desenvolvemos, conectamos ao WhatsApp, à agenda, ao sistema de cobrança e ao que mais a operação usa. Testamos com cenários reais.'),('Ativação e evolução','Entra em produção com a sua equipe treinada no painel. Acompanhamos os atendimentos reais e refinamos todo mês.')],'Usamos na nossa própria operação o que entregamos para o cliente.'), bg='bg-navy', sid='como')
home += section('Em produção','Onde isso <em>já está rodando</em>','Escopo e mecanismo de cada projeto. Os resultados numéricos entram quando forem medidos com o cliente.',
 '<div class="cards-grid reveal">'
 + gcard('Clínica odontológica','Click Odonto','Agente de IA de atendimento integrado ao ERP Click Gest, sistema completo de gestão da clínica.','Agente + plataforma no segmento-âncora')
 + gcard('Anfitriões Airbnb e Booking','Venx Empresarial · app Hostax','Aplicativo de automação fiscal do checkout ao imposto, com Carnê-Leão para residente e não residente.','Aplicativo desenvolvido para o cliente')
 + gcard('Hospedagem','Pousada Marisis','Motor de reservas com página pública, painel, sincronização iCal com Booking e Airbnb, cobrança e confirmação de pagamento automáticas e automação do WhatsApp.','Plataforma + automação no mesmo projeto')
 + gcard('Clínica veterinária','Vet Pop Ceilândia','Agente "Celina": recepção no WhatsApp, identificação da necessidade e agendamento de castração.','Agente em produção')
 + '</div><p class="reveal" style="margin-top:2rem"><a class="btn-secondary" href="cases.html">Ver todos os cases '+ARROW+'</a></p>')
home += cta('Veja funcionando <em>para a sua empresa</em>','Demonstração gratuita de 20 minutos. Você traz o processo que mais consome a equipe, a gente mostra como ele fica.','home')
page('index.html','Smart Skills Hub | Plataformas, agentes de IA e automações para empresas de serviços','Construímos sistemas e aplicativos, implantamos agentes de IA no WhatsApp e automatizamos processos para clínicas, serviços locais e franquias. Veja funcionando ao vivo.', home, mode='hero')

# ───────────────────────── PLATAFORMAS ─────────────────────────
p = hero('Plataformas e aplicativos','A planilha virou gargalo.<br><em>Vira sistema.</em><br>Feito para a sua operação.',
 'Construímos SaaS, aplicativos, painéis internos e portais do cliente do diagnóstico ao deploy. A mesma equipe que mantém produtos próprios em produção é a que desenvolve o seu.',
 'plataformas', scene('layers','Camadas de sistema · cena interativa'), ('#entregas','Ver o que construímos'), cls='hero-3d')
p += section('Sinais','Quando o software de prateleira <em>para de servir</em>','',
 '<div class="bento reveal">'
 + card(4,'grid','Sinal 1','A operação vive em três lugares','Planilha, WhatsApp e um sistema que não conversa com os outros. Alguém da equipe passa o dia copiando de um para o outro.')
 + card(4,'cpu','Sinal 2','O sistema atual não faz o seu processo','Ele foi feito para a média do mercado. A sua regra de agendamento, de cobrança ou de triagem fica fora dele.')
 + card(4,'users','Sinal 3','Crescer significa contratar','Cada cliente novo é mais gente digitando. A margem não acompanha o faturamento.')
 + '</div><p class="steps-note reveal">→ Se dois desses três descrevem a sua empresa, o sistema sob medida costuma sair mais barato do que parece.</p>')
p += section('Entregas','Quatro formatos. <em>Um método.</em>','',
 '<div class="bento reveal">'
 + card(6,'layers','SaaS e plataformas multi-tenant','Produto com planos, múltiplos clientes e painel de administração','Cobrança recorrente, permissões por cliente e administração central. Em produção: triagem fiscal para escritórios contábeis, recuperação de glosas para clínicas, motor de reservas para pousadas.')
 + card(6,'phone','Aplicativos e PWA','App instalável no celular, com push, pagamento e conteúdo','Funciona como aplicativo sem depender de loja. Em produção: programa de bem-estar de 28 dias com IA conversacional e pagamentos.')
 + card(4,'grid','Painéis internos e ERPs','Sistema de gestão da operação','Agenda, cadastro, financeiro, estoque e relatórios no mesmo lugar. Em produção: ERP de clínica odontológica.')
 + card(8,'link','Integrações e portais','Portal do cliente e conexões com o que a empresa já usa','Painel de atendimento integrado ao app, portal do cliente, conexões com SERPRO, meios de pagamento, Booking e Airbnb, Google Agenda e WhatsApp API.','', '<div class="badges"><span class="int-badge">Supabase</span><span class="int-badge">Next.js</span><span class="int-badge">n8n</span><span class="int-badge">Pagamentos</span><span class="int-badge">WhatsApp API</span><span class="int-badge">SERPRO</span><span class="int-badge">iCal</span><span class="int-badge">Cloudflare</span></div>')
 + card(12,'cpu','IA embarcada onde faz sentido','A IA entra como função do sistema, não como enfeite','Triagem automática com trecho-fonte, assistente conversacional com a base do produto, classificação de documentos. O usuário vê a resposta e a evidência de onde ela veio.','<div class="card-highlight">→ Resposta com evidência, não caixa-preta.</div>')
 + '</div>', bg='bg-navy', sid='entregas')
p += section('Processo','Do diagnóstico <em>ao deploy</em>','Você não precisa escrever especificação. Precisa mostrar como a operação acontece hoje.',
 steps([('Discovery','Sentamos com quem opera. Mapeamos o fluxo real, as exceções e os sistemas que já existem. Saída: escopo fechado por etapas, com o que entra na primeira versão e o que fica para depois.'),('Arquitetura e construção','Definimos a stack, desenhamos o banco e as telas, construímos em ciclos curtos. Você vê a tela funcionando a cada ciclo, não só no fim.'),('Deploy e evolução','Entra em produção com migração dos dados, treinamento da equipe e monitoramento. Depois, evolução contínua para o sistema acompanhar a operação.')],'Prazo e investimento dependem do escopo da primeira versão. Saem do discovery, não de um chute.'), sid='como')
p += section('Diferença','Construímos produtos. <em>Não só telas.</em>','',
 '<div class="bento reveal">'
 + card(4,'check','Prova','Produtos próprios em produção','Mantemos SaaS nossos, com usuários. Sabemos o que quebra depois do lançamento porque já quebrou com a gente.')
 + card(4,'chat','Integração','O agente e a automação entram no mesmo projeto','Quem constrói o sistema é quem implanta o agente de IA e os fluxos. Sem três fornecedores para uma integração.')
 + card(4,'flow','Infraestrutura','Hub próprio testado','WhatsApp API, n8n, Mautic e channel manager rodam na nossa infraestrutura antes de ir para o cliente.')
 + '</div>', bg='bg-navy')
p += section('Em produção','Plataformas <em>que já rodam</em>','',
 '<div class="cards-grid reveal">'
 + gcard('Clínica odontológica','Click Gest · Click Odonto','ERP completo: agenda, pacientes, financeiro, procedimentos. Integrado ao agente de IA de atendimento.')
 + gcard('Anfitriões Airbnb e Booking','Aplicativo Hostax · Venx Empresarial','Automação fiscal do checkout ao imposto, Carnê-Leão para residente e não residente.')
 + gcard('Operação e atendimento','Plataforma interna · Hostax','Painel interno de operação integrado ao aplicativo, com dashboard e e-mails.')
 + gcard('Hospedagem','Motor de reservas · Pousada Marisis','Multi-tenant com página pública de reserva, painel, iCal com Booking e Airbnb, cobrança e confirmação de pagamento automáticas e automação do WhatsApp.')
 + gcard('Escritórios contábeis · produto próprio','Ciente','Triagem de intimações fiscais (DTE/e-CAC) com integração SERPRO, IA com trecho-fonte, fila por gravidade e prazo.')
 + gcard('Clínicas · produto próprio','Glosax','Recuperação de glosas de convênio: demonstrativo → classificação → recurso → acompanhamento.')
 + '</div>')
p += section('Perguntas','O que costumam <em>perguntar antes</em>','',
 faq([('Já tenho um sistema. Vocês integram ou substituem?','Depende do que ele faz bem. Na maioria dos casos, construímos em volta do que funciona e substituímos só a parte que trava.'),
      ('Quanto tempo leva?','A primeira versão sai do discovery com escopo e prazo fechados. Projetos menores entram em produção em semanas; plataformas completas, em meses.'),
      ('E se a minha equipe não adotar?','O treinamento faz parte da entrega e o sistema é desenhado a partir do processo que a equipe já faz, não de um ideal.'),
      ('Vocês ficam depois do lançamento?','Sim. A evolução contínua existe para isso: o sistema acompanha a operação conforme ela muda.')]), bg='bg-navy')
p += cta('Traga o processo que mais <em>consome a sua equipe</em>','Em 20 minutos, mapeamos com você se ele pede um sistema, um agente ou uma automação. Sem proposta genérica.','plataformas')
page('plataformas.html','Desenvolvimento de plataformas e aplicativos sob medida | Smart Skills Hub','SaaS, aplicativo, painel interno ou portal do cliente, construídos do diagnóstico ao deploy pela equipe que já colocou produtos em produção. Com IA embarcada quando faz sentido.', p, mode='layers', current='plataformas.html')

# ───────────────────────── AGENTES DE IA ─────────────────────────
a = hero('Agente de IA · Atendimento automatizado','Seu cliente manda mensagem.<br><em>O agente responde.</em><br>24 horas por dia.',
 'Um agente de inteligência artificial treinado para a sua empresa, que atende no WhatsApp e mídias sociais, qualifica leads, agenda, gera cobranças e fecha contratos. E transfere para a sua equipe quando o cliente pede ou quando a conversa precisa de gente.',
 'agentes', CHAT, ('#como','Ver como funciona'))
a += '''<section class="proof" aria-label="O que o agente faz"><div class="proof-grid">
<div class="proof-item reveal"><div class="proof-num">24h por dia</div><div class="proof-label">Atende de madrugada, feriado e fim de semana</div></div>
<div class="proof-item reveal reveal-delay-1"><div class="proof-num">4 formatos</div><div class="proof-label">Texto, áudio, documento e imagem</div></div>
<div class="proof-item reveal reveal-delay-2"><div class="proof-num">Ações reais</div><div class="proof-label">Agenda, cobra, assina e dispara a operação</div></div>
<div class="proof-item reveal reveal-delay-3"><div class="proof-num">20 min</div><div class="proof-label">Demonstração ao vivo com o seu segmento</div></div></div></section>'''
a += section('Recursos','Tudo que seu atendimento<br><em>precisa funcionar sozinho</em>','O agente não é um chatbot com botões. É uma IA treinada com o conhecimento da sua empresa, que entende o contexto, responde de forma natural e executa ações reais.',
 '<div class="bento reveal">'
 + card(6,'clock','Disponibilidade','Atendimento 24 horas, 7 dias por semana','O agente atende seu cliente às 22h de uma sexta-feira com a mesma qualidade de uma segunda de manhã. Nenhum lead fica sem resposta por causa de horário.','<div class="card-highlight">→ Sexta à noite, feriado ou segunda de manhã, a resposta sai no mesmo padrão.</div>')
 + card(6,'chat','Conversação','Conversa com naturalidade','O agente é treinado com o tom e o vocabulário da sua empresa. Responde com naturalidade, lembra o contexto da conversa e adapta a linguagem ao cliente.','<div class="card-highlight">→ Soa como a sua empresa. E passa para alguém da equipe quando o cliente pede.</div>')
 + card(4,'grid','Multimodal','Entende texto, áudio, documento e imagem','Não apenas texto. O agente processa mensagens de voz, lê documentos enviados pelo cliente e interpreta imagens, como fotos de exames, receitas ou comprovantes.','<div class="pills"><span class="pill cyan">Texto</span><span class="pill violet">Áudio</span><span class="pill amber">Documento</span><span class="pill green">Imagem</span></div>')
 + card(8,'check','Inteligência comercial','Filtra e qualifica leads automaticamente','O agente faz as perguntas certas para entender a intenção do cliente, e classifica cada contato por interesse, urgência e perfil. Sua equipe recebe apenas os leads prontos para fechar.','<div class="card-highlight">→ Você foca em vender. O agente faz a triagem.</div>')
 + card(6,'cal','Agendamento direto','Agenda no sistema do cliente ou Google Agenda','O agente verifica disponibilidade em tempo real e confirma o agendamento dentro da própria conversa, sem ninguém da equipe precisar parar para consultar a agenda.','','<div class="badges"><span class="int-badge">Google Agenda</span><span class="int-badge">Clinicorp</span><span class="int-badge">Odontosys</span><span class="int-badge">+ outros via API</span></div>')
 + card(6,'doc','Financeiro e contratos','Gera cobrança, confirma pagamento e assina contratos','O agente gera links de pagamento (Pix, boleto, cartão), confirma quando o pagamento é realizado e encaminha contratos para assinatura digital, tudo dentro do WhatsApp.','<div class="card-highlight">→ Da conversa ao contrato assinado sem sair do chat.</div>')
 + card(12,'flow','Automações internas','Integração com fluxos de automação da operação','O agente se conecta com as automações internas da sua empresa via n8n, Zapier ou Make, disparando notificações para a equipe, atualizando CRMs, preenchendo planilhas e muito mais.','<div class="card-highlight">→ O atendimento vira o gatilho de toda a operação.</div>','<div class="badges"><span class="int-badge">n8n</span><span class="int-badge">Zapier</span><span class="int-badge">Make</span><span class="int-badge">ActiveCampaign</span><span class="int-badge">RD Station</span><span class="int-badge">Chatwoot</span><span class="int-badge">Google Sheets</span><span class="int-badge">Supabase</span><span class="int-badge">Slack / Teams</span><span class="int-badge">Webhooks</span></div>')
 + '</div>', sid='recursos')
a += section('Processo','Do briefing ao agente <em>em produção</em>','A implementação é feita pela nossa equipe. Você não precisa entender de tecnologia. Basta a aprovação e o treinamento da sua equipe para usar o painel.',
 steps([('Diagnóstico e treinamento','Levantamos as perguntas mais frequentes dos seus clientes, os serviços que você oferece, regras de agendamento, valores e o tom de comunicação da sua empresa. Esse material vira a base de conhecimento do agente.'),('Desenvolvimento e integrações','Construímos o agente, conectamos ao seu WhatsApp Business, configuramos as integrações necessárias (agenda, cobrança, CRM) e realizamos os testes com cenários reais antes de ativar.'),('Ativação e manutenção contínua','O agente entra em produção. Treinamos sua equipe para acompanhar as conversas pelo painel e, mensalmente, refinamos as respostas com base nos atendimentos reais. O agente fica mais preciso com o tempo.')]), bg='bg-navy', sid='como')
a += section('Segmentos','Onde o agente <em>já prova resultado</em>','O agente é treinado especificamente para o seu segmento, não é solução genérica. Cada nicho tem suas próprias perguntas, objeções e fluxo de atendimento.',
 '<div class="cards-grid reveal">'
 + gcard('','Clínica Odontológica','Responde sobre convênios, valores de tratamento, disponibilidade de horário. Agenda consultas e envia confirmação automática. Atende às 22h o paciente que quer marcar implante.','O paciente que quer marcar implante às 22h não espera até amanhã',featured=True,badge='Melhor caso de uso')
 + gcard('','Clínica Veterinária','Triagem de urgências fora do horário, retorno de exames, agendamento de banho e tosa, controle de vacinas, tudo automatizado no WhatsApp.','Urgências fora de horário são dor real e recorrente')
 + gcard('','Salão de Beleza e Estética','Agendamento por WhatsApp sem confusão, confirmação de horário 24h antes, lista de espera automática para cancelamentos e cobrança de sinal antecipado.','Cancela menos, agenda mais, perde menos receita')
 + gcard('','Clínica de Saúde e Bem-Estar','Fonoaudiologia, psicologia, fisioterapia: atende as dúvidas iniciais dos responsáveis, qualifica o caso e agenda a primeira consulta de avaliação.','Triagem que economiza o tempo do especialista')
 + gcard('','Hospedagem e Pousadas','Responde disponibilidade, apresenta as acomodações, qualifica o tipo de hóspede, cobra o sinal e transfere para a recepção quando a reserva está pronta.','A reserva fecha na conversa, não no dia seguinte')
 + gcard('','Serviços Locais e Franquias','Academias, studios, escritórios, imobiliárias: o agente escala o atendimento sem crescer a equipe na mesma proporção, mantendo consistência em todas as unidades.','Escala sem crescer o headcount na mesma proporção')
 + '</div>')
a += section('Em produção','Agentes <em>que já atendem</em>','',
 '<div class="cards-grid reveal">'
 + gcard('Clínica veterinária','Celina · Vet Pop Ceilândia','Recepção no WhatsApp, identificação da necessidade e fluxo de agendamento de castração.')
 + gcard('Hospitalidade premium','Gabi · Borgo San Felice Boutique','Recepção de leads, apresentação da proposta, qualificação por tipo de experiência e transferência por protocolo quando o cliente está pronto para reservar.')
 + gcard('Beleza e estética','Isabella · Salão Rosa Bella','Recebe leads de anúncios online, conecta e conduz até o agendamento.')
 + gcard('Clínica odontológica','Agente de atendimento · Click Odonto','Atendimento integrado ao ERP Click Gest.')
 + '</div>', bg='bg-navy')
a += cta('Veja o agente funcionando <em>para a sua empresa</em>','Demonstração gratuita de 20 minutos. Mostramos o agente respondendo perguntas reais do seu segmento, ao vivo, sem script.','agentes')
page('agentes-de-ia.html','Agente de IA para atendimento 24h no WhatsApp | Smart Skills Hub','Agente de IA que atende seus clientes 24h no WhatsApp. Qualifica leads, agenda consultas, gera cobranças e contratos. Veja funcionando ao vivo.', a, current='agentes-de-ia.html')

# ───────────────────────── AUTOMAÇÕES ─────────────────────────
au = hero('Automações de processo','O que hoje é copiar e colar<br><em>vira rotina que roda sozinha.</em>',
 'Ligamos os sistemas que a sua empresa já usa. O pagamento confirma e o contrato sai. O lead entra e o CRM atualiza. A reserva fecha e o WhatsApp avisa. Ninguém da equipe precisa lembrar.',
 'automacoes', scene('graph','Grafo de integrações · cena interativa'), ('#fluxos','Ver exemplos de fluxo'), cls='hero-3d')
def flow(span, icon, title, trigger, desc, badges):
    return f'<div class="bento-card span-{span}"><div><div class="card-icon {"cyan" if icon in ("card","cal","link") else "violet" if icon in ("users","mail") else "amber" if icon=="bed" else "green"}">{ICONS[icon]}</div><div class="card-trigger">Gatilho · {trigger}</div><div class="card-title">{title}</div><div class="card-desc">{desc}</div></div><div class="badges">{"".join(f"<span class=int-badge>{b}</span>" for b in badges)}</div></div>'
au += section('Fluxos','Automações que <em>já rodam em produção</em>','',
 '<div class="bento reveal">'
 + flow(6,'card','Cobrança e confirmação','agendamento confirmado','Gera o link de pagamento (Pix, boleto, cartão), confirma o recebimento, libera a reserva ou a consulta e avisa o cliente no WhatsApp.',['Pix, boleto e cartão','WhatsApp API'])
 + flow(6,'users','Lead para CRM','mensagem de anúncio','Qualifica, cria o contato no CRM com origem e interesse e avisa o vendedor com o resumo da conversa.',['Mautic','RD Station','ActiveCampaign','Chatwoot'])
 + flow(4,'cal','Agenda e lembretes','consulta marcada','Confirma 24h antes, reagenda em caso de cancelamento e aciona a lista de espera.',['Google Agenda','Clinicorp','Odontosys'])
 + flow(4,'bed','Canal de reservas','reserva no Booking ou Airbnb','Sincroniza a disponibilidade, cobra o sinal e envia as instruções de check-in.',['iCal','Pagamento automático','WhatsApp API'])
 + flow(4,'sheet','Planilha e relatório','fim do dia','Consolida atendimentos, vendas e pendências e envia o resumo para o gestor.',['Google Sheets','Supabase','Slack / Teams'])
 + flow(12,'mail','Nutrição por e-mail','demonstração realizada','Sequência de e-mails por segmento, com alerta para a equipe quando o lead volta a abrir.',['Mautic'])
 + '</div><p class="steps-note reveal">→ Se o sistema tem API, entra no fluxo.</p>', sid='fluxos')
au += section('Processo','Mapeamos o processo <em>antes de automatizar</em>','A maioria pula essa etapa e entrega automação que não funciona na prática.',
 steps([('Mapeamento','Desenhamos o processo como ele acontece, com as exceções. Definimos o que automatiza agora e o que continua manual por enquanto.'),('Construção e testes','Montamos os fluxos no n8n, conectamos as APIs e testamos com dados reais, incluindo o que dá errado: pagamento recusado, cliente que some, sistema fora do ar.'),('Ativação e monitoramento','Fluxo em produção com alerta quando algo falha. Revisamos com você o que rodou e o que precisa de ajuste.')]), bg='bg-navy', sid='como')
au += section('Diferença','Por que <em>com a gente</em>','',
 '<div class="bento reveal">'
 + card(4,'flow','Infraestrutura','Hub próprio','Nossos fluxos de atendimento, cobrança e e-mail rodam na mesma infraestrutura que oferecemos: n8n, WhatsApp API, Mautic.')
 + card(4,'chat','Integração','Automação que conversa com o agente','O agente de IA dispara os fluxos e recebe o retorno deles. Atendimento e operação na mesma linha.')
 + card(4,'layers','Profundidade','Quando o fluxo pede sistema, a gente constrói','Se a automação esbarra no limite da ferramenta, a mesma equipe desenvolve o módulo que falta.')
 + '</div>')
au += section('Perguntas','O que costumam <em>perguntar antes</em>','',
 faq([('Preciso trocar de sistema?','Não. A automação conecta o que você já usa. Só sugerimos troca quando o sistema atual não tem API.'),
      ('Zapier e Make servem?','Servem, e usamos quando fazem sentido. Preferimos n8n por custo por execução e por rodar na nossa infraestrutura.'),
      ('O que acontece quando dá erro?','O fluxo avisa. Nenhuma automação nossa falha em silêncio.'),
      ('Como é cobrado?','Projeto fechado por fluxo ou acompanhamento mensal de operação, conforme o volume.')]), bg='bg-navy')
au += cta('Qual tarefa repetitiva <em>a sua equipe faz toda semana?</em>','Conta para a gente em 20 minutos. Saímos da conversa com o desenho do fluxo.','automacoes')
page('automacoes.html','Automação de processos com n8n e integrações | Smart Skills Hub','Cobrança, CRM, notificações, planilhas e e-mail rodando sozinhos. Fluxos em n8n e APIs conectando os sistemas que a sua empresa já usa.', au, mode='graph', current='automacoes.html')

# ───────────────────────── CASES ─────────────────────────
c = hero('Em produção','O que construímos<br><em>e está rodando hoje</em>',
 'Cada projeto descrito pelo escopo e pelo mecanismo. Resultados numéricos entram quando são medidos com o cliente e autorizados para publicação.',
 'cases', scene('particles','Mensagens em trânsito · cena interativa'), ('#lista','Ver os projetos'), cls='hero-3d')
c += section('Projetos','Plataformas, agentes <em>e automações</em>','',
 '<div class="filters reveal"><button class="filter active" data-filter="all">Todos</button><button class="filter" data-filter="plat">Plataformas</button><button class="filter" data-filter="agente">Agentes de IA</button><button class="filter" data-filter="auto">Automações</button></div><div class="cards-grid reveal">'
 + gcard('Plataforma · Clínica odontológica','Click Gest · Click Odonto','ERP completo de gestão da clínica: agenda, pacientes, financeiro, procedimentos. Integrado ao agente de IA de atendimento.','Plataforma sob medida no segmento-âncora',cat='plat')
 + gcard('Aplicativo · Anfitriões Airbnb e Booking','Aplicativo Hostax · Venx Empresarial','Automação fiscal do checkout ao imposto, com Carnê-Leão para residente e não residente.','Aplicativo desenvolvido para o cliente',cat='plat')
 + gcard('Plataforma interna · Operação','Plataforma interna · Hostax','Painel interno de operação integrado ao aplicativo, com dashboard e e-mails.','Plataforma interna + integração',cat='plat')
 + gcard('Plataforma + automação · Hospedagem','Motor de reservas · Pousada Marisis','Motor multi-tenant com página pública de reserva, painel, sincronização iCal com Booking e Airbnb, cobrança e confirmação de pagamento de forma automática e automação do WhatsApp.','Plataforma e automação no mesmo projeto',cat='plat auto')
 + gcard('Produto próprio · Escritórios contábeis','Ciente','SaaS de triagem de intimações fiscais (DTE/e-CAC) com integração SERPRO, triagem por IA com trecho-fonte, fila por gravidade e prazo, alertas.','IA embarcada com evidência',cat='plat')
 + gcard('Produto próprio · Clínicas','Glosax','SaaS de recuperação de glosas de convênio: demonstrativo, classificação, recurso e acompanhamento.','Ciclo completo em um produto',cat='plat')
 + gcard('Produto de cliente · Bem-estar','Netzach · Raquel Guimarães','PWA com IA conversacional (RAG), créditos por plano, push e pagamento integrado.','App completo em produção',cat='plat')
 + gcard('Agente de IA · Clínica veterinária','Celina · Vet Pop Ceilândia','Recepção no WhatsApp, identificação da necessidade e fluxo de agendamento de castração.','',cat='agente')
 + gcard('Agente de IA · Hospitalidade premium','Gabi · Borgo San Felice Boutique','Recepção de leads, apresentação da proposta, qualificação por tipo de experiência (grupo ou casal/família) e transferência por protocolo quando o cliente está pronto para reservar.','',cat='agente')
 + gcard('Agente de IA · Beleza e estética','Isabella · Salão Rosa Bella','Recebe leads de anúncios online, conecta e conduz até o agendamento.','',cat='agente')
 + gcard('Agente de IA · Clínica odontológica','Agente de atendimento · Click Odonto','Atendimento integrado ao ERP Click Gest.','',cat='agente')
 + gcard('Automação · A nossa operação','Hub Smart Skills Hub','Agente no WhatsApp, fluxos n8n, nutrição no Mautic e rastreamento do funil. A mesma infraestrutura que entregamos.','Usamos o que vendemos',cat='auto')
 + '</div>', sid='lista')
c += cta('Seu segmento <em>não está aqui?</em>','Os mecanismos são os mesmos. Na demonstração, mostramos como ficam no seu processo.','cases')
page('cases.html','Cases: plataformas, agentes de IA e automações em produção | Smart Skills Hub','Projetos entregues para clínicas, pousadas, salões, escritórios contábeis e anfitriões. Escopo, mecanismo e integrações de cada um.', c, mode='particles', current='cases.html')

# ───────────────────────── SOBRE ─────────────────────────
s = hero('Sobre','Uma equipe de engenharia<br><em>que opera o que constrói</em>',
 'A Smart Skills Hub constrói plataformas, implanta agentes de IA e automatiza processos. Mantemos produtos próprios em produção e rodamos nossa operação na mesma infraestrutura que entregamos.',
 'sobre', scene('hero','Símbolo Smart Skills Hub · cena interativa'), ('#principios','Como pensamos'), cls='hero-3d')
s += section('Princípios','Cinco regras <em>que não negociamos</em>','',
 '<div class="principles reveal">' + ''.join(f'<div class="principle"><div class="n">0{i+1}</div><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate([
  ('Mapear antes de automatizar','Automação em cima de processo confuso só acelera a confusão. Primeiro o desenho, depois o fluxo.'),
  ('Demonstrar antes de explicar','Você vê o agente ou o sistema funcionando com o seu caso antes de ouvir qualquer argumento.'),
  ('Ação real, não botão','Agente que só responde é FAQ. O nosso agenda, cobra, assina e dispara a operação.'),
  ('Limite dito em voz alta','O agente erra e melhora. Por isso existe painel, supervisão da equipe e refinamento mensal.'),
  ('Testar em casa primeiro','WhatsApp API, n8n, Mautic e channel manager rodam na nossa operação antes de ir para o cliente.')])) + '</div>', sid='principios')
s += section('Infraestrutura','O que roda <em>na nossa casa</em>','A mesma infraestrutura atende os nossos clientes e o nosso funil. Quando você manda mensagem para a gente, quem responde primeiro é o nosso agente.',
 '<div class="badges reveal">' + ''.join(f'<span class="int-badge">{b}</span>' for b in ['WhatsApp API','n8n','Mautic','Channel manager','Supabase','Next.js','Cloudflare']) + '</div>', bg='bg-navy')
s += section('Onde estamos','Rio de Janeiro. <em>Atendimento em todo o Brasil.</em>','A implantação é remota e não exige visita presencial. A demonstração acontece por videochamada, com o seu caso na tela.','')
s += cta('Fale com quem <em>vai construir</em>','Na demonstração, quem atende é da equipe de engenharia, não um vendedor com roteiro.','sobre')
page('sobre.html','Sobre a Smart Skills Hub | Engenharia de produto, IA e automação','Equipe de engenharia que constrói plataformas, implanta agentes de IA e automatiza processos para empresas de serviços. Operamos o nosso próprio hub antes de levar ao cliente.', s, mode='hero', current='sobre.html')

# ───────────────────────── WHATSAPP (intermediária) ─────────────────────────
w = f'''<section class="wa-page"><div class="hero-grid-bg"></div><div class="box">
<a class="nav-logo" href="index.html" style="justify-content:center;margin-bottom:2.5rem">{SYMBOL}<div class="nav-logo-text">SMART<span>SKILLS</span></div></a>
<div class="hero-tag">Atendimento</div>
<h1 class="hero-title">Você vai falar<br><em>com a nossa equipe</em></h1>
<p>O primeiro contato é o nosso agente de IA. Ele entende o que você precisa e passa para a pessoa certa da equipe. É o mesmo agente que implantamos nos clientes.</p>
<a id="wa-open" href="{WA}" class="btn-primary" target="_blank" rel="noopener noreferrer">{WA_ICON}Abrir o WhatsApp</a>
<div class="meta">{PHONE} · resposta por pessoa da equipe em horário comercial<br>fora dele, o agente registra e agenda</div>
<p style="margin-top:2rem"><a class="btn-secondary" href="mailto:{MAIL}">Prefiro e-mail · {MAIL} {ARROW}</a></p>
</div></section>'''
page('whatsapp.html','Falar com a Smart Skills Hub no WhatsApp','Abra uma conversa com a equipe da Smart Skills Hub no WhatsApp.', w, minimal=True)

# 404
page('404.html','Página não encontrada | Smart Skills Hub','', f'''<section class="wa-page"><div class="hero-grid-bg"></div><div class="box"><div class="hero-tag">404</div><h1 class="hero-title">Essa página<br><em>não está em produção</em></h1><p>O link pode ter mudado quando o site cresceu. Os caminhos abaixo funcionam.</p><div class="seg-pills" style="justify-content:center">{"".join(f'<a class="seg-pill" href="{h}">{t}</a>' for h,t in [("index.html","Início")]+NAV)}</div></div></section>''')
