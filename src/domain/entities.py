from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

# 1. Enums para evitar erros de digitação (Magic Strings)
class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TransactionType(Enum):
    DEPOSIT_PIX = "DEPOSIT_PIX"
    MINT_TOKEN = "MINT_TOKEN"     # Compra de token
    GAME_CREDIT = "GAME_CREDIT"   # Envio pro jogo

# 2. Entidade Transaction
@dataclass
class Transaction:
    amount: Decimal
    type: TransactionType
    description: str
    wallet_id: UUID
    id: UUID = field(default_factory=uuid4)
    status: TransactionStatus = TransactionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    def complete(self):
        if self.status == TransactionStatus.PENDING:
            self.status = TransactionStatus.COMPLETED

    def fail(self):
        if self.status == TransactionStatus.PENDING:
            self.status = TransactionStatus.FAILED

# 3. Entidade Wallet
@dataclass
class Wallet:
    user_id: UUID
    # Decimal garante precisão financeira
    fiat_balance: Decimal = Decimal("0.00")  
    token_balance: int = 0  # Tokens geralmente são inteiros, mas podem ser Decimal
    
    def deposit_fiat(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("O valor deve ser positivo")
        self.fiat_balance += amount

    def withdraw_fiat(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("O valor deve ser positivo")
        if self.fiat_balance < amount:
            raise ValueError("Saldo insuficiente")
        self.fiat_balance -= amount

    def add_tokens(self, amount: int):
        if amount <= 0:
            raise ValueError("Quantidade de tokens deve ser positiva")
        self.token_balance += amount

# 4. Objeto de Valor Pix
@dataclass
class PixCharge:
    txid: str
    amount: Decimal
    qr_code: str
    qr_code_base64: str
    status: str = "ATIVO"