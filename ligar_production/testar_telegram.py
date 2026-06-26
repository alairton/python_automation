import os
import logging
import requests
import re
from dotenv import load_dotenv

# Configura o logging básico
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_telegram(msg, status):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.warning(
            "TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não estão configurados no arquivo .env.")
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
            logging.error(
                f"Erro ao enviar Telegram. Status: {response.status_code}, Resposta: {response.text}")
        else:
            logging.info(
                f"Notificação Telegram enviada com sucesso! Código HTTP: {response.status_code}")
    except Exception as e:
        logging.error(f"Erro ao enviar Telegram: {e}")


if __name__ == "__main__":
    test_msg = "**Sistemas Online:** HSHC STG, UCR STG\n\n**Falhas/Offline:** Nenhuma"
    enviar_telegram(test_msg, "Sucesso")
