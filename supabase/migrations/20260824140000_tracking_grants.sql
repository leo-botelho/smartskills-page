-- Permissões do schema tracking.
-- A migration anterior criou o schema sem conceder acesso a ninguém, e o PostgREST
-- (que se autentica como service_role) recebia 42501 "permission denied for schema tracking".
-- Ignorar RLS e ter permissão são coisas distintas: service_role precisa das duas.

-- Quem escreve e lê: apenas a service_role, usada só pelas Cloudflare Functions.
grant usage on schema tracking to service_role;
grant all privileges on all tables    in schema tracking to service_role;
grant all privileges on all sequences in schema tracking to service_role;
grant execute        on all functions in schema tracking to service_role;

-- Objetos criados no futuro herdam as mesmas permissões.
alter default privileges in schema tracking grant all     on tables    to service_role;
alter default privileges in schema tracking grant all     on sequences to service_role;
alter default privileges in schema tracking grant execute on functions to service_role;

-- Reforço: as chaves públicas (anon e authenticated) continuam sem qualquer acesso.
-- A chave anon vive no navegador em projetos Supabase; aqui ela não enxerga o schema.
revoke all on schema tracking from anon, authenticated;
revoke all on all tables    in schema tracking from anon, authenticated;
revoke all on all functions in schema tracking from anon, authenticated;
alter default privileges in schema tracking revoke all on tables    from anon, authenticated;
alter default privileges in schema tracking revoke all on functions from anon, authenticated;

-- Recarrega o cache de schema do PostgREST para valer na hora.
notify pgrst, 'reload schema';
