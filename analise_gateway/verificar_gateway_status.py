import os
import json
import sys
import paramiko
from dotenv import load_dotenv

# Garante que a saída do terminal use UTF-8 (evita UnicodeEncodeError no Windows)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- CONFIGURAÇÕES DE ACESSO ---
SSH_USER = os.getenv("SSH_USER")
SSH_PASS = os.getenv("SSH_PASS")

if not all([SSH_USER, SSH_PASS]):
    raise ValueError("Erro crítico: As credenciais SSH_USER e SSH_PASS devem estar configuradas no arquivo .env!")

# --- CARREGAMENTO DOS SERVIDORES ---
SERVERS_RAW = os.getenv("SERVERS_JSON")
if not SERVERS_RAW:
    raise ValueError("Erro crítico: A lista de servidores (SERVERS_JSON) não está configurada no arquivo .env!")

try:
    SERVERS = json.loads(SERVERS_RAW)
except Exception as e:
    raise ValueError(f"Erro crítico: A variável SERVERS_JSON no arquivo .env não é um JSON válido! Detalhes: {e}")


def check_gateway_status(ip, name):
    print(f"\n--- {name} ({ip}) ---")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conexão SSH
        client.connect(ip, username=SSH_USER, password=SSH_PASS, timeout=5)

        # 1. Obtenção do Uptime do Sistema
        stdin, stdout, stderr = client.exec_command("cat /proc/uptime")
        uptime_out = stdout.read().decode().strip()
        
        if uptime_out:
            uptime_sec = float(uptime_out.split()[0])
            uptime_dias = uptime_sec / 86400
            print(f"⏱️ Uptime do Sistema: {uptime_dias:.2f} dias")

        # 2. Comando focado nas linhas de performance do Apache
        cmd = "systemctl status httpd | grep -E 'Active:|Status:|Memory:|CPU:'"
        stdin, stdout, stderr = client.exec_command(cmd)

        output = stdout.read().decode().strip()

        if not output:
            print("⚠️ Erro: Não foi possível obter o status do httpd (serviço pode estar offline).")
        else:
            # Formatando a saída para leitura limpa
            lines = output.split('\n')
            for line in lines:
                clean_line = line.strip()
                if "Active:" in clean_line:
                    print(f"✅ {clean_line}")
                elif "Status:" in clean_line:
                    print(f"📊 {clean_line}")
                elif "Memory:" in clean_line:
                    print(f"🧠 {clean_line}")
                elif "CPU:" in clean_line:
                    print(f"⚡ {clean_line}")

    except Exception as e:
        print(f"❌ Falha de conexão: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    for server in SERVERS:
        check_gateway_status(server["ip"], server["name"])
