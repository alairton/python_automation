import os
import logging
import requests
from dotenv import load_dotenv

# Configura o logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

def enviar_teams(msg, status):
    if not TEAMS_WEBHOOK_URL:
        logging.warning("TEAMS_WEBHOOK_URL não está configurada no arquivo .env.")
        return

    is_modern_workflow = "logic.azure.com" in TEAMS_WEBHOOK_URL
    logging.info(f"Usando URL do Webhook: {TEAMS_WEBHOOK_URL}")
    logging.info(f"Tipo de webhook detectado: {'Moderno (Workflows/Power Automate)' if is_modern_workflow else 'Legado (Office 365 Connector)'}")

    if is_modern_workflow:
        # Formato moderno para Workflows do Teams (Power Automate) usando Adaptive Card
        payload = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "type": "AdaptiveCard",
                        "version": "1.2",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": f"**Automação IRIS: {status}** (Teste de Webhook)",
                                "weight": "Bolder",
                                "size": "Medium",
                                "color": "Good" if status == "Sucesso" else "Attention"
                            },
                            {
                                "type": "TextBlock",
                                "text": msg,
                                "wrap": True
                            }
                        ],
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
                    }
                }
            ]
        }
    else:
        # Formato legado (MessageCard)
        color = "00FF00" if status == "Sucesso" else "FF0000"
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color,
            "summary": "Status Produção IRIS - Teste",
            "sections": [{"activityTitle": f"Automação IRIS: {status} (Teste de Webhook)", "text": msg, "markdown": True}]
        }

    try:
        logging.info("Enviando requisição POST para o Teams...")
        response = requests.post(TEAMS_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code not in [200, 202]:
            logging.error(f"Erro ao enviar Teams. Status: {response.status_code}, Resposta: {response.text}")
        else:
            logging.info(f"Notificação Teams enviada com sucesso! Código HTTP: {response.status_code}, Resposta: {response.text}")
    except Exception as e:
        logging.error(f"Erro ao enviar Teams: {e}")

if __name__ == "__main__":
    test_msg = "**Sistemas Online:** HSHC STG, UCR STG\n\n**Falhas/Offline:** Nenhuma"
    enviar_teams(test_msg, "Sucesso")
