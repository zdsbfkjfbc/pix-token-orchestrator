import uvicorn
import uuid
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.database import engine, get_db
from src.infra.db.models import Base
from src.infra.repositories.wallet_repository import WalletRepository
from src.app.use_cases.process_deposit import ProcessDepositUseCase
from src.app.services.crypto_ledger import CryptoLedgerService

app = FastAPI(title="Pix Token Orchestrator")

class MockPixWebhook(BaseModel):
    user_id: str
    amount: float

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/wallets/")
async def create_wallet(db: AsyncSession = Depends(get_db)):
    repo = WalletRepository(db)
    fake_user_id = uuid.uuid4()
    new_wallet = await repo.create_wallet(fake_user_id)
    return {
        "message": "Carteira criada com sucesso!",
        "wallet_id": new_wallet.id,
        "user_id": new_wallet.user_id,
        "balance_brl": new_wallet.fiat_balance
    }

@app.post("/webhook/pix-simulation")
async def simulate_pix_deposit(
    webhook_data: MockPixWebhook, 
    db: AsyncSession = Depends(get_db)
):
    repo = WalletRepository(db)
    use_case = ProcessDepositUseCase(repo)
    try:
        result = await use_case.execute(webhook_data.user_id, webhook_data.amount)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA NOVA DE AUDITORIA ---
@app.get("/audit/{wallet_id}")
async def audit_wallet(wallet_id: str, db: AsyncSession = Depends(get_db)):
    repo = WalletRepository(db)
    try:
        # 1. Validação de UUID (Se o usuário mandar "batata", dá erro 400)
        try:
            real_uuid = uuid.UUID(wallet_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID da carteira inválido")

        # 2. VERIFICAÇÃO DE EXISTÊNCIA (A Correção!)
        wallet = await repo.get_wallet_by_id(real_uuid)
        if not wallet:
            raise HTTPException(status_code=404, detail="Carteira não encontrada. Verifique se você não usou o User ID por engano.")

        # 3. Agora sim, busca as transações
        txs = await repo.get_all_transactions(real_uuid)
        
        is_valid = CryptoLedgerService.validate_chain(txs)
        
        return {
            "wallet_id": wallet_id,
            "chain_valid": is_valid,
            "transaction_count": len(txs),
            "chain_data": [
                {"id": str(tx.id), "hash": tx.hash, "prev": tx.previous_hash} for tx in txs
            ]
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)