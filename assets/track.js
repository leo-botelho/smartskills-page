// Tracking first-party da Smart Skills Hub.
// Manda o mínimo para /api/collect (mesmo domínio). IP, user agent e geolocalização
// são preenchidos no servidor — o navegador não coleta nada disso.
(function () {
  'use strict';
  var ENDPOINT = '/api/collect';
  var enviados = {};

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
      click_id: q.get('gclid') || q.get('fbclid') || q.get('ttclid'),
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

  // pageview
  if (document.readyState === 'loading') addEventListener('DOMContentLoaded', function () { enviar('pageview'); });
  else enviar('pageview');

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
