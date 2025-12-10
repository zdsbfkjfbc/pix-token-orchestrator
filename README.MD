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