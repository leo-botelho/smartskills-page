// GET /api/diag — diagnóstico do tracking. Protegido por Basic Auth (_middleware.js).
// Mostra o que está configurado e o erro exato do Supabase, sem revelar segredos.

function lerJwt(chave) {
  // Chaves antigas do Supabase são JWT: dá para ler o papel sem expor a chave.
  try {
    const p = chave.split('.');
    if (p.length !== 3) return null;
    const payload = JSON.parse(atob(p[1].replace(/-/g, '+').replace(/_/g, '/')));
    return { papel: payload.role ?? null, projeto: payload.ref ?? null };
  } catch {
    return null;
  }
}

function descreverChave(chave) {
  if (!chave) return { definida: false };
  const jwt = lerJwt(chave);
  return {
    definida: true,
    tamanho: chave.length,
    inicio: chave.slice(0, 8) + '…',
    formato: jwt ? 'JWT (chave clássica)' : (chave.startsWith('sb_secret_') ? 'sb_secret (chave nova)' : 'desconhecido'),
    papel: jwt?.papel ?? (chave.startsWith('sb_secret_') ? 'secret' : null),
    projeto: jwt?.projeto ?? null,
    alerta: jwt?.papel && jwt.papel !== 'service_role'
      ? `Esta chave é "${jwt.papel}", não "service_role". Use a service_role em SUPABASE_SERVICE_ROLE_KEY.`
      : (chave.startsWith('sb_publishable') ? 'Esta é a chave publicável, não a secreta.' : null),
  };
}

async function tentar(nome, fn) {
  const t0 = Date.now();
  try {
    const r = await fn();
    const corpo = await r.text();
    return {
      teste: nome,
      ok: r.ok,
      status: r.status,
      ms: Date.now() - t0,
      resposta: corpo.slice(0, 400) || '(vazia)',
    };
  } catch (e) {
    return { teste: nome, ok: false, erro: e.message, ms: Date.now() - t0 };
  }
}

export async function onRequestGet(ctx) {
  const { env, request } = ctx;
  const url = (env.SUPABASE_URL || '').replace(/\/+$/, '');
  const key = env.SUPABASE_SERVICE_ROLE_KEY || '';
  const cabecalhos = { apikey: key, authorization: `Bearer ${key}`, 'content-type': 'application/json' };

  const diag = {
    quando: new Date().toISOString(),
    variaveis: {
      SUPABASE_URL: url ? new URL(url).host : '❌ NÃO DEFINIDA',
      SUPABASE_SERVICE_ROLE_KEY: descreverChave(key),
      IP_SALT: env.IP_SALT ? 'definida' : '❌ não definida',
      PAINEL_USUARIO: env.PAINEL_USUARIO ? 'definida' : '❌ não definida',
      ARMAZENAR_IP_BRUTO: env.ARMAZENAR_IP_BRUTO ?? '(padrão: true)',
      destinos_externos: {
        ga4: !!(env.GA4_MEASUREMENT_ID && env.GA4_API_SECRET),
        meta_capi: !!(env.META_PIXEL_ID && env.META_CAPI_TOKEN),
        webhook: !!env.WEBHOOK_URL,
      },
    },
    geolocalizacao: request.cf
      ? { disponivel: true, pais: request.cf.country, cidade: request.cf.city, colo: request.cf.colo }
      : { disponivel: false, nota: 'request.cf ausente (normal em ambiente local, não em produção)' },
    testes: [],
  };

  if (!url || !key) {
    diag.conclusao = 'Faltam SUPABASE_URL e/ou SUPABASE_SERVICE_ROLE_KEY no ambiente Production.';
    return Response.json(diag, { status: 200 });
  }

  // 1. A Data API responde?
  diag.testes.push(await tentar('data_api_alcancavel', () =>
    fetch(`${url}/rest/v1/`, { headers: cabecalhos, signal: AbortSignal.timeout(8000) })));

  // 2. O schema tracking está exposto? (leitura simples na tabela)
  diag.testes.push(await tentar('schema_tracking_exposto', () =>
    fetch(`${url}/rest/v1/eventos?select=id&limit=1`, {
      headers: { ...cabecalhos, 'accept-profile': 'tracking' },
      signal: AbortSignal.timeout(8000),
    })));

  // 3. Consegue gravar? (insere uma linha marcada como diagnóstico)
  diag.testes.push(await tentar('insert_de_teste', () =>
    fetch(`${url}/rest/v1/eventos`, {
      method: 'POST',
      headers: { ...cabecalhos, 'content-profile': 'tracking', prefer: 'return=minimal' },
      body: JSON.stringify([{
        visitante_id: crypto.randomUUID(),
        sessao_id: crypto.randomUUID(),
        evento: 'diagnostico',
        is_bot: true,               // marcado como bot: não entra nas métricas do painel
        caminho: '/api/diag',
        geo_fonte: 'cloudflare',
        pais: request.cf?.country ?? null,
        cidade: request.cf?.city ?? null,
      }]),
      signal: AbortSignal.timeout(8000),
    })));

  // 4. A função do painel responde?
  diag.testes.push(await tentar('rpc_painel', () =>
    fetch(`${url}/rest/v1/rpc/painel`, {
      method: 'POST',
      headers: { ...cabecalhos, 'content-profile': 'tracking' },
      body: JSON.stringify({ p_dias: 7 }),
      signal: AbortSignal.timeout(10000),
    })));

  const falhou = diag.testes.find((t) => !t.ok);
  diag.conclusao = falhou
    ? `Falhou em "${falhou.teste}" (status ${falhou.status ?? 'sem resposta'}). Veja o campo "resposta" desse teste.`
    : 'Tudo certo: a Function grava e lê no Supabase. Apague as linhas de diagnóstico com: delete from tracking.eventos where evento in (\'diagnostico\',\'teste_deploy\');';

  return Response.json(diag, { status: 200, headers: { 'cache-control': 'no-store' } });
}
