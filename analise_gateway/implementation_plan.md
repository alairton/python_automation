# Plano de Implementação: Refatoração de Segurança e Automação de Reboot no `analise_gateway`

Este plano detalha o refactoring do projeto `analise_gateway` para implementar boas práticas de segurança (armazenamento de dados sensíveis no `.env`), remover redundâncias no código de conexão SSH, adicionar a verificação automatizada de tempo de atividade (uptime) do servidor com reinicialização automática se estiver ativo há mais de 1 dia, configurar o ambiente virtual (`venv`) e preparar o repositório para o GitHub.

## User Review Required

> [!IMPORTANT]
> **Definição de "Servidor Ligado há mais de 1 dia":**
> Implementaremos a verificação baseada no tempo de atividade do **sistema operacional** do servidor (Uptime do OS) lido diretamente de `/proc/uptime` (que não requer permissão de administrador para leitura). 
> Se o tempo de atividade for superior a **86.400 segundos (24 horas)**, o script executará o comando de reinicialização.

> [!WARNING]
> **Comando de Restart:**
> O comando padrão de reinicialização de um servidor Linux é o `sudo reboot`. Para que a automação execute esse comando sem travar a execução por solicitação de senha, o usuário SSH `cspar.alairton` precisará ter permissões de execução do `reboot` sem senha no arquivo `sudoers` do servidor Linux (`NOPASSWD`).

## Open Questions

> [!NOTE]
> Se o objetivo for reiniciar o **serviço Apache (`httpd`)** e não a máquina física/virtual inteira, por favor nos avise. Por padrão, prosseguiremos com a reinicialização da máquina inteira (`sudo reboot`) conforme solicitado ("servidores ligados a mais de um dia").

---

## Proposed Changes

### 📁 Estrutura de Diretórios Proposta

O projeto dentro de [**`analise_gateway`**](file:///C:/Users/alair/OneDrive/Documentos/automacao/python/analise_gateway) ficará estruturado da seguinte forma:

```text
analise_gateway/
├── .env                  # Credenciais e IPs (Ignorado pelo Git)
├── .env.example          # Modelo de configuração pública
├── .gitignore            # Ignora .env e venv/
├── requirements.txt      # Dependências do Python
├── README.md             # Documentação do Projeto
└── analise_gateway_ssh.py # Script de automação principal
```

---

### [Component Name] analise_gateway

#### [NEW] [`.env`](file:///C:/Users/alair/OneDrive/Documentos/automacao/python/analise_gateway/.env)
Arquivo contendo de forma isolada e segura as credenciais e a lista de servidores em formato JSON.

#### [NEW] [`.env.example`](file:///C:/Users/alair/OneDrive/Documentos/automacao/python/analise_gateway/.env.example)
Modelo público para preenchimento de variáveis de ambiente.

#### [NEW] [`.gitignore`](file:///C:/Users/alair/OneDrive/Documentos/automacao/python/analise_gateway/.gitignore)
Regras para impedir o envio do `.env` e da pasta `venv/` ao GitHub.

#### [NEW] [`requirements.txt`](file:///C:/Users/alair/OneDrive/Documentos/automacao/python/analise_gateway/requirements.txt)
Dependências do projeto (`paramiko`, `python-dotenv`).

#### [NEW] [`README.md`](file:///C:/Users/alair/OneDrive/Documentos/automacao/python/analise_gateway/README.md)
Guia completo de instalação, segurança e execução do projeto.

#### [MODIFY] [`analise_gateway_ssh.py`](file:///C:/Users/alair/OneDrive/Documentos/automacao/python/analise_gateway/analise_gateway_ssh.py)
*   Remoção de credenciais expostas.
*   Importação do `dotenv` e `json`.
*   Refatoração da inicialização redundante do `paramiko.SSHClient()`.
*   Remoção do import não utilizado `requests`.
*   **Nova Funcionalidade**: Leitura de `/proc/uptime`. Se maior que 86400 segundos, loga a informação e dispara `sudo reboot`.

---

## Verification Plan

### Automated Tests
1.  **Criação do Venv e Instalação**:
    *   Criar o ambiente virtual na nova pasta e instalar as dependências.
2.  **Validação de Sintaxe e Importações**:
    *   Executar o script com interpretador do ambiente virtual no modo de importação rápida para certificar que o carregamento do JSON de servidores e do `.env` funcionam perfeitamente.

### Manual Verification
*   O operador executará o script e poderá acompanhar visualmente a conexão a cada gateway, as métricas do Apache e, caso o uptime supere 24 horas, a tentativa de reboot.
