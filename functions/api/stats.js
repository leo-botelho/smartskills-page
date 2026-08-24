// GET /api/stats?dias=30 — dados do dashboard, em uma chamada só.
// Protegido por Basic Auth (o mesmo do /dashboard.html, aplicado no _middleware.js).

import { rpc } from '../_lib/supabase.js';

export async function onRequestGet(ctx) {
  const dias = Math.min(Math.max(parseInt(new URL(ctx.request.url).searchParams.get('dias') || '30', 10) || 30, 1), 365);
  try {
    const dados = await rpc(ctx.env, 'tracking', 'painel', { p_dias: dias });
    return new Response(JSON.stringify(dados), {
      headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
    });
  } catch (e) {
    return new Response(JSON.stringify({ erro: e.message }), {
      status: 500,
      headers: { 'content-type': 'application/json' },
    });
  }
}
