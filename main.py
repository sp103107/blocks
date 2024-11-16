from blockchain.genesis_block import create_genesis_block
from blockchain.block_structure import Block
from ai_validator.validator import AIValidator
import json

class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]
        self.validator = AIValidator()

    def add_block(self, transactions, metadata=""):
        previous_block = self.chain[-1]
        block_id = previous_block["block_id"] + 1

        # Validate transactions using AI validator
        is_valid, score = self.validator.validate_transactions(transactions)
        if not is_valid:
            raise ValueError("Transactions failed ethical validation.")

        new_block = Block(
            block_id=block_id,
            previous_hash=previous_block["hash"],
            transactions=transactions,
            ai_validation_score=score,
            metadata=metadata
        )
        self.chain.append(new_block.to_dict())
        return new_block

    def save_chain(self, file_path="json_logs/blockchain.json"):
        with open(file_path, "w") as f:
            json.dump(self.chain, f, indent=4)

    def load_chain(self, file_path="json_logs/blockchain.json"):
        try:
            with open(file_path, "r") as f:
                self.chain = json.load(f)
        except FileNotFoundError:
            print("Blockchain file not found, starting a new chain.")
            self.chain = [create_genesis_block()]

if __name__ == "__main__":
    blockchain = Blockchain()
    print("Blockchain initialized.")

    # Example: Add a block
    transactions = ["Alice pays Bob 10 tokens", "Charlie pays Dave 15 tokens"]
    try:
        new_block = blockchain.add_block(transactions, metadata="Sample Block")
        print("New Block Added:")
        print(json.dumps(new_block.to_dict(), indent=4))
    except ValueError as e:
        print(f"Block addition failed: {e}")

    blockchain.save_chain()