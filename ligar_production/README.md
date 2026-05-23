# Automação de Produções IRIS (Ligar Production)

Este projeto automatiza o fluxo de conexão VPN, validação de status de banco de dados e inicialização de produções (*integrations*) do **InterSystems IRIS** em múltiplos ambientes de Staging (STG) e Desenvolvimento (DEV), notificando a equipe em tempo real no **Microsoft Teams**.

A arquitetura do script foi projetada seguindo as melhores práticas de **Segurança da Informação**, mantendo todo o código genérico e isolando credenciais, URLs privadas e infraestrutura de servidores em arquivos de configuração locais (`.env`), que são automaticamente ignorados pelo Git para evitar vazamentos acidentais no GitHub.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

*   **Python 3.x**: Linguagem de programação principal.
*   **Selenium & Webdriver Manager**: Automação de interface web para login e acionamento dos portais de gerenciamento IRIS.
*   **Paramiko**: Conexões SSH seguras para verificar instâncias de banco de dados na linha de comando (`iris list`).
*   **Python-Dotenv**: Carregamento dinâmico de credenciais e infraestrutura a partir de arquivos `.env`.
*   **Requests**: Envio de notificações de status ao Microsoft Teams via Webhook.
*   **Subprocess & Winsound**: Integração nativa com Windows para inicializar a OpenVPN GUI e emitir alertas sonoros físicos na máquina do operador em caso de falha.

---

## 🔒 Segurança de Credenciais e Arquitetura do Projeto

O projeto adota uma arquitetura **Zero-Hardcoded-Secrets**:
1.  **`.env`**: Armazena localmente suas credenciais de acesso Web, acesso SSH, webhook do Teams e a lista estruturada de servidores. **Nunca deve ser enviado para o GitHub**.
2.  **`.env.example`**: Um modelo limpo e genérico que serve de guia para configurar novos ambientes.
3.  **`.gitignore`**: Configurado para ignorar o arquivo `.env` e a pasta do ambiente virtual `venv/`, impedindo que esses arquivos sejam rastreados pelo Git.

---

## 🚀 Pré-requisitos

1.  **Python 3.8+** instalado na máquina.
2.  **Google Chrome** instalado.
3.  **OpenVPN GUI** instalado no diretório padrão: `C:\Program Files\OpenVPN\bin\openvpn-gui.exe`.
4.  O perfil de conexão VPN (`downloaded-client-config.ovpn`) presente no diretório padrão do OpenVPN ou na mesma pasta de execução.

---

## 📦 Instalação e Configuração

### 1. Clonar o projeto e acessar a pasta
```bash
git clone <url-do-seu-repositorio>
cd ligar_production
```

### 2. Configurar as credenciais e infraestrutura
Copie o arquivo `.env.example` para criar o seu arquivo local `.env`:
```bash
cp .env.example .env
```
Abra o arquivo `.env` recém-criado e preencha as variáveis de ambiente com os dados de acesso corretos.

> 💡 **Nota sobre a lista de sistemas**: A variável `SISTEMAS_JSON` no `.env` aceita um formato JSON simples de linha única contendo o nome, URL do portal e IP SSH de cada servidor. Exemplo:
> ```env
> SISTEMAS_JSON='[{"nome": "HSHC STG", "url": "http://172.21.0.68/hshcstg/csp/sys/UtilHome.csp", "ip": "172.21.0.68"}]'
> ```

### 3. Criar e configurar o Ambiente Virtual (`venv`)
Crie um ambiente virtual para isolar as dependências:
```powershell
python -m venv venv
```

Instale os pacotes necessários:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 🏃 Como Executar

Para iniciar a automação completa, execute o script utilizando o interpretador do seu ambiente virtual:

```powershell
.\venv\Scripts\python.exe liga_production_valida_iris_list_v2.py
```

### O que o script fará ao ser iniciado?
1.  **Conexão VPN**: Abre o OpenVPN GUI de forma silenciosa e aguarda 10 segundos para a estabilização do túnel de rede.
2.  **Validação SSH (`iris list`)**: Conecta-se remotamente a cada servidor definido no `.env` e roda o comando `iris list` para checar se a instância está `"running"`. Se houver falha de conexão ou se a instância estiver inativa, gera um alerta sonoro e adiciona à lista de falhas.
3.  **Login e Start na Production (Selenium)**: Abre uma sessão automatizada no Chrome. Para cada servidor ativo, efetua login no portal do IRIS, navega até o namespace de integração e clica em **Start**.
4.  **Conferência Manual**: Deixa o navegador aberto por **2 minutos** para que o operador possa analisar visualmente a tela e verificar possíveis logs ou pop-ups.
5.  **Finalização e Notificação**: Encerra a sessão do navegador e envia um relatório detalhado com os sucessos e falhas diretamente para o canal configurado no **Microsoft Teams**.

---

## 📄 Licença

Este projeto é de uso interno e confidencial. Certifique-se de manter o arquivo `.env` fora de qualquer commit ou compartilhamento público.
