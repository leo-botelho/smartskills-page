// Geolocalização própria — sem serviço de terceiro no caminho do usuário.
// Ordem: request.cf (Cloudflare, custo zero e sem chamada externa)
//        → headers de visitante (Managed Transform "Add visitor location headers")
//        → GEO_API_URL (uma API sua, se um dia quiser trocar a fonte)

const num = (v) => {
  const n = typeof v === 'string' ? parseFloat(v) : v;
  return Number.isFinite(n) ? n : null;
};

/** Lê o objeto cf que a Cloudflare anexa a cada request. */
export function geoDoCf(cf) {
  if (!cf || typeof cf !== 'object') return null;
  if (!cf.country && !cf.city && !cf.colo) return null;
  return {
    geo_fonte: 'cloudflare',
    pais: cf.country ?? null,
    regiao: cf.region ?? null,
    regiao_codigo: cf.regionCode ?? null,
    cidade: cf.city ?? null,
    cep: cf.postalCode ?? null,
    latitude: num(cf.latitude),
    longitude: num(cf.longitude),
    fuso: cf.timezone ?? null,
    continente: cf.continent ?? null,
    asn: Number.isFinite(cf.asn) ? cf.asn : null,
    as_org: cf.asOrganization ?? null,
    colo: cf.colo ?? null,
  };
}

/** Fallback: headers de localização do visitante (Managed Transform da Cloudflare). */
export function geoDosHeaders(headers) {
  const h = (k) => headers.get(k) || null;
  const pais = h('cf-ipcountry');
  if (!pais && !h('cf-ipcity')) return null;
  return {
    geo_fonte: 'header',
    pais,
    regiao: h('cf-region'),
    regiao_codigo: h('cf-region-code'),
    cidade: h('cf-ipcity'),
    cep: h('cf-postal-code'),
    latitude: num(h('cf-iplatitude')),
    longitude: num(h('cf-iplongitude')),
    fuso: h('cf-timezone'),
    continente: h('cf-ipcontinent'),
    asn: null,
    as_org: null,
    colo: null,
  };
}

/**
 * API própria opcional. Só é chamada se GEO_API_URL estiver configurada e as
 * fontes locais não resolverem. Espera JSON com chaves compatíveis.
 * Timeout curto: tracking nunca pode segurar a resposta ao usuário.
 */
export async function geoDaApiPropria(ip, env) {
  if (!env?.GEO_API_URL || !ip) return null;
  try {
    const url = env.GEO_API_URL.replace('{ip}', encodeURIComponent(ip));
    const r = await fetch(url, {
      headers: env.GEO_API_TOKEN ? { authorization: `Bearer ${env.GEO_API_TOKEN}` } : {},
      signal: AbortSignal.timeout(800),
    });
    if (!r.ok) return null;
    const d = await r.json();
    return {
      geo_fonte: 'api_propria',
      pais: d.pais ?? d.country ?? d.country_code ?? null,
      regiao: d.regiao ?? d.region ?? null,
      regiao_codigo: d.regiao_codigo ?? d.region_code ?? null,
      cidade: d.cidade ?? d.city ?? null,
      cep: d.cep ?? d.postal ?? d.postal_code ?? null,
      latitude: num(d.latitude ?? d.lat),
      longitude: num(d.longitude ?? d.lon ?? d.lng),
      fuso: d.fuso ?? d.timezone ?? null,
      continente: d.continente ?? d.continent ?? null,
      asn: Number.isFinite(d.asn) ? d.asn : num(d.asn),
      as_org: d.as_org ?? d.org ?? null,
      colo: null,
    };
  } catch {
    return null; // nunca derruba a coleta
  }
}

const VAZIO = {
  geo_fonte: null, pais: null, regiao: null, regiao_codigo: null, cidade: null, cep: null,
  latitude: null, longitude: null, fuso: null, continente: null, asn: null, as_org: null, colo: null,
};

export async function resolverGeo(request, env, ip) {
  return geoDoCf(request.cf)
      ?? geoDosHeaders(request.headers)
      ?? (await geoDaApiPropria(ip, env))
      ?? { ...VAZIO };
}
