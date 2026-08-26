-- external_id (protocolo do visitante), click ids separados e atribuição sempre preenchida.
--
-- O external_id é um código curto e numérico gerado na primeira visita. Ele viaja em
-- todo evento, vai para a Meta como identificador, e entra disfarçado na mensagem do
-- WhatsApp ("[cod. 784975675]"), o que permite ligar a conversa à visita que a originou.

alter table tracking.eventos add column if not exists external_id text;
alter table tracking.eventos add column if not exists gclid       text;
alter table tracking.eventos add column if not exists fbclid      text;

comment on column tracking.eventos.external_id is 'Protocolo do visitante: código curto enviado na mensagem do WhatsApp e à Meta como external_id.';

create index if not exists idx_eventos_external_id on tracking.eventos (external_id) where external_id is not null;
create index if not exists idx_eventos_gclid       on tracking.eventos (gclid)       where gclid is not null;

-- ─────────────────────────────────────────────────────────────
-- Sessões passam a expor o protocolo
-- ─────────────────────────────────────────────────────────────
-- "create or replace view" não aceita coluna nova no meio da lista: recriamos a view.
-- Não usa cascade: o corpo de painel() é string, então não é dependência forte.
drop view if exists tracking.vw_sessoes;
create view tracking.vw_sessoes as
select
  sessao_id,
  min(visitante_id::text)::uuid                      as visitante_id,
  (array_agg(external_id order by criado_em) filter (where external_id is not null))[1] as external_id,
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
  (array_agg(gclid order by criado_em) filter (where gclid is not null))[1] as gclid,
  (array_agg(pais order by criado_em))[1]            as pais,
  (array_agg(cidade order by criado_em))[1]          as cidade,
  (array_agg(dispositivo order by criado_em))[1]     as dispositivo
from tracking.eventos
where not is_bot
group by sessao_id;

-- ─────────────────────────────────────────────────────────────
-- Consulta de atendimento: o lead manda o código no WhatsApp e você vê a visita inteira
-- ─────────────────────────────────────────────────────────────
create or replace function tracking.jornada(p_codigo text)
returns jsonb
language sql
stable
security definer
set search_path = tracking, public
as $$
with ev as (
  select * from tracking.eventos
  where external_id = regexp_replace(coalesce(p_codigo, ''), '\D', '', 'g')
  order by criado_em
)
select case when not exists (select 1 from ev) then
  jsonb_build_object('encontrado', false, 'codigo', p_codigo)
else
  jsonb_build_object(
    'encontrado', true,
    'codigo', (select external_id from ev limit 1),
    'primeira_visita', (select min(criado_em) from ev),
    'ultima_visita', (select max(criado_em) from ev),
    'sessoes', (select count(distinct sessao_id) from ev),
    'converteu', (select bool_or(conversao) from ev),
    'origem', (select jsonb_build_object(
        'utm_source', (array_agg(utm_source order by criado_em) filter (where utm_source is not null))[1],
        'utm_medium', (array_agg(utm_medium order by criado_em) filter (where utm_medium is not null))[1],
        'utm_campaign', (array_agg(utm_campaign order by criado_em) filter (where utm_campaign is not null))[1],
        'utm_content', (array_agg(utm_content order by criado_em) filter (where utm_content is not null))[1],
        'referrer', (array_agg(referrer order by criado_em) filter (where referrer is not null))[1],
        'gclid', (array_agg(gclid order by criado_em) filter (where gclid is not null))[1],
        'fbclid', (array_agg(fbclid order by criado_em) filter (where fbclid is not null))[1]
      ) from ev),
    'local', (select jsonb_build_object('cidade', cidade, 'regiao', regiao_codigo, 'pais', pais,
                                        'dispositivo', dispositivo, 'navegador', navegador)
              from ev order by criado_em desc limit 1),
    'linha_do_tempo', (select jsonb_agg(jsonb_build_object(
        'quando', criado_em, 'evento', evento, 'pagina', caminho, 'conversao', conversao
      ) order by criado_em) from ev)
  )
end;
$$;

comment on function tracking.jornada(text) is 'Recebe o código que o lead mandou no WhatsApp (com ou sem colchetes) e devolve a jornada dele no site.';

-- ─────────────────────────────────────────────────────────────
-- Painel: o protocolo aparece junto de cada conversa iniciada
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
        'quando', quando, 'codigo', codigo, 'origem', origem, 'campanha', campanha, 'conteudo', conteudo,
        'cidade', cidade, 'pais', pais, 'dispositivo', dispositivo) order by quando desc), '[]'::jsonb) from (
      select criado_em as quando, coalesce(external_id, '') as codigo,
             coalesce(utm_source, origem, '(sem)') as origem,
             coalesce(utm_campaign, '(nenhuma)') as campanha, coalesce(utm_content, '') as conteudo,
             coalesce(cidade, '') as cidade, coalesce(pais, '') as pais, coalesce(dispositivo, '') as dispositivo
      from base where conversao order by criado_em desc limit 30) t)
);
$$;

-- Permissões dos objetos novos (o schema já tem default privileges, isto é reforço).
grant execute on function tracking.jornada(text) to service_role;
grant execute on function tracking.painel(int)  to service_role;
revoke all on function tracking.jornada(text) from anon, authenticated;

notify pgrst, 'reload schema';
