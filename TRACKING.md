# Tracking próprio — Smart Skills Hub

Coleta **server-side, first-party**, com armazenamento em **Supabase** e painel próprio.
Sem Google Tag Manager, sem Stape, sem pixel de terceiro no caminho do usuário.

## Como funciona

```
navegador                  Cloudflare (seu domínio)              Supabase
─────────                  ────────────────────────              ────────
assets/track.js            functions/api/collect.js              schema tracking
  evento + página   ──▶      + IP (CF-Connecting-IP)      ──▶      eventos
  UTMs + referrer            + user agent (navegador/SO)          views + função painel()
  (sendBeacon)               + geolocalização (request.cf)
                             + cookies first-party HttpOnly
                                      │
                                      └─▶ destinos opcionais (GA4, Meta CAPI, webhook n8n)

/dashboard.html  ◀──  functions/api/stats.js  ◀──  tracking.painel(dias)
   (Basic Auth)          (uma chamada só)
```

**Por que server-side importa aqui:** o `/api/collect` é do próprio domínio, então não é bloqueado como script de terceiro; o cookie é first-party e HttpOnly (nem o JS da página lê); e IP, user agent e geolocalização são preenchidos pelo servidor, não pelo navegador. A chave do Supabase nunca sai da função.

## Arquivos

| Arquivo | O que faz |
|---------|-----------|
| `supabase/migrations/20260823120000_tracking.sql` | Schema `tracking`: tabela `eventos`, views, função `painel()`, função de retenção, RLS |
| `functions/api/collect.js` | Endpoint de coleta (POST via sendBeacon, GET como pixel sem JS) |
| `functions/api/stats.js` | Devolve os dados do painel em uma chamada |
| `functions/_middleware.js` | Basic Auth em `/dashboard.html` e `/api/stats` |
| `functions/_lib/geo.js` | Geolocalização: `request.cf` → headers → API própria (opcional) |
| `functions/_lib/ua.js` | Navegador, SO, tipo de dispositivo e detecção de bot |
| `functions/_lib/supabase.js` | Escrita e RPC via PostgREST, sem SDK |
| `functions/_lib/destinos.js` | Encaminhamento opcional: GA4, Meta CAPI, webhook |
| `assets/track.js` | Cliente mínimo no navegador |
| `dashboard.html` | Painel |
| `_routes.json` | As funções só rodam em `/api/*` e `/dashboard*`; o resto é estático puro |

## Instalação

### 1. Supabase

```bash
supabase link --project-ref SEU_PROJECT_REF
supabase db push
```

Ou cole o conteúdo de `supabase/migrations/20260823120000_tracking.sql` no SQL Editor do painel do Supabase.

Depois, em **Project Settings → API → Data API**, exponha o schema `tracking` (campo "Exposed schemas"). Sem isso o PostgREST devolve 404 ao gravar.

### 2. Variáveis no Cloudflare Pages

Em **Workers & Pages → smartskills-site → Settings → Variables and Secrets**, cadastre como **Secret**:

| Variável | Valor |
|----------|-------|
| `SUPABASE_URL` | `https://xxxx.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | a chave `service_role` (nunca a `anon`) |
| `IP_SALT` | string longa e aleatória |
| `PAINEL_USUARIO` / `PAINEL_SENHA` | acesso ao painel |

Opcionais: `ARMAZENAR_IP_BRUTO`, `COOKIE_DOMINIO`, `GEO_API_URL`, `GEO_API_TOKEN`, `GA4_MEASUREMENT_ID`, `GA4_API_SECRET`, `META_PIXEL_ID`, `META_CAPI_TOKEN`, `WEBHOOK_URL`. Modelo completo em `.dev.vars.example`.

### 3. Deploy

```bash
npm install
npm run deploy
```

### 4. Local

```bash
cp .dev.vars.example .dev.vars   # preencha
npm run dev                      # http://localhost:8788
```

Atenção: `request.cf` não existe no `wrangler pages dev` nem no preview do dashboard da Cloudflare. Local, a geolocalização vem vazia (ou da `GEO_API_URL`, se configurada). Em produção funciona normalmente.

## O que é coletado

**Do navegador** (`assets/track.js`): nome do evento, URL, caminho, título, referrer, UTMs, `origem`, idioma, resolução de tela e viewport.

**Do servidor** (`functions/api/collect.js`): IP, user agent, navegador, SO, tipo de dispositivo, é-bot, país, região, cidade, CEP, latitude, longitude, fuso, continente, ASN, operadora, datacenter, e os cookies de visitante e sessão.

**Eventos automáticos**: `pageview`, `scroll_50`, `scroll_90`, `tempo_30s`, `whatsapp_click` (conversão), `email_click`, `clique_externo`.

**Evento manual**: `window.ssTrack('nome_do_evento', { qualquer: 'dado' })`, ou `data-track="nome"` em qualquer link ou botão.

## Geolocalização própria

A fonte padrão é o objeto `request.cf`, que a Cloudflare entrega junto do request: sem chamada externa, sem custo, sem terceiro vendo o IP do seu visitante. Se um dia quiser trocar por uma base própria (MaxMind, IP2Location ou uma API sua), basta configurar `GEO_API_URL` com `{ip}` no lugar do endereço — `functions/_lib/geo.js` já trata timeout de 800 ms e falha silenciosa, para tracking nunca atrasar a página.

## LGPD e privacidade

IP é dado pessoal na LGPD. O que está implementado:

- `ip_hash` (SHA-256 com sal) sempre gravado; o IP bruto é opcional via `ARMAZENAR_IP_BRUTO`.
- `tracking.limpar_antigos(30, 180)`: apaga o IP bruto depois de 30 dias e o evento inteiro depois de 180. Agende com `pg_cron` (SQL comentado no fim da migration).
- Cookies HttpOnly, SameSite=Lax, sem compartilhamento com terceiros.
- Nenhum dado sai do seu domínio, a não ser que você ligue GA4/Meta.

**Pendente do seu lado:** atualizar `privacidade.html` dizendo que o site coleta IP, user agent e localização aproximada para medir origem de visitas, por quanto tempo guarda e como pedir exclusão. Sem esse texto, a coleta fica sem base documentada. Posso escrever quando você quiser.

## Custos

| Item | Free | Quando passa disso |
|------|------|--------------------|
| Cloudflare Pages Functions | 100 mil requisições/dia | ~10 mil visitas/dia com 6 eventos cada |
| Supabase | 500 MB de banco | ~1 milhão de eventos (≈500 bytes cada) |

A retenção de 180 dias segura o crescimento. Se o volume subir muito, o caminho é agregar por dia e apagar o detalhe.

## Verificação depois do deploy

1. Abra o site em uma aba anônima e navegue por duas páginas.
2. No Supabase: `select evento, caminho, cidade, dispositivo, criado_em from tracking.eventos order by id desc limit 10;`
3. Clique em um botão de WhatsApp e confirme a linha com `conversao = true`.
4. Abra `/dashboard.html` e confira os números.

Se não aparecer nada: veja o log da função em Workers & Pages → Deployments → Functions, confirme que o schema `tracking` está exposto na Data API do Supabase e que a chave é a `service_role`.

## Testes

O que foi validado antes da entrega, com Postgres real (PGlite) e o handler rodando em Node:

- **Coleta (34 verificações)**: status 202, gravação no schema certo, chave só no servidor, geolocalização completa, IP bruto e hash, detecção de dispositivo/navegador/SO, bot, UTMs, cookies HttpOnly/Secure/SameSite, sessão mantida entre eventos, conversão marcada, bloqueio de origem externa, fallback GET em pixel.
- **Banco (26 verificações)**: migration aplica, RLS ativo sem policy pública, índices, `painel()` com totais/série/campanhas/geo, `vw_sessoes` com duração e página de entrada e saída, retenção apagando só o que passou do prazo.
- **Painel (12 verificações)**: Basic Auth cobrindo `/dashboard` e `/api/stats`, liberando o resto.
- **Render**: dashboard renderizado com 963 eventos sintéticos, sem erro de console.
