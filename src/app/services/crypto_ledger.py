import hashlib
import json
from decimal import Decimal
from typing import Any

class CryptoLedgerService:
    
    @staticmethod
    def generate_hash(data: dict, previous_hash: str) -> str:
        """
        Gera um hash SHA-256 único baseado nos dados atuais + hash anterior.
        Isso cria o vínculo "corrente" (Chain).
        """
        # 1. Prepara os dados de forma determinística (ordena chaves para o JSON ser sempre igual)
        # Convertemos Decimals para string para evitar erros de serialização
        data_clean = {k: str(v) if isinstance(v, Decimal) else v for k, v in data.items()}
        
        data_string = json.dumps(data_clean, sort_keys=True)
        
        # 2. O Segredo da Blockchain: Payload = Dados Atuais + Hash Anterior
        payload = f"{data_string}{previous_hash}"
        
        # 3. Gera o Hash
        return hashlib.sha256(payload.encode()).hexdigest()

    @staticmethod
    def validate_chain(transactions: list) -> bool:
        """
        Audita uma lista de transações para ver se alguém adulterou o banco.
        Retorna True se estiver íntegro, False se houver fraude.
        """
        for i in range(1, len(transactions)):
            current_tx = transactions[i]
            previous_tx = transactions[i-1]
            
            # Recalcula o hash com os dados que estão no banco
            data_to_hash = {
                "amount": current_tx.amount,
                "type": current_tx.type,
                "wallet_id": str(current_tx.wallet_id)
            }
            
            recalculated_hash = CryptoLedgerService.generate_hash(
                data_to_hash, 
                previous_hash=previous_tx.hash
            )
            
            # Se o hash recalculado não bater com o gravado, houve fraude!
            if recalculated_hash != current_tx.hash:
                print(f"FRAUDE DETECTADA na Tx {current_tx.id}")
                return False
                
        return True