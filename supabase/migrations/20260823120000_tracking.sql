-- Tracking first-party da Smart Skills Hub
-- Coleta server-side (Cloudflare Pages Functions) → Supabase. Sem tag manager e sem terceiros.
-- O navegador nunca fala com o Supabase: quem escreve é a função com a service_role key.

create schema if not exists tracking;

-- ─────────────────────────────────────────────────────────────
-- Tabela principal: um registro por evento
-- ─────────────────────────────────────────────────────────────
create table if not exists tracking.eventos (
  id              bigserial primary key,
  criado_em       timestamptz not null default now(),
  ocorrido_em     timestamptz not null default now(),   -- horário do cliente, se enviado

  -- identidade (cookies first-party, HttpOnly, gerados no servidor)
  visitante_id    uuid not null,
  sessao_id       uuid not null,
  sessao_nova     boolean not null default false,

  -- evento
  evento          text not null,                         -- pageview, scroll_50, clique_cta, whatsapp_click...
  conversao       boolean not null default false,
  valor           numeric(12,2),                         -- opcional, para eventos com valor

  -- página
  url             text,
  caminho         text,
  titulo          text,
  referrer        text,
  referrer_host   text,

  -- origem / campanha
  origem          text,                                  -- parâmetro ?origem= do nosso próprio padrão
  utm_source      text,
  utm_medium      text,
  utm_campaign    text,
  utm_content     text,
  utm_term        text,
  click_id        text,                                  -- gclid / fbclid / ttclid

  -- rede e dispositivo (preenchidos no servidor)
  ip              inet,                                  -- ver ARMAZENAR_IP_BRUTO e política de retenção
  ip_hash         text,                                  -- sha256(ip + salt), sempre preenchido
  user_agent      text,
  navegador       text,
  so              text,
  dispositivo     text,                                  -- desktop | mobile | tablet | bot
  is_bot          boolean not null default false,
  idioma          text,
  tela            text,                                  -- 1920x1080
  viewport        text,

  -- geolocalização (API própria: request.cf da Cloudflare, sem chamada externa)
  geo_fonte       text,                                  -- cloudflare | api_propria | header
  pais            text,
  regiao          text,
  regiao_codigo   text,
  cidade          text,
  cep             text,
  latitude        numeric(9,6),
  longitude       numeric(9,6),
  fuso            text,
  continente      text,
  asn             integer,
  as_org          text,
  colo            text,                                  -- datacenter que atendeu

  extras          jsonb not null default '{}'::jsonb
);

comment on table tracking.eventos is 'Eventos de tracking coletados server-side. IP é dado pessoal (LGPD): ver função tracking.limpar_antigos e a política de retenção no TRACKING.md.';

create index if not exists idx_eventos_criado_em   on tracking.eventos (criado_em desc);
create index if not exists idx_eventos_evento_data on tracking.eventos (evento, criado_em desc);
create index if not exists idx_eventos_sessao      on tracking.eventos (sessao_id);
create index if not exists idx_eventos_visitante   on tracking.eventos (visitante_id);
create index if not exists idx_eventos_campanha    on tracking.eventos (utm_campaign, utm_content) where utm_campaign is not null;
create index if not exists idx_eventos_conversao   on tracking.eventos (criado_em desc) where conversao;
create index if not exists idx_eventos_humanos     on tracking.eventos (criado_em desc) where not is_bot;

-- ─────────────────────────────────────────────────────────────
-- RLS: ninguém lê pelo cliente. Só a service_role (nas funções) enxerga.
-- ─────────────────────────────────────────────────────────────
alter table tracking.eventos enable row level security;
revoke all on tracking.eventos from anon, authenticated;
-- Sem policy para anon/authenticated = acesso negado. service_role ignora RLS.

-- ─────────────────────────────────────────────────────────────
-- Views de leitura para o dashboard
-- ─────────────────────────────────────────────────────────────
create or replace view tracking.vw_sessoes as
select
  sessao_id,
  min(visitante_id::text)::uuid                      as visitante_id,
  min(criado_em)                                     as inicio,
  max(criado_em)                                     as fim,
  extract(epoch from (max(criado_em) - min(criado_em)))::int as duracao_seg,
  count(*) filter (where evento = 'pageview')        as paginas,
  bool_or(conversao)                                 as converteu,
  (array_agg(caminho order by criado_em))[1]         as pagina_entrada,
  (array_agg(caminho order by criado_em desc))[1]    as pagina_saida,
  (array_agg(utm_source order by criado_em) filter (where utm_source is not null))[1] as utm_source,
  (array_agg(utm_medium order by criado_em) filter (where utm_medium is not null))[1] as utm_medium,
  (array_agg(utm_campaign order by criado_em) filter (where utm_campaign is not null))[1] as utm_campaign,
  (array_agg(utm_content order by criado_em) filter (where utm_content is not null))[1] as utm_content,
  (array_agg(origem order by criado_em) filter (where origem is not null))[1] as origem,
  (array_agg(referrer_host order by criado_em) filter (where referrer_host is not null))[1] as referrer_host,
  (array_agg(pais order by criado_em))[1]            as pais,
  (array_agg(cidade order by criado_em))[1]          as cidade,
  (array_agg(dispositivo order by criado_em))[1]     as dispositivo
from tracking.eventos
where not is_bot
group by sessao_id;

create or replace view tracking.vw_resumo_diario as
select
  date_trunc('day', criado_em)::date as dia,
  count(*) filter (where evento = 'pageview')      as pageviews,
  count(distinct sessao_id)                        as sessoes,
  count(distinct visitante_id)                     as visitantes,
  count(*) filter (where conversao)                as conversoes
from tracking.eventos
where not is_bot
group by 1
order by 1 desc;

-- ─────────────────────────────────────────────────────────────
-- Uma chamada só devolve tudo que o dashboard precisa
-- ─────────────────────────────────────────────────────────────
create or replace function tracking.painel(p_dias int default 30)
returns jsonb
language sql
stable
security definer
set search_path = tracking, public
as $$
with base as (
  select * from tracking.eventos
  where criado_em >= now() - make_interval(days => p_dias) and not is_bot
),
sess as (
  select * from tracking.vw_sessoes where inicio >= now() - make_interval(days => p_dias)
)
select jsonb_build_object(
  'periodo_dias', p_dias,
  'gerado_em', now(),
  'totais', (select jsonb_build_object(
      'pageviews',   count(*) filter (where evento = 'pageview'),
      'sessoes',     count(distinct sessao_id),
      'visitantes',  count(distinct visitante_id),
      'conversoes',  count(*) filter (where conversao),
      'taxa_conversao', round(
          coalesce(count(distinct sessao_id) filter (where conversao)::numeric
                   / nullif(count(distinct sessao_id), 0) * 100, 0), 2)
    ) from base),

  'por_dia', (select coalesce(jsonb_agg(jsonb_build_object(
        'dia', dia, 'pageviews', pageviews, 'sessoes', sessoes, 'conversoes', conversoes
      ) order by dia), '[]'::jsonb) from (
      select date_trunc('day', criado_em)::date          as dia,
             count(*) filter (where evento = 'pageview') as pageviews,
             count(distinct sessao_id)                   as sessoes,
             count(*) filter (where conversao)           as conversoes
      from base group by date_trunc('day', criado_em)::date) t),

  'eventos', (select coalesce(jsonb_agg(jsonb_build_object('evento', evento, 'total', total) order by total desc), '[]'::jsonb) from (
      select evento, count(*) as total from base group by evento order by count(*) desc) t),

  'paginas', (select coalesce(jsonb_agg(jsonb_build_object('caminho', caminho, 'total', total) order by total desc), '[]'::jsonb) from (
      select coalesce(caminho, '(sem)') as caminho, count(*) as total
      from base where evento = 'pageview' group by 1 order by 2 desc limit 15) t),

  'campanhas', (select coalesce(jsonb_agg(jsonb_build_object(
        'source', source, 'medium', medium, 'campanha', campanha, 'conteudo', conteudo,
        'sessoes', sessoes, 'conversoes', conversoes) order by sessoes desc), '[]'::jsonb) from (
      select coalesce(utm_source, referrer_host, '(direto)') as source,
             coalesce(utm_medium, '(nenhum)')                as medium,
             coalesce(utm_campaign, '(nenhuma)')             as campanha,
             coalesce(utm_content, '(nenhum)')               as conteudo,
             count(*)                                        as sessoes,
             count(*) filter (where converteu)               as conversoes
      from sess group by 1,2,3,4 order by 5 desc limit 25) t),

  'origens', (select coalesce(jsonb_agg(jsonb_build_object('origem', origem, 'total', total) order by total desc), '[]'::jsonb) from (
      select coalesce(origem, '(sem)') as origem, count(*) as total
      from base where conversao group by 1 order by 2 desc) t),

  'geo_cidades', (select coalesce(jsonb_agg(jsonb_build_object(
        'cidade', cidade, 'regiao', regiao, 'sessoes', sessoes, 'lat', lat, 'lng', lng) order by sessoes desc), '[]'::jsonb) from (
      select coalesce(cidade, '(desconhecida)') as cidade,
             coalesce(pais, '') || case when regiao_codigo is not null then '/' || regiao_codigo else '' end as regiao,
             count(distinct sessao_id) as sessoes,
             round(avg(latitude), 4)  as lat,
             round(avg(longitude), 4) as lng
      from base group by 1, 2 order by 3 desc limit 20) t),

  'geo_paises', (select coalesce(jsonb_agg(jsonb_build_object('pais', pais, 'sessoes', sessoes) order by sessoes desc), '[]'::jsonb) from (
      select coalesce(pais, '??') as pais, count(distinct sessao_id) as sessoes
      from base group by 1 order by 2 desc limit 12) t),

  'dispositivos', (select coalesce(jsonb_agg(jsonb_build_object('dispositivo', dispositivo, 'total', total) order by total desc), '[]'::jsonb) from (
      select coalesce(dispositivo, '?') as dispositivo, count(distinct sessao_id) as total
      from base group by 1 order by 2 desc) t),

  'navegadores', (select coalesce(jsonb_agg(jsonb_build_object('navegador', navegador, 'total', total) order by total desc), '[]'::jsonb) from (
      select coalesce(navegador, '?') as navegador, count(distinct sessao_id) as total
      from base group by 1 order by 2 desc limit 8) t),

  'ultimas_conversas', (select coalesce(jsonb_agg(jsonb_build_object(
        'quando', quando, 'origem', origem, 'campanha', campanha, 'conteudo', conteudo,
        'cidade', cidade, 'pais', pais, 'dispositivo', dispositivo) order by quando desc), '[]'::jsonb) from (
      select criado_em as quando, coalesce(origem, '(sem)') as origem,
             coalesce(utm_campaign, '(nenhuma)') as campanha, coalesce(utm_content, '') as conteudo,
             coalesce(cidade, '') as cidade, coalesce(pais, '') as pais, coalesce(dispositivo, '') as dispositivo
      from base where conversao order by criado_em desc limit 30) t)
);
$$;

revoke all on function tracking.painel(int) from anon, authenticated;

-- ─────────────────────────────────────────────────────────────
-- Retenção (LGPD): apaga eventos antigos e anonimiza IP antes disso
-- ─────────────────────────────────────────────────────────────
create or replace function tracking.limpar_antigos(
  p_dias_ip int default 30,      -- depois disso, some o IP bruto (fica só o hash)
  p_dias_evento int default 180  -- depois disso, some o evento inteiro
)
returns table (ips_anonimizados bigint, eventos_apagados bigint)
language plpgsql
security definer
set search_path = tracking, public
as $$
declare v_ip bigint; v_ev bigint;
begin
  update tracking.eventos set ip = null
   where ip is not null and criado_em < now() - make_interval(days => p_dias_ip);
  get diagnostics v_ip = row_count;

  delete from tracking.eventos
   where criado_em < now() - make_interval(days => p_dias_evento);
  get diagnostics v_ev = row_count;

  return query select v_ip, v_ev;
end;
$$;

-- Agendar a limpeza diária (requer a extensão pg_cron habilitada no projeto):
-- create extension if not exists pg_cron;
-- select cron.schedule('tracking-limpeza', '30 3 * * *', $$select tracking.limpar_antigos(30, 180)$$);
