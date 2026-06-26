# Telegram Notification Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the IRIS automation notification channel from Microsoft Teams to Telegram by updating configurations and replacement of notification helper functions.

**Architecture:** Update configurations in environment files and replace the Teams Webhook request payload with Telegram Bot API `sendMessage` requests using HTML parse mode and regular expression translation for bold markdown.

**Tech Stack:** Python 3, `requests` library, `re` (built-in regex).

## Global Constraints

- Must remove all code references to Teams webhook logic.
- Must support formatting conversion from `**bold**` to `<b>bold</b>`.
- Must load configuration from `ligar_production/.env`.

---

### Task 1: Environment Configuration

**Files:**
- Modify: `ligar_production/.env:1-3`
- Modify: `ligar_production/.env.example:1-3`

**Interfaces:**
- Produces: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` environment variables.

- [ ] **Step 1: Update `.env.example`**
  Modify [ligar_production/.env.example](file:///c:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production/.env.example) to replace Teams config with Telegram config.
  ```env
  # Configurações do Telegram
  TELEGRAM_BOT_TOKEN=seu_bot_token_aqui
  TELEGRAM_CHAT_ID=seu_chat_id_aqui
  ```

- [ ] **Step 2: Update `.env`**
  Modify [ligar_production/.env](file:///c:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production/.env) to replace `TEAMS_WEBHOOK_URL` with `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
  *(Keep the user's existing values if they already entered them, otherwise use placeholders for them to fill)*
  ```env
  # Configurações do Telegram
  TELEGRAM_BOT_TOKEN=seu_bot_token_aqui
  TELEGRAM_CHAT_ID=seu_chat_id_aqui
  ```

- [ ] **Step 3: Commit changes**
  ```bash
  git add ligar_production/.env.example
  git commit -m "config: replace Teams webhook config with Telegram bot config templates"
  ```

---

### Task 2: Create Test Script `testar_telegram.py`

**Files:**
- Create: `ligar_production/testar_telegram.py`
- Delete: `ligar_production/testar_webhook.py`

**Interfaces:**
- Produces: Command line script `python ligar_production/testar_telegram.py`.

- [ ] **Step 1: Create `testar_telegram.py`**
  Write [testar_telegram.py](file:///c:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production/testar_telegram.py):
  ```python
  import os
  import logging
  import requests
  import re
  from dotenv import load_dotenv

  # Configura o logging básico
  logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

  # Carrega as variáveis de ambiente do arquivo .env
  load_dotenv()
  TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
  TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

  def enviar_telegram(msg, status):
      if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
          logging.warning("TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não estão configurados no arquivo .env.")
          return

      # Converte **negrito** em <b>negrito</b> para HTML do Telegram
      msg_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', msg)
      
      emoji = "🟢" if status == "Sucesso" else "🔴"
      texto_final = f"{emoji} <b>Automação IRIS: {status}</b>\n\n{msg_html}"

      url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
      payload = {
          "chat_id": TELEGRAM_CHAT_ID,
          "text": texto_final,
          "parse_mode": "HTML"
      }

      try:
          logging.info("Enviando notificação para o Telegram...")
          response = requests.post(url, json=payload, timeout=10)
          if response.status_code != 200:
              logging.error(f"Erro ao enviar Telegram. Status: {response.status_code}, Resposta: {response.text}")
          else:
              logging.info(f"Notificação Telegram enviada com sucesso! Código HTTP: {response.status_code}")
      except Exception as e:
          logging.error(f"Erro ao enviar Telegram: {e}")

  if __name__ == "__main__":
      test_msg = "**Sistemas Online:** HSHC STG, UCR STG\n\n**Falhas/Offline:** Nenhuma"
      enviar_telegram(test_msg, "Sucesso")
  ```

- [ ] **Step 2: Delete `testar_webhook.py`**
  Remove [testar_webhook.py](file:///c:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production/testar_webhook.py).

- [ ] **Step 3: Run the new test script**
  Run: `python ligar_production/testar_telegram.py`
  Expected: If credentials are not set, prints warning `TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não estão configurados`. If credentials are set, prints `Notificação Telegram enviada com sucesso!`.

- [ ] **Step 4: Commit changes**
  ```bash
  git rm ligar_production/testar_webhook.py
  git add ligar_production/testar_telegram.py
  git commit -m "feat: implement testar_telegram.py and remove legacy testar_webhook.py"
  ```

---

### Task 3: Update Main Automation Script `liga_production_valida_iris_list_v2.py`

**Files:**
- Modify: `ligar_production/liga_production_valida_iris_list_v2.py`

**Interfaces:**
- Consumes: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` environment variables.

- [ ] **Step 1: Modify Environment loading and validation**
  Replace Teams webhook config variables loading with Telegram credentials.
  ```python
  TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
  TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
  # ... and replace validation lines around 29-30:
  if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, USUARIO_WEB, SENHA_WEB, SSH_USER, SSH_PASS]):
      raise ValueError("Erro crítico: As configurações e credenciais (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, USUARIO_WEB, SENHA_WEB, SSH_USER, SSH_PASS) devem estar configuradas no arquivo .env!")
  ```

- [ ] **Step 2: Replace `enviar_teams` with `enviar_telegram`**
  Replace the function `enviar_teams` implementation with `enviar_telegram(msg, status)`:
  ```python
  def enviar_telegram(msg, status):
      if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
          logging.warning("TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não estão configuradas no arquivo .env.")
          return

      # Converte **negrito** em <b>negrito</b> para HTML do Telegram
      msg_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', msg)
      
      emoji = "🟢" if status == "Sucesso" else "🔴"
      texto_final = f"{emoji} <b>Automação IRIS: {status}</b>\n\n{msg_html}"

      url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
      payload = {
          "chat_id": TELEGRAM_CHAT_ID,
          "text": texto_final,
          "parse_mode": "HTML"
      }

      try:
          response = requests.post(url, json=payload, timeout=10)
          if response.status_code != 200:
              logging.error(f"Erro ao enviar Telegram. Status: {response.status_code}, Resposta: {response.text}")
          else:
              logging.info(f"Notificação Telegram enviada com sucesso! Status: {response.status_code}")
      except Exception as e:
          logging.error(f"Erro ao enviar Telegram: {e}")
  ```

- [ ] **Step 3: Update callers**
  Replace all `enviar_teams(...)` calls with `enviar_telegram(...)`.
  - Around line 176: `enviar_telegram("Falha Crítica: Todos os sistemas via SSH estão offline.", "Erro")`
  - Around line 202: `enviar_telegram(resumo, status_final)`

- [ ] **Step 4: Commit changes**
  ```bash
  git add ligar_production/liga_production_valida_iris_list_v2.py
  git commit -m "feat: migrate main script notification to Telegram"
  ```
