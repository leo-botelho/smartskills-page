// Atribuição: garante que utm_source nunca fique vazia e classifica a origem.
// Ideia adaptada do script de rastreio 4.0 (Nova Ordem do Digital): quando a visita
// chega sem UTM, o referrer vira a origem; sem referrer, a origem é "direto".

const BUSCADORES = /(^|\.)(google|bing|duckduckgo|yahoo|ecosia|brave|yandex|baidu|search\.marginalia)\./i;
const REDES = {
  'instagram.com': 'instagram', 'l.instagram.com': 'instagram', 'lm.instagram.com': 'instagram',
  'facebook.com': 'facebook', 'l.facebook.com': 'facebook', 'lm.facebook.com': 'facebook', 'm.facebook.com': 'facebook',
  'linkedin.com': 'linkedin', 'lnkd.in': 'linkedin',
  't.co': 'twitter', 'twitter.com': 'twitter', 'x.com': 'twitter',
  'youtube.com': 'youtube', 'm.youtube.com': 'youtube', 'youtu.be': 'youtube',
  'tiktok.com': 'tiktok', 'pinterest.com': 'pinterest', 'reddit.com': 'reddit',
  'whatsapp.com': 'whatsapp', 'wa.me': 'whatsapp', 'web.whatsapp.com': 'whatsapp',
  't.me': 'telegram', 'telegram.org': 'telegram',
};

const limpo = (h) => String(h || '').replace(/^www\./, '').toLowerCase();

/**
 * Descobre origem e meio a partir do referrer.
 * Devolve null quando o referrer é do próprio site ou não existe.
 */
export function daReferrer(referrerHost, hostDoSite) {
  const h = limpo(referrerHost);
  if (!h) return null;
  if (h === limpo(hostDoSite)) return null;               // navegação interna não é nova origem
  const rede = REDES[h];
  if (rede) return { utm_source: rede, utm_medium: 'social' };
  if (BUSCADORES.test(h)) return { utm_source: h.split('.').slice(-3).join('.').replace(/^(www|m)\./, ''), utm_medium: 'organic' };
  return { utm_source: h, utm_medium: 'referral' };
}

/**
 * Monta a atribuição final do evento, nesta ordem de prioridade:
 *   1. UTMs na URL da página (clique novo em campanha manda no resultado)
 *   2. UTMs guardadas do próprio visitante (a origem da visita continua valendo nas páginas seguintes)
 *   3. Referrer traduzido em origem
 *   4. "direto"
 */
export function resolverAtribuicao({ daUrl, doCookie, referrerHost, hostDoSite, temClickId }) {
  const url = daUrl || {};
  const cookie = doCookie || {};

  // Um clique de anúncio (gclid/fbclid) ou qualquer utm na URL inicia uma atribuição nova.
  const urlTemFonte = !!(url.utm_source || url.utm_medium || url.utm_campaign || temClickId);

  if (urlTemFonte) {
    const daRef = daReferrer(referrerHost, hostDoSite);
    return {
      utm_source: url.utm_source || daRef?.utm_source || (temClickId ? 'anuncio' : 'direto'),
      utm_medium: url.utm_medium || (temClickId ? 'cpc' : daRef?.utm_medium || 'direto'),
      utm_campaign: url.utm_campaign || null,
      utm_content: url.utm_content || null,
      utm_term: url.utm_term || null,
      novo: true,
    };
  }

  if (cookie.utm_source) {
    return { ...cookie, novo: false };
  }

  const daRef = daReferrer(referrerHost, hostDoSite);
  if (daRef) {
    return { ...daRef, utm_campaign: null, utm_content: null, utm_term: null, novo: true };
  }

  return { utm_source: 'direto', utm_medium: 'direto', utm_campaign: null, utm_content: null, utm_term: null, novo: true };
}
