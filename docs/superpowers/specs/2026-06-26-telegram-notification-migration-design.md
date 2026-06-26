# Especificação de Design: Migração de Notificações para o Telegram

Este documento detalha o design técnico para substituir as notificações do Microsoft Teams pelo Telegram no sistema de automação do IRIS.

## Objetivo
Como os conectores do Microsoft Teams herdados foram desativados definitivamente pela Microsoft (causando erros HTTP 403), decidimos migrar todo o canal de notificações de status da automação para o Telegram.

## Alterações de Configuração (`.env`)

A variável obsoleta `TEAMS_WEBHOOK_URL` será removida do arquivo `.env` e substituída pelas credenciais do Telegram:

- `TELEGRAM_BOT_TOKEN`: Token do bot criado via @BotFather.
- `TELEGRAM_CHAT_ID`: ID do chat/grupo do Telegram para onde as mensagens serão enviadas.

## Detalhes de Formatação e API

Usaremos a API HTTP do Telegram para enviar mensagens:
- **Endpoint**: `https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage`
- **Método**: `POST`
- **Payload (JSON)**:
  ```json
  {
    "chat_id": "<TELEGRAM_CHAT_ID>",
    "text": "<MENSAGEM>",
    "parse_mode": "HTML"
  }
  ```

### Formatação HTML
Para manter a compatibilidade com a formatação atual baseada em Markdown (`**negrito**`), a função de envio converterá a marcação usando expressões regulares:
- `**texto**` será convertido para `<b>texto</b>`.
- Emojis serão injetados dinamicamente no início da mensagem com base no `status`:
  - `Sucesso` -> `🟢`
  - Qualquer outro status (ex: `Atenção`, `Erro`) -> `🔴`

## Componentes Afetados

### 1. `testar_webhook.py` (Renomeado para `testar_telegram.py`)
- **Ação**: Deletar `testar_webhook.py` e criar `testar_telegram.py`.
- **Propósito**: Script isolado para testes rápidos de envio de mensagens no Telegram.

### 2. `liga_production_valida_iris_list_v2.py`
- **Ação**: Modificar.
- **Mudanças**:
  - Atualizar a validação inicial de variáveis de ambiente para checar `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` ao invés de `TEAMS_WEBHOOK_URL`.
  - Substituir a função `enviar_teams` por `enviar_telegram(msg, status)`.
  - Atualizar todas as chamadas de envio de notificação no script principal.

## Plano de Verificação

1. **Configuração**: Adicionar as credenciais válidas do Telegram no arquivo `.env`.
2. **Execução de Teste**: Executar o script `testar_telegram.py` e verificar a entrega da mensagem formatada no Telegram.
3. **Execução Completa**: Executar o script principal `liga_production_valida_iris_list_v2.py` para garantir que o fluxo de ponta a ponta envie a mensagem final com sucesso.
