import hashlib
import time

class Block:
    def __init__(self, block_id, previous_hash, transactions, ai_validation_score, metadata):
        self.block_id = block_id
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.ai_validation_score = ai_validation_score
        self.metadata = metadata
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.block_id}{self.previous_hash}{self.timestamp}{self.transactions}{self.ai_validation_score}{self.metadata}"
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self):
        return {
            "block_id": self.block_id,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "ai_validation_score": self.ai_validation_score,
            "metadata": self.metadata,
            "hash": self.hash,
        }