from uuid import UUID
from decimal import Decimal
from src.infra.repositories.wallet_repository import WalletRepository

class ProcessDepositUseCase:
    def __init__(self, repo: WalletRepository):
        self.repo = repo

    async def execute(self, user_id: str, amount: float):
        # 1. Converter tipos (Segurança)
        # O banco manda string/float, nós convertemos para UUID e Decimal
        try:
            uid_obj = UUID(str(user_id))
            amount_decimal = Decimal(str(amount))
        except ValueError:
            raise ValueError("ID de usuário ou valor inválidos.")

        # 2. Busca a carteira
        wallet = await self.repo.get_wallet_by_user_id(uid_obj)
        if not wallet:
            raise ValueError("Carteira não encontrada para este usuário.")

        # 3. Executa a lógica de crédito (aquela função segura que criamos no repo)
        success = await self.repo.credit_tokens_safely(wallet.id, amount_decimal)
        
        if not success:
            raise Exception("Erro ao processar o depósito no banco de dados.")

        return {
            "user_id": user_id,
            "new_balance_fiat": wallet.fiat_balance, # O SQLAlchemy atualiza o objeto automaticamente
            "new_balance_token": wallet.token_balance,
            "status": "COMPLETED"
        }