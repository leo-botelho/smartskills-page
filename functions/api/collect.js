// POST /api/collect — coleta server-side, first-party.
// O navegador manda o mínimo (evento, página, UTMs). Quem enriquece com IP,
// user agent e geolocalização é esta função. Nada de tag manager, nada de terceiro.

import { resolverGeo } from '../_lib/geo.js';
import { lerUA } from '../_lib/ua.js';
import { inserir } from '../_lib/supabase.js';
import { encaminharDestinos } from '../_lib/destinos.js';

const COOKIE_VISITANTE = 'ssh_vid';
const COOKIE_SESSAO = 'ssh_sid';
const SESSAO_MIN = 30;              // sessão expira com 30 min de inatividade
const VISITANTE_DIAS = 365;
const CONVERSOES = new Set(['whatsapp_click', 'email_click', 'form_submit', 'demo_agendada']);
const LIMITE_TEXTO = 2048;

const corta = (v, n = 512) => (typeof v === 'string' && v ? v.slice(0, n) : null);
const uuid = () => crypto.randomUUID();

function lerCookies(request) {
  const out = {};
  const raw = request.headers.get('cookie') || '';
  for (const parte of raw.split(';')) {
    const i = parte.indexOf('=');
    if (i > 0) out[parte.slice(0, i).trim()] = decodeURIComponent(parte.slice(i + 1).trim());
  }
  return out;
}

function cookie(nome, valor, maxAgeSeg, dominio) {
  const p = [
    `${nome}=${valor}`,
    'Path=/',
    'Secure',
    'HttpOnly',
    'SameSite=Lax',
    `Max-Age=${maxAgeSeg}`,
  ];
  if (dominio) p.push(`Domain=${dominio}`);
  return p.join('; ');
}

async function sha256(texto) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(texto));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

const EHUUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function host(u) {
  try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return null; }
}

export async function onRequestPost(ctx) {
  const { request, env } = ctx;

  // Só aceita chamada do próprio site (é tracking first-party, não endpoint público).
  const origem = request.headers.get('origin');
  const alvo = new URL(request.url);
  if (origem && host(origem) !== alvo.hostname.replace(/^www\./, '') && env.PERMITIR_ORIGEM !== '*') {
    return new Response(null, { status: 403 });
  }

  let corpo = {};
  try {
    const texto = await request.text();
    if (texto.length > 8192) return new Response(null, { status: 413 });
    corpo = texto ? JSON.parse(texto) : {};
  } catch {
    return new Response(null, { status: 400 });
  }

  const evento = corta(corpo.evento, 64);
  if (!evento) return new Response(null, { status: 400 });

  // ── identidade em cookie first-party, gerada no servidor ──────────────
  const cookies = lerCookies(request);
  let visitante = EHUUID.test(cookies[COOKIE_VISITANTE] || '') ? cookies[COOKIE_VISITANTE] : uuid();
  let sessao = EHUUID.test(cookies[COOKIE_SESSAO] || '') ? cookies[COOKIE_SESSAO] : null;
  const sessaoNova = !sessao;
  if (!sessao) sessao = uuid();

  // ── enriquecimento no servidor ────────────────────────────────────────
  const ip = request.headers.get('cf-connecting-ip')
          || request.headers.get('x-forwarded-for')?.split(',')[0].trim()
          || null;
  const ua = request.headers.get('user-agent') || '';
  const { navegador, so, dispositivo, is_bot } = lerUA(ua);
  const geo = await resolverGeo(request, env, ip);
  const ipHash = ip ? await sha256(ip + (env.IP_SALT || 'smartskills')) : null;
  const guardarIpBruto = String(env.ARMAZENAR_IP_BRUTO ?? 'true') === 'true';

  const url = corta(corpo.url, LIMITE_TEXTO);
  const ref = corta(corpo.referrer, LIMITE_TEXTO);
  const q = (() => { try { return new URL(url).searchParams; } catch { return new URLSearchParams(); } })();
  const p = (k) => corta(corpo[k] ?? q.get(k), 255);

  const linha = {
    ocorrido_em: corpo.ts ? new Date(corpo.ts).toISOString() : new Date().toISOString(),
    visitante_id: visitante,
    sessao_id: sessao,
    sessao_nova: sessaoNova,

    evento,
    conversao: CONVERSOES.has(evento),
    valor: Number.isFinite(corpo.valor) ? corpo.valor : null,

    url,
    caminho: corta(corpo.caminho ?? (() => { try { return new URL(url).pathname; } catch { return null; } })(), 512),
    titulo: corta(corpo.titulo, 255),
    referrer: ref,
    referrer_host: host(ref),

    origem: p('origem'),
    utm_source: p('utm_source'),
    utm_medium: p('utm_medium'),
    utm_campaign: p('utm_campaign'),
    utm_content: p('utm_content'),
    utm_term: p('utm_term'),
    click_id: corta(corpo.click_id ?? q.get('gclid') ?? q.get('fbclid') ?? q.get('ttclid'), 255),

    ip: guardarIpBruto ? ip : null,
    ip_hash: ipHash,
    user_agent: corta(ua, LIMITE_TEXTO),
    navegador, so, dispositivo, is_bot,
    idioma: corta(corpo.idioma ?? request.headers.get('accept-language'), 64),
    tela: corta(corpo.tela, 32),
    viewport: corta(corpo.viewport, 32),

    ...geo,
    extras: (corpo.extras && typeof corpo.extras === 'object') ? corpo.extras : {},
  };

  // Responde na hora; a gravação segue em background (não segura o usuário).
  ctx.waitUntil((async () => {
    try {
      await inserir(env, 'tracking', 'eventos', linha);
    } catch (e) {
      console.error('collect: falha ao gravar', e.message);
    }
    try {
      await encaminharDestinos(env, linha);   // GA4 / Meta CAPI, se configurados
    } catch (e) {
      console.error('collect: falha ao encaminhar', e.message);
    }
  })());

  const dominio = env.COOKIE_DOMINIO || null;
  const headers = new Headers({
    'cache-control': 'no-store',
    'content-type': 'application/json',
  });
  headers.append('set-cookie', cookie(COOKIE_VISITANTE, visitante, VISITANTE_DIAS * 86400, dominio));
  headers.append('set-cookie', cookie(COOKIE_SESSAO, sessao, SESSAO_MIN * 60, dominio));
  return new Response(JSON.stringify({ ok: true }), { status: 202, headers });
}

// Fallback sem JavaScript: <img src="/api/collect?evento=pageview&...">
export async function onRequestGet(ctx) {
  const u = new URL(ctx.request.url);
  if (!u.searchParams.get('evento')) return new Response(null, { status: 400 });
  const corpo = Object.fromEntries(u.searchParams.entries());
  corpo.url = corpo.url || ctx.request.headers.get('referer') || null;
  const req = new Request(ctx.request.url, {
    method: 'POST',
    headers: ctx.request.headers,
    body: JSON.stringify(corpo),
  });
  Object.defineProperty(req, 'cf', { value: ctx.request.cf });
  const r = await onRequestPost({ ...ctx, request: req });
  // devolve 1x1 transparente
  const gif = Uint8Array.from(atob('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'), (c) => c.charCodeAt(0));
  const h = new Headers(r.headers);
  h.set('content-type', 'image/gif');
  h.set('cache-control', 'no-store');
  return new Response(gif, { status: 200, headers: h });
}
