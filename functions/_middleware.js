// Protege o dashboard e a API de estatísticas com Basic Auth.
// O resto do site (páginas públicas e /api/collect) passa direto.

const PROTEGIDO = [/^\/dashboard(\.html)?$/, /^\/api\/stats$/];

// Arquivos do repositório que não devem ser servidos no domínio.
// Regra de _redirects não resolve: asset existente tem precedência sobre redirect.
// Function tem precedência sobre asset, então o bloqueio vive aqui.
const INTERNO = [
  /^\/supabase\//,
  /^\/(TRACKING|README)\.md$/i,
  /^\/build\.py$/i,
  /^\/package(-lock)?\.json$/i,
  /^\/wrangler\.jsonc?$/i,
  /^\/\.dev\.vars/i,
];

function naoAutorizado() {
  return new Response('Acesso restrito', {
    status: 401,
    headers: {
      'www-authenticate': 'Basic realm="Smart Skills Hub", charset="UTF-8"',
      'cache-control': 'no-store',
    },
  });
}

// Comparação em tempo constante, para não vazar a senha por timing.
function iguais(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

export async function onRequest(ctx) {
  const url = new URL(ctx.request.url);

  if (INTERNO.some((r) => r.test(url.pathname))) {
    return new Response('Não encontrado', { status: 404, headers: { 'content-type': 'text/plain; charset=utf-8' } });
  }

  if (!PROTEGIDO.some((r) => r.test(url.pathname))) return ctx.next();

  const usuario = ctx.env.PAINEL_USUARIO;
  const senha = ctx.env.PAINEL_SENHA;
  if (!usuario || !senha) {
    return new Response('Painel sem credenciais configuradas (PAINEL_USUARIO / PAINEL_SENHA).', { status: 503 });
  }

  const auth = ctx.request.headers.get('authorization') || '';
  if (!auth.startsWith('Basic ')) return naoAutorizado();

  let decodificado = '';
  try { decodificado = atob(auth.slice(6)); } catch { return naoAutorizado(); }
  const i = decodificado.indexOf(':');
  const u = decodificado.slice(0, i);
  const s = decodificado.slice(i + 1);
  if (!iguais(u, usuario) || !iguais(s, senha)) return naoAutorizado();

  return ctx.next();
}
