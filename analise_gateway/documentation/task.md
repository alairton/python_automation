# Checklist de Execução: Refatoração do `analise_gateway` [CONCLUÍDO]

- `[x]` Criar arquivo de credenciais `.env` com a lista de servidores em formato JSON
- `[x]` Criar modelo genérico `.env.example`
- `[x]` Criar `.gitignore` para omitir chaves e o ambiente virtual
- `[x]` Criar arquivo de dependências `requirements.txt`
- `[x]` Refatorar `analise_gateway_ssh.py`
  - `[x]` Adicionar suporte para carregar `.env` e realizar parse do JSON de servidores
  - `[x]` Limpar conexões SSH redundantes e importações desnecessárias
  - `[x]` Adicionar lógica de verificação de uptime (/proc/uptime > 86400s)
  - `[x]` Adicionar comando para reiniciar o Apache (`sudo systemctl restart httpd`)
- `[x]` Configurar ambiente virtual local (`venv`) e instalar dependências
- `[x]` Validar importação e funcionamento básico do script refatorado
- `[x]` Criar documentação profissional `README.md`
