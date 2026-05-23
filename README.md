# 🚀 Suíte de Automação Python (Python Automation Suite)

Bem-vindo ao repositório **Python Automation Suite**! Este é um ecossistema consolidado de scripts e ferramentas de automação industrializados para gerenciamento de servidores, monitoramento de desempenho e integração contínua de serviços de infraestrutura.

Todos os projetos contidos nesta suíte foram desenvolvidos seguindo padrões rigorosos de engenharia de software, garantindo segurança absoluta, isolamento de dados sensíveis e eficiência operacional.

---

## 📂 Estrutura dos Projetos

A suíte está dividida em módulos independentes e altamente focados:

```text
python_automation/
├── ligar_production/      # 📡 Automação e Validação do IRIS Production
└── analise_gateway/       # 🖥️ Monitor SSH & Reinicialização Inteligente do Apache
```

### 1. 📡 [ligar_production](file:///C:/Users/alair/OneDrive/Documentos/automacao/python/ligar_production) (Automação IRIS)
Este script gerencia e valida a saúde do ambiente **IRIS**. Ele automatiza a inicialização de túneis seguros via OpenVPN, realiza login e navegação simulada em portais web via Selenium Webdriver para conferir o status de produção e dispara notificações detalhadas via Webhook do Microsoft Teams caso anomalias sejam detectadas.
*   **Destaques**: Conexão OpenVPN automatizada, extração de status com Selenium em Headless Mode e alertas dinâmicos no Teams.

### 2. 🖥️ [analise_gateway](file:///C:/Users/alair/OneDrive/Documentos/automacao/python/analise_gateway) (Monitor SSH do Apache)
Um analisador de desempenho em tempo real focado no servidor web Apache (`httpd`). O script conecta-se remotamente via SSH seguro (Paramiko) aos gateways de teste e staging, extrai métricas críticas de hardware (CPU e Memória RAM) e, caso o uptime do sistema operacional seja superior a 24 horas, realiza o reinício preventivo e automático do serviço HTTPD para mitigar vazamentos de memória.
*   **Destaques**: Parse inteligente de comandos `systemctl`, verificação passiva de uptime via `/proc/uptime` e reinício preventivo controlado do Apache.

---

## 🔒 Pilares de Segurança e Arquitetura

Para garantir a viabilidade deste repositório público e a segurança dos dados da infraestrutura:

1.  **Arquitetura Zero-Secrets**: Nenhuma credencial (usuário, senha, IP, URL ou Token de Webhook) é salva no código. Todas são lidas dinamicamente em tempo de execução de arquivos locais `.env` individuais em cada pasta.
2.  **Modelos Seguros (`.env.example`)**: Cada projeto inclui um template limpo demonstrando as variáveis necessárias para facilitar novas implantações de forma transparente.
3.  **Isolamento de Escopo (`.gitignore`)**: Filtros globais impedem que chaves criptográficas, segredos de produção e dependências locais de compilação sejam publicados acidentalmente.
4.  **Ambientes Limpos (`venv`)**: Uso obrigatório de ambientes virtuais do Python com o manifesto de dependências em arquivos `requirements.txt` dedicados por pasta.

---

## 🚀 Como Começar

### Pré-requisitos
Certifique-se de possuir o **Python 3.8+** instalado em seu sistema de desenvolvimento.

### Passos para Execução de Qualquer Projeto:

1.  **Clone o repositório em sua máquina local**:
    ```bash
    git clone https://github.com/alairton/python_automation.git
    cd python_automation
    ```

2.  **Acesse o projeto desejado**:
    *   Para o IRIS: `cd ligar_production`
    *   Para o Monitor SSH: `cd analise_gateway`

3.  **Crie e Ative seu Ambiente Virtual**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\python.exe -m pip install -r requirements.txt
    ```

4.  **Configure as Chaves e Variáveis**:
    Copie o arquivo `.env.example` para `.env` e preencha-o com as credenciais válidas da sua rede:
    ```bash
    cp .env.example .env
    ```

5.  **Rode a Automação**:
    *   Para o IRIS: `.\venv\Scripts\python.exe liga_production_valida_iris_list_v2.py`
    *   Para o Monitor: `.\venv\Scripts\python.exe analise_gateway_ssh.py`

---

## 📝 Licença e Propósito

Este projeto foi construído sob demanda para otimizar fluxos de engenharia, reduzir a intervenção manual em diagnósticos de rotina e elevar a segurança das chaves operacionais.
