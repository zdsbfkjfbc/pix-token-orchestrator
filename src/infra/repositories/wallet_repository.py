from uuid import UUID
from decimal import Decimal
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models import WalletModel, TransactionModel
from src.domain.entities import TransactionType, TransactionStatus
from src.app.services.crypto_ledger import CryptoLedgerService 

class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_wallet_by_user_id(self, user_id: UUID) -> WalletModel | None:
        stmt = select(WalletModel).where(WalletModel.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_wallet(self, user_id: UUID) -> WalletModel:
        wallet = WalletModel(user_id=user_id, fiat_balance=Decimal("0.00"), token_balance=0)
        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet

    async def credit_tokens_safely(self, wallet_id: UUID, amount: Decimal) -> bool:
        """
        Processa um PIX e registra na Blockchain interna.
        """
        # 1. Busca Carteira
        stmt = select(WalletModel).where(WalletModel.id == wallet_id)
        result = await self.session.execute(stmt)
        wallet = result.scalars().first()

        if not wallet:
            print(f"Carteira {wallet_id} não encontrada.")
            return False

        # 2. Busca a ÚLTIMA transação dessa carteira (para pegar o Hash anterior)
        stmt_last_tx = (
            select(TransactionModel)
            .where(TransactionModel.wallet_id == wallet_id)
            .order_by(desc(TransactionModel.created_at)) # Pega a mais recente
            .limit(1)
        )
        result_tx = await self.session.execute(stmt_last_tx)
        last_tx = result_tx.scalars().first()

        # Se for a primeira transação, hash anterior é zeros (Gênesis Block)
        previous_hash = last_tx.hash if last_tx else "0" * 64

        # 3. Atualiza Token
        wallet.token_balance += int(amount)

        # 4. Prepara dados para Hash
        tx_data = {
            "amount": amount,
            "type": TransactionType.DEPOSIT_PIX.value,
            "wallet_id": str(wallet_id)
        }
        
        # 5. Gera Hash atual
        current_hash = CryptoLedgerService.generate_hash(tx_data, previous_hash)

        # 6. Salva Transação
        transaction = TransactionModel(
            wallet_id=wallet.id,
            amount=amount,
            type=TransactionType.DEPOSIT_PIX.value,
            status=TransactionStatus.COMPLETED.value,
            description=f"Depósito Pix recebido: R$ {amount}",
            
            # Campos Blockchain
            previous_hash=previous_hash,
            hash=current_hash
        )
        
        self.session.add(transaction)
        
        try:
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"❌ ERRO NO BANCO DE DADOS: {str(e)}")
            return False
            
    # --- NOVO: Método para Auditar ---
    async def get_all_transactions(self, wallet_id: UUID):
        # Pega todas as transações na ordem correta (da mais antiga pra mais nova)
        stmt = (
            select(TransactionModel)
            .where(TransactionModel.wallet_id == wallet_id)
            .order_by(TransactionModel.created_at)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_wallet_by_id(self, wallet_id: UUID) -> WalletModel | None:
        stmt = select(WalletModel).where(WalletModel.id == wallet_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()