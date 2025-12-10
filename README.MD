# 🪙 Pix Token Orchestrator

Um sistema backend financeiro robusto desenvolvido em Python, focado em alta performance, segurança e auditabilidade. O projeto orquestra recebimentos via Pix e converte valores fiduciários (BRL) em tokens digitais (Lastro 1:1), utilizando uma **Blockchain Interna (Ledger Criptográfico)** para garantir a imutabilidade das transações.

## 🚀 Tecnologias e Arquitetura

Este projeto segue rigorosamente os princípios de **Clean Architecture** para garantir desacoplamento e testabilidade.

-   **Linguagem:** Python 3.11+
-   **Framework Web:** FastAPI (Async)
-   **Banco de Dados:** SQLite (via `aiosqlite` para suporte assíncrono) / SQLAlchemy 2.0
-   **Segurança:** SHA-256 Hash Chaining (Blockchain Privada)
-   **Design Patterns:** Repository Pattern, Use Cases, Factory, Dependency Injection.

## 🏛️ Estrutura do Projeto (Clean Architecture)

O código foi organizado para separar regras de negócio de detalhes de infraestrutura:

```text
src/
├── domain/           # Regras de Negócio Puras (Entidades & Enums)
│   └── entities.py   # Definição de Wallet, Transaction e regras de validação
├── app/              # Casos de Uso (Ações do Sistema)
│   ├── use_cases/    # Lógica de aplicação (ex: Processar Depósito)
│   └── services/     # Serviços de domínio (ex: CryptoLedgerService)
├── infra/            # Camada externa (Banco, APIs, Frameworks)
│   ├── db/           # Configuração do Banco de Dados e Models ORM
│   └── repositories/ # Implementação do acesso a dados (SQLAlchemy)
└── main.py           # Entrypoint da API e Configuração de Rotas
```

🔒 Destaque: Ledger Criptográfico (Blockchain Interna)
Diferente de sistemas comuns que apenas salvam o saldo, este projeto implementa um Ledger Auditável. Cada transação salva no banco contém um hash criptográfico que depende da transação anterior.

Como funciona:

Gênesis: A primeira transação recebe hash anterior zerado.

Encadeamento: Hash Atual = SHA256(Dados da Transação + Hash da Transação Anterior).

Auditoria: O sistema possui um endpoint /audit/{wallet_id} que recalcula toda a corrente em tempo real. Se um dado for alterado manualmente no banco, a matemática não bate e a API alerta FRAUDE.

⚙️ Como Rodar Localmente
Pré-requisitos
Python 3.11 ou superior

Git

Instalação
Clone o repositório:

Bash

git clone [https://github.com/SEU-USUARIO/pix-token-orchestrator.git](https://github.com/SEU-USUARIO/pix-token-orchestrator.git)
cd pix-token-orchestrator
Crie e ative o ambiente virtual:

Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Instale as dependências:

Bash

pip install fastapi uvicorn sqlalchemy pydantic alembic python-dotenv aiosqlite
Rode a aplicação:

Bash

python -m uvicorn src.main:app --reload
Acesse a documentação interativa (Swagger):

Abra seu navegador em: http://127.0.0.1:8000/docs

🧪 Testando a API
Criar Carteira: Use POST /wallets/ para criar um usuário. Copie o user_id e o wallet_id.

Simular Pix: Use POST /webhook/pix-simulation com o user_id para depositar valores.

Auditar: Use GET /audit/{wallet_id} para verificar a integridade da blockchain daquela carteira.

🤝 Colaboração e Desenvolvimento
Este projeto foi desenvolvido utilizando a metodologia de AI-Pair Programming. A arquitetura, regras de negócio e refatoração de código foram construídas em colaboração entre:

[Seu Nome]: Engenharia de Software, Decisões de Arquitetura e Implementação.

Gemini (Google AI): Consultoria Técnica, Code Review e Sugestões de Clean Code.

Projeto desenvolvido para fins de estudo em Engenharia de Software Backend Sênior.
