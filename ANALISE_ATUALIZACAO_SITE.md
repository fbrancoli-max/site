# Guia prático: atualizar este site com Codex (sem mudar estrutura)

Perfeito — se você já está satisfeito com o site, a estratégia ideal é:

- **manter a estrutura atual**;
- usar o Codex só para **atualizações de conteúdo**;
- aplicar mudanças pequenas e seguras em cada rodada.

## O que manter como está

- Arquitetura atual do site (HTML estático + arquivos existentes).
- Organização de páginas em inglês (`/index.html`) e português (`/pt/index.html`).
- Estilo visual e navegação atuais.

## O que o Codex pode fazer para você no dia a dia

Use o Codex para tarefas como:

1. adicionar novo paper/publicação;
2. atualizar bio curta/longa;
3. incluir nova participação em mídia;
4. atualizar links (Google Scholar, ORCID, entrevistas etc.);
5. corrigir ortografia, datas e padronização de texto;
6. espelhar uma atualização do inglês para português (ou vice-versa).

## Modelo de pedido (prompt) que funciona bem

Copie e adapte:

```text
Quero atualizar meu site sem mudar estrutura/layout.

Tarefa:
- Adicionar [ITEM NOVO] na seção [SEÇÃO], em [index.html ou pt/index.html].
- Manter o mesmo estilo dos itens já existentes.
- Não refatorar HTML/CSS/JS.
- No final, me mostre exatamente o que foi alterado.
```

## Fluxo recomendado para cada atualização

1. Você descreve a alteração de conteúdo.
2. Codex altera **somente** os trechos necessários no HTML.
3. Codex mostra diff claro e curto.
4. Você valida texto/data/link.
5. Commit com mensagem objetiva (ex.: `content: add new publication (Apr 2026)`).

## Regras para evitar mudanças estruturais sem querer

Sempre incluir no pedido:

- “**Sem alterar estrutura/layout**”.
- “**Sem criar novos arquivos, salvo se eu pedir**”.
- “**Sem refatoração**”.
- “**Preservar classes/IDs existentes**”.

## Checklist rápido antes de publicar

- Data correta?
- Link abre corretamente?
- Atualização feita no idioma certo (EN/PT)?
- Texto consistente com o restante da página?
- Nada além do conteúdo foi alterado?

---

Se você quiser, no próximo passo eu já posso fazer sua **primeira atualização real de conteúdo** aqui no repo (ex.: novo paper, nova entrevista ou nova seção de agenda), mantendo 100% da estrutura atual.
