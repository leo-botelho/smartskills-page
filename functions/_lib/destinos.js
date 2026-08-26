// Encaminhamento server-side para destinos externos (opcional).
// A vantagem do tracking próprio: um ponto de coleta, vários destinos.
// Cada destino só liga quando as variáveis dele existem. Sem variável, nada é enviado.

async function sha256Hex(v) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(String(v).trim().toLowerCase()));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

/** GA4 via Measurement Protocol. */
async function ga4(env, e) {
  if (!env.GA4_MEASUREMENT_ID || !env.GA4_API_SECRET) return;
  const url = `https://www.google-analytics.com/mp/collect?measurement_id=${env.GA4_MEASUREMENT_ID}&api_secret=${env.GA4_API_SECRET}`;
  await fetch(url, {
    method: 'POST',
    body: JSON.stringify({
      client_id: e.visitante_id,
      events: [{
        name: e.evento,
        params: {
          session_id: e.sessao_id,
          page_location: e.url,
          page_title: e.titulo,
          campaign: e.utm_campaign,
          source: e.utm_source,
          medium: e.utm_medium,
          content: e.utm_content,
          origem: e.origem,
          external_id: e.external_id,
          gclid: e.gclid,
          engagement_time_msec: 1,
        },
      }],
    }),
    signal: AbortSignal.timeout(3000),
  });
}

/** Meta Conversions API (só para conversões, com IP e UA — é o que dá qualidade ao match). */
async function metaCapi(env, e) {
  if (!env.META_PIXEL_ID || !env.META_CAPI_TOKEN || !e.conversao) return;
  const url = `https://graph.facebook.com/v21.0/${env.META_PIXEL_ID}/events?access_token=${env.META_CAPI_TOKEN}`;
  const user_data = {
    client_ip_address: e.ip || undefined,
    client_user_agent: e.user_agent || undefined,
    // O protocolo é o identificador que também viaja na conversa do WhatsApp,
    // então serve para casar conversão online e fechamento offline depois.
    external_id: e.external_id
      ? [await sha256Hex(e.external_id), await sha256Hex(e.visitante_id)]
      : await sha256Hex(e.visitante_id),
  };
  if (e.cidade) user_data.ct = await sha256Hex(e.cidade);
  if (e.pais) user_data.country = await sha256Hex(e.pais);
  if (e.regiao_codigo) user_data.st = await sha256Hex(e.regiao_codigo);
  // fbc: identifica o clique no anúncio. É o que mais pesa na qualidade da correspondência.
  if (e.extras?.fbc) user_data.fbc = e.extras.fbc;
  await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      data: [{
        event_name: e.evento === 'whatsapp_click' ? 'Contact' : e.evento,
        // event_id permite deduplicar caso um pixel de navegador seja adicionado depois.
        event_id: `${e.sessao_id}-${e.evento}-${Math.floor(new Date(e.ocorrido_em).getTime() / 1000)}`,
        event_time: Math.floor(new Date(e.ocorrido_em).getTime() / 1000),
        event_source_url: e.url,
        action_source: 'website',
        user_data,
        custom_data: { origem: e.origem, campanha: e.utm_campaign, conteudo: e.utm_content, protocolo: e.external_id },
      }],
      ...(env.META_TEST_EVENT_CODE ? { test_event_code: env.META_TEST_EVENT_CODE } : {}),
    }),
    signal: AbortSignal.timeout(3000),
  });
}

/** Webhook livre (n8n, por exemplo) — útil para avisar a equipe de uma conversão na hora. */
async function webhook(env, e) {
  if (!env.WEBHOOK_URL) return;
  if (String(env.WEBHOOK_SO_CONVERSOES ?? 'true') === 'true' && !e.conversao) return;
  await fetch(env.WEBHOOK_URL, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      ...(env.WEBHOOK_TOKEN ? { authorization: `Bearer ${env.WEBHOOK_TOKEN}` } : {}),
    },
    body: JSON.stringify(e),
    signal: AbortSignal.timeout(3000),
  });
}

export async function encaminharDestinos(env, evento) {
  const r = await Promise.allSettled([ga4(env, evento), metaCapi(env, evento), webhook(env, evento)]);
  for (const x of r) if (x.status === 'rejected') console.error('destino falhou:', x.reason?.message);
}
