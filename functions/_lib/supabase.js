// Acesso ao Supabase pela API REST (PostgREST). Sem SDK: menos bundle, menos cold start.
// A service_role key vive só como secret da função. O navegador nunca a vê.

function base(env) {
  const url = (env.SUPABASE_URL || '').replace(/\/+$/, '');
  const key = env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw new Error('SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY não configuradas');
  return { url, key };
}

function headers(key, extra = {}) {
  return { apikey: key, authorization: `Bearer ${key}`, 'content-type': 'application/json', ...extra };
}

/** Insere linhas em uma tabela de um schema. */
export async function inserir(env, schema, tabela, linhas) {
  const { url, key } = base(env);
  const r = await fetch(`${url}/rest/v1/${tabela}`, {
    method: 'POST',
    headers: headers(key, {
      'content-profile': schema,          // grava no schema tracking, não no public
      prefer: 'return=minimal',           // resposta vazia = mais rápido
    }),
    body: JSON.stringify(Array.isArray(linhas) ? linhas : [linhas]),
    signal: AbortSignal.timeout(5000),
  });
  if (!r.ok) throw new Error(`supabase insert ${r.status}: ${(await r.text()).slice(0, 300)}`);
  return true;
}

/** Chama uma function do Postgres (RPC). */
export async function rpc(env, schema, funcao, args = {}) {
  const { url, key } = base(env);
  const r = await fetch(`${url}/rest/v1/rpc/${funcao}`, {
    method: 'POST',
    headers: headers(key, { 'content-profile': schema, accept: 'application/json' }),
    body: JSON.stringify(args),
    signal: AbortSignal.timeout(10000),
  });
  if (!r.ok) throw new Error(`supabase rpc ${r.status}: ${(await r.text()).slice(0, 300)}`);
  return r.json();
}
