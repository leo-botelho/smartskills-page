// Tracking first-party da Smart Skills Hub.
// Manda o mínimo para /api/collect (mesmo domínio). IP, user agent e geolocalização
// são preenchidos no servidor — o navegador não coleta nada disso.
(function () {
  'use strict';
  var ENDPOINT = '/api/collect';
  var COOKIE_EID = 'ssh_eid';
  var MARCADOR = 'cod.';            // vira "[cod. 784975675]" na mensagem do WhatsApp
  var RE_CODIGO = /^[1-9][0-9]{8}$/;
  var RE_MARCA = /\s*\[cod\.\s*\d{9}\]/g;
  var enviados = {};

  function lerCookie(nome) {
    var m = ('; ' + document.cookie).split('; ' + nome + '=');
    return m.length === 2 ? decodeURIComponent(m.pop().split(';').shift()) : null;
  }

  // Protocolo do visitante. O servidor valida e grava; aqui geramos um candidato na
  // primeira visita para o link do WhatsApp já sair com o código, sem depender da
  // resposta da primeira requisição.
  function protocolo() {
    var c = lerCookie(COOKIE_EID);
    if (RE_CODIGO.test(c || '')) return c;
    if (!protocolo.candidato) {
      var n = new Uint32Array(1);
      (window.crypto || window.msCrypto).getRandomValues(n);
      protocolo.candidato = String(100000000 + (n[0] % 900000000));
    }
    return protocolo.candidato;
  }

  function linksWhats() {
    return document.querySelectorAll('a[href*="wa.me"], a[href*="api.whatsapp.com"]');
  }

  // Acrescenta "[cod. XXXXXXXXX]" ao texto de todo link de WhatsApp da página.
  function marcarLinks() {
    var cod = protocolo();
    if (!cod) return;
    var links = linksWhats();
    for (var i = 0; i < links.length; i++) {
      try {
        var u = new URL(links[i].getAttribute('href') || '', location.href);
        var texto = (u.searchParams.get('text') || '').replace(RE_MARCA, '');
        u.searchParams.set('text', texto + ' [' + MARCADOR + ' ' + cod + ']');
        links[i].setAttribute('href', u.toString());
      } catch (e) { /* link fora do padrão: deixa como está */ }
    }
  }

  function ctx() {
    var q = new URLSearchParams(location.search);
    return {
      url: location.href,
      caminho: location.pathname,
      titulo: document.title,
      referrer: document.referrer || null,
      idioma: navigator.language,
      tela: screen.width + 'x' + screen.height,
      viewport: innerWidth + 'x' + innerHeight,
      origem: q.get('origem'),
      utm_source: q.get('utm_source'),
      utm_medium: q.get('utm_medium'),
      utm_campaign: q.get('utm_campaign'),
      utm_content: q.get('utm_content'),
      utm_term: q.get('utm_term'),
      gclid: q.get('gclid') || q.get('wbraid') || q.get('gbraid'),
      fbclid: q.get('fbclid'),
      click_id: q.get('gclid') || q.get('fbclid') || q.get('ttclid'),
      external_id: protocolo(),
      ts: new Date().toISOString()
    };
  }

  function enviar(evento, extras) {
    var corpo = ctx();
    corpo.evento = evento;
    if (extras) corpo.extras = extras;
    var json = JSON.stringify(corpo);
    // sendBeacon sobrevive à saída da página; fetch keepalive é o plano B
    if (navigator.sendBeacon) {
      navigator.sendBeacon(ENDPOINT, new Blob([json], { type: 'application/json' }));
    } else {
      fetch(ENDPOINT, { method: 'POST', body: json, keepalive: true, credentials: 'same-origin',
                        headers: { 'content-type': 'application/json' } }).catch(function () {});
    }
  }

  function umaVez(evento, extras) {
    if (enviados[evento]) return;
    enviados[evento] = 1;
    enviar(evento, extras);
  }

  window.ssTrack = enviar;

  // pageview + marcação dos links de WhatsApp com o protocolo
  function iniciar() {
    marcarLinks();
    var corpo = ctx();
    corpo.evento = 'pageview';
    fetch(ENDPOINT, {
      method: 'POST', credentials: 'same-origin', keepalive: true,
      headers: { 'content-type': 'application/json' }, body: JSON.stringify(corpo)
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        // Visitante já conhecido: o servidor devolve o código dele, que vale mais que o candidato.
        if (d && RE_CODIGO.test(d.external_id || '') && d.external_id !== protocolo()) {
          protocolo.candidato = d.external_id;
          marcarLinks();
        }
      })
      .catch(function () { /* rede indisponível: o pageview se perde, sem quebrar a página */ });
  }
  if (document.readyState === 'loading') addEventListener('DOMContentLoaded', iniciar);
  else iniciar();

  // profundidade de rolagem
  addEventListener('scroll', function () {
    var h = document.documentElement;
    var pct = (h.scrollTop + innerHeight) / h.scrollHeight * 100;
    if (pct >= 50) umaVez('scroll_50');
    if (pct >= 90) umaVez('scroll_90');
  }, { passive: true });

  // tempo na página
  setTimeout(function () { umaVez('tempo_30s'); }, 30000);

  // cliques que importam: WhatsApp, e-mail e qualquer [data-track]
  addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a, [data-track]');
    if (!a) return;
    var nome = a.getAttribute('data-track');
    var href = a.getAttribute('href') || '';
    if (nome) return enviar(nome, { texto: (a.textContent || '').trim().slice(0, 80), href: href });
    if (/^https?:\/\/(wa\.me|api\.whatsapp\.com)/.test(href) || /whatsapp\.html/.test(href))
      return enviar('whatsapp_click', { href: href });
    if (/^mailto:/.test(href)) return enviar('email_click', { href: href });
    if (/^https?:/.test(href) && href.indexOf(location.host) === -1)
      return enviar('clique_externo', { href: href.slice(0, 300) });
  }, true);
})();
