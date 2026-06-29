# Analisador de Performance do Apache (Access Gateway SSH)

Este projeto realiza o diagnóstico rápido de integridade e desempenho do servidor web Apache (`httpd`) em servidores de Access Gateway (Staging e Testing) via conexão SSH segura.

O script monitora as principais métricas de performance do serviço e, **caso o sistema operacional do servidor esteja ligado há mais de 1 dia (24 horas)**, executa automaticamente a reinicialização segura apenas do serviço Apache (`httpd`) para liberar recursos e garantir estabilidade.

---

## ✨ Recursos Principais

*   **Métricas em Tempo Real**: Coleta de uso de CPU, Memória RAM, Ativação (`Active`) e Detalhes de status (`Status`) do Apache.
*   **Boas Práticas de Segurança**: Todas as credenciais, usuários e IPs dos servidores estão externos em arquivo de ambiente `.env` protegido.
*   **Automação de Reinicialização**: Leitura automatizada e sem privilégios de `/proc/uptime`. Se o uptime for superior a 24 horas, o script reinicia o Apache remotamente (`sudo systemctl restart httpd`).
*   **Formatação Visual Clara**: Saída estruturada no terminal com emojis para facilitar a leitura rápida pelo operador.

---

## 🛠️ Requisitos

1.  **Python 3.8+** instalado.
2.  Acesso SSH liberado nos servidores de Gateway de Destino.
3.  **Permissão no sudoers**: O usuário SSH configurado precisa ter a permissão de executar o comando `systemctl restart httpd` com privilégios administrativos via `sudo` sem a solicitação de senha (`NOPASSWD` no arquivo `/etc/sudoers` do Linux).

---

## 📦 Instalação e Configuração

### 1. Clonar ou copiar o projeto para a máquina
Acesse a pasta `analise_gateway`:
```bash
cd analise_gateway
```

### 2. Configurar as credenciais do ambiente
Copie o arquivo `.env.example` para gerar seu `.env` local:
```bash
cp .env.example .env
```
Abra o arquivo `.env` e defina seu usuário SSH, senha SSH e a lista de servidores em formato JSON na variável `SERVERS_JSON`.

> 💡 **Exemplo de lista de servidores**:
> ```env
> SERVERS_JSON='[{"ip": "10.0.0.1", "name": "Access Gateway apache"}]'
> ```

### 3. Configurar o Ambiente Virtual (`venv`)
Crie e ative o ambiente virtual para instalar as dependências necessárias de forma isolada:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 🏃 Como Executar

O projeto conta com dois scripts principais que utilizam o interpretador do ambiente virtual:

### 1. Apenas Visualizar Status (Leitura)
Para verificar o Uptime do Sistema e as métricas do Apache (`Active`, `Status`, `Memory`, `CPU`) sem reiniciar nada:
```powershell
.\venv\Scripts\python.exe verificar_gateway_status.py
```

### 2. Verificar Status e Reiniciar Apache (Automação)
Para monitorar a saúde e reiniciar automaticamente o Apache (`httpd`) caso o servidor esteja online há mais de 1 dia:
```powershell
.\venv\Scripts\python.exe analise_gateway_ssh.py
```

### Saída Esperada no Terminal:
```text
--- Access Gateway apache 01 (10.0.0.1) ---
⏱️ Uptime do Sistema: 2.14 dias
🔄 Servidor online há mais de 1 dia. Reiniciando o Apache (httpd)...
✅ Apache (httpd) reiniciado com sucesso!
✅ Active: active (running) since Sat 2026-05-23 19:28:44 -03; 2s ago
📊 Status: "Total requests: 12053; Current requests/sec: 0.2; Current KB/sec: 1.4"
🧠 Memory: 42.1M
⚡ CPU: 1.2s
```

---

## 🔒 Segurança do Repositório

Este repositório está configurado com um arquivo `.gitignore` que impede que seu arquivo de credenciais locais `.env` ou a pasta `venv/` sejam enviados ao GitHub por acidente, protegendo a segurança da sua infraestrutura.
