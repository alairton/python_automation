# Migração de Notificações para o Telegram

Substituição completa do canal de notificações do Microsoft Teams pelo Telegram nos scripts de automação.

## User Review Required

> [!IMPORTANT]
> Você precisará adicionar o `TELEGRAM_BOT_TOKEN` e o `TELEGRAM_CHAT_ID` no arquivo `.env` para que as notificações sejam entregues com sucesso.

## Proposed Changes

---

### Configuração

#### [MODIFY] [.env](file:///c:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production/.env)
#### [MODIFY] [.env.example](file:///c:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production/.env.example)
- Remoção de `TEAMS_WEBHOOK_URL`
- Inclusão de `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`

---

### Scripts

#### [DELETE] [testar_webhook.py](file:///c:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production/testar_webhook.py)
- Remoção do script antigo de teste do webhook do Teams.

#### [NEW] [testar_telegram.py](file:///c:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production/testar_telegram.py)
- Script de teste para validação de envio de mensagens formatadas via API do Telegram.

#### [MODIFY] [liga_production_valida_iris_list_v2.py](file:///c:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production/liga_production_valida_iris_list_v2.py)
- Substituição da lógica de envio e das validações iniciais do Teams pelo fluxo do Telegram.

## Verification Plan

### Automated Tests
* N/A

### Manual Verification
1. Configurar credenciais reais no `.env`.
2. Executar `python ligar_production/testar_telegram.py` e verificar o recebimento no Telegram.
3. Executar o script principal `liga_production_valida_iris_list_v2.py` e validar a mensagem de resumo final no Telegram.
