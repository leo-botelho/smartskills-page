# smartskills-site — site novo da Smart Skills Hub (2026-08-22)

Site estático (HTML + CSS + JS) com cena 3D em Three.js (ESM via CDN, importmap). Pronto para Cloudflare Pages, sem build.

## Estrutura
- `build.py` — gera as páginas a partir de um layout comum (nav, rodapé, SEO, schema.org). Edite o conteúdo aqui e rode `python build.py`.
- `assets/site.css` — tokens e componentes (derivados do brandbook, `marketing-smartskills/output/2026-08-21-cmo-brandbook-smartskills.md`).
- `assets/scene.js` — cena 3D do símbolo. Modos: `hero` (home, sobre), `layers` (plataformas), `graph` (automações), `particles` (cases). Fallback: SVG estático quando não há WebGL; respeita `prefers-reduced-motion`; pausa fora da viewport.
- `assets/site.js` — menu mobile, reveal, chat simulado, filtros de cases, página intermediária de WhatsApp (mensagem por `?origem=` + evento `whatsapp_click` para GA4/Meta/dataLayer).
- Páginas: `index`, `plataformas`, `agentes-de-ia`, `automacoes`, `cases`, `sobre`, `whatsapp` (fora do menu), `404`, + legais copiadas do site atual.

## Rodar local
```
python -m http.server 8787
```
(ou `.claude/launch.json` → preview). Precisa de servidor HTTP por causa dos módulos ES.

## Deploy (Cloudflare Pages)
Publicar a pasta inteira. Adicionar `_redirects` se quiser URLs sem `.html` (Pages já serve `/plataformas` → `plataformas.html`). A LP antiga vivia em `/`; a nova home substitui e o conteúdo dela está em `/agentes-de-ia`.

## Tracking próprio

Coleta server-side com Supabase e painel em `/dashboard.html`. Ver **TRACKING.md** (instalação, variáveis, LGPD, custos e testes).

## Pendências antes de publicar
- Tracking próprio: aplicar a migration no Supabase e cadastrar os secrets (TRACKING.md). GA4/Meta Pixel são opcionais: o `collect` já encaminha server-side se as variáveis existirem.
- Atualizar `privacidade.html` com a coleta de IP, user agent e localização aproximada.
- Confirmar com a dona: cidade/abrangência (página Sobre), stack pública nos badges, FAQs comerciais.
- Pinar a versão do Three.js localmente (`assets/vendor/three.module.js`) se quiser zero dependência de CDN.
