import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, DateTime, func, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

# Importamos os Enums do domínio
from src.domain.entities import TransactionStatus, TransactionType

class Base(AsyncAttrs, DeclarativeBase):
    pass

class WalletModel(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, unique=True, index=True)
    
    fiat_balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    token_balance: Mapped[int] = mapped_column(Numeric(18, 0), default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now(), server_default=func.now())

    transactions: Mapped[list["TransactionModel"]] = relationship(back_populates="wallet")

class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    wallet_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("wallets.id"))
    
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default=TransactionStatus.PENDING.value)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # --- BLOCKCHAIN FIELDS ---
    hash: Mapped[str] = mapped_column(String, nullable=True)
    previous_hash: Mapped[str] = mapped_column(String, nullable=True)
    # -------------------------

    wallet: Mapped["WalletModel"] = relationship(back_populates="transactions")

class PixChargeModel(Base):
    __tablename__ = "pix_charges"

    txid: Mapped[str] = mapped_column(String, primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    qr_code: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="ATIVO")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())