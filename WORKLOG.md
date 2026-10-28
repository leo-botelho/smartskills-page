# WORKLOG — smartskills-page

Entradas mais recentes no topo.

## 2026-10-28 — Páginas legais ajustadas para o FlowJob

Fonte: `D:\repo-local\wacrm\docs\ajustes-paginas-legais.md` (rascunho sem revisão jurídica). Motivo: a Meta avalia se a política cobre o que o app FlowJob (CRM em que empresas conectam o próprio WhatsApp Business) realmente faz.

- `privacidade.html`: FlowJob na intro e na seção "Quem somos"; nova seção 3 "Dados tratados no FlowJob" (papéis controlador/operador, dados tratados, conexão via Embedded Signup com token criptografado, revogação); Cloudflare e Supabase passam a citar o FlowJob; retenção do FlowJob na seção 8. Seções seguintes renumeradas (3→4 … 11→12) e a referência cruzada "item 3" virou "item 4".
- `termos.html`: FlowJob na intro e na descrição do serviço; nova seção 4 "Uso do FlowJob pelo cliente" (responsabilidades do cliente, dependência da Meta, suspensão). Seções seguintes renumeradas (4→5 … 10→11).
- `exclusao-dados.html`: blocos "Se você usa o FlowJob (cliente)" (remoção pela Meta, Redefinir Configuração, e-mail de exclusão) e "Se você é contato de um cliente do FlowJob", com a ressalva de que a exclusão de conversas de contatos pode passar antes pelo cliente (controlador). Heading antigo virou "Se você conversou com o agente de IA".
- "Última atualização" das três páginas: 28 de outubro de 2026.

Pendências:
- Revisão jurídica dos blocos novos (papéis controlador/operador e limitação de responsabilidade).
- Cadastrar no app da Meta as URLs de política, termos, exclusão e desautorização (lista no md de origem). O callback `https://crm.smartskillshub.com.br/exclusao-de-dados?code=...` e os endpoints `/api/meta/data-deletion` e `/api/meta/deauthorize` pertencem ao wacrm e precisam existir no ar.
- Publicar (commit/deploy) — as alterações ainda não foram commitadas.
