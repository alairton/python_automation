import os
import json
import subprocess
import time
import logging
import requests
import winsound
import paramiko
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- CONFIGURAÇÕES ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
USUARIO_WEB = os.getenv("USUARIO_WEB")
SENHA_WEB = os.getenv("SENHA_WEB")

SSH_USER = os.getenv("SSH_USER")
SSH_PASS = os.getenv("SSH_PASS")

if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, USUARIO_WEB, SENHA_WEB, SSH_USER, SSH_PASS]):
    raise ValueError("Erro crítico: As configurações e credenciais (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, USUARIO_WEB, SENHA_WEB, SSH_USER, SSH_PASS) devem estar configuradas no arquivo .env!")

PATH_OPENVPN_GUI = r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe"
NOME_CONFIG_OVPN = "downloaded-client-config.ovpn"

SISTEMAS_RAW = os.getenv("SISTEMAS_JSON")
if not SISTEMAS_RAW:
    raise ValueError(
        "Erro crítico: A lista de sistemas (SISTEMAS_JSON) não está configurada no arquivo .env!")

try:
    SISTEMAS = json.loads(SISTEMAS_RAW)
except Exception as e:
    raise ValueError(
        f"Erro crítico: A variável SISTEMAS_JSON no arquivo .env não é um JSON válido! Detalhes: {e}")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')


# --- FUNÇÕES ---

def emitir_alerta_sonoro():
    for _ in range(2):
        winsound.Beep(1200, 400)
        time.sleep(0.1)


def enviar_telegram(msg, status):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.warning(
            "TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não estão configuradas no arquivo .env.")
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
            logging.error(
                f"Erro ao enviar Telegram. Status: {response.status_code}, Resposta: {response.text}")
        else:
            logging.info(
                f"Notificação Telegram enviada com sucesso! Status: {response.status_code}")
    except Exception as e:
        logging.error(f"Erro ao enviar Telegram: {e}")


def validar_via_iris_list_ssh(ip):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=SSH_USER, password=SSH_PASS, timeout=5)
        stdin, stdout, stderr = client.exec_command("iris list")
        saida = stdout.read().decode("utf-8").lower()
        client.close()
        return ("running" in saida), saida.strip()
    except Exception as e:
        return False, f"Falha SSH: {str(e)}"


def processar_sistema(driver, sistema):
    wait = WebDriverWait(driver, 20)
    try:
        driver.get(sistema['url'])
        user_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name*='User']")))
        user_field.send_keys(USUARIO_WEB)
        pass_field = driver.find_element(
            By.CSS_SELECTOR, "input[type='password']")
        pass_field.send_keys(SENHA_WEB + Keys.ENTER)

        wait.until(EC.element_to_be_clickable((By.ID, "cat_HS"))).click()
        wait.until(EC.element_to_be_clickable(
            (By.ID, "command_cmdStart"))).click()

        # Pausa curta para você conseguir ver o pop-up antes do accept
        time.sleep(2)

        try:
            driver.switch_to.alert.accept()
        except:
            pass

        wait.until(EC.presence_of_element_located((By.ID, "command_cmdStop")))
        return True
    except Exception as e:
        logging.error(f"Erro no portal de {sistema['nome']}: {e}")
        return False


def main():
    logging.info("Iniciando comando OpenVPN GUI...")
    subprocess.Popen(
        f'"{PATH_OPENVPN_GUI}" --connect "{NOME_CONFIG_OVPN}"', shell=True)
    logging.info("Aguardando 10s para túnel estabilizar...")
    time.sleep(10)

    sistemas_online = []
    sucessos = []
    falhas = []

    logging.info("=== VALIDANDO CONECTIVIDADE E STATUS IRIS ===")
    for sis in SISTEMAS:
        is_up, info = validar_via_iris_list_ssh(sis['ip'])
        if is_up:
            logging.info(
                f"   [ONLINE] {sis['nome']} - Instância está RUNNING.")
            sistemas_online.append(sis)
        else:
            msg_erro = f"{sis['nome']} (Instância DOWN ou SSH falhou)"
            logging.error(f"   [OFFLINE] {msg_erro}")
            falhas.append(msg_erro)
            emitir_alerta_sonoro()

    if not sistemas_online:
        logging.critical("Nenhum sistema acessível via SSH. Abortando.")
        enviar_telegram(
            "Falha Crítica: Todos os sistemas via SSH estão offline.", "Erro")
        return

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        for i, sis in enumerate(sistemas_online):
            if i > 0:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])

            logging.info(f"Iniciando Produção no Portal: {sis['nome']}")
            if processar_sistema(driver, sis):
                sucessos.append(sis['nome'])
            else:
                falhas.append(
                    f"{sis['nome']} (Verificar falha de inicialização)")
                emitir_alerta_sonoro()

        # --- PAUSA PARA VERIFICAÇÃO MANUAL ---
        logging.info(
            "Aguardando 2 minutos para conferência manual dos pop-ups...")
        time.sleep(120)

    finally:
        driver.quit()
        status_final = "Sucesso" if not falhas else "Atenção"
        resumo = f"**Sistemas Online:** {', '.join(sucessos) if sucessos else 'Nenhum'}\n\n**Falhas/Offline:** {', '.join(falhas) if falhas else 'Nenhuma'}"
        enviar_telegram(resumo, status_final)
        logging.info("=== Processo Finalizado Production ONLINE ===")


if __name__ == "__main__":
    main()
