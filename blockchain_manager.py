import json
import os
from dotenv import load_dotenv
from transformers import pipeline
from blockchain.genesis_block import create_genesis_block
from blockchain.block_structure import Block

class BlockchainJSONManager:
    def __init__(self, file_path="json_logs/blockchain.json"):
        self.file_path = file_path
        self.blockchain = self.load_blockchain()

        # Load Hugging Face API Key
        load_dotenv()
        huggingface_token = os.getenv("HUGGINGFACE_API_KEY")
        
        # Debugging: Print the API key to verify it's loaded
        print(f"Hugging Face API Key: {huggingface_token}")

        if not huggingface_token:
            raise ValueError("Hugging Face API Key is missing. Add it to the .env file.")

        # Initialize Hugging Face sentiment analysis pipeline
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis", 
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # Explicitly set to use CPU
        )

    def initialize_blockchain(self):
        """Initialize blockchain with genesis block."""
        if not os.path.exists(self.file_path):
            genesis_block = create_genesis_block()
            self.blockchain.append(genesis_block)
            self.save_blockchain()
        else:
            self.load_blockchain()

    def load_blockchain(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                # Validate the structure of the JSON data
                if not isinstance(data, list):
                    raise ValueError("Blockchain data should be a list of blocks.")
                for block in data:
                    if not all(key in block for key in ["block_id", "previous_hash", "timestamp", "transactions", "ai_validation_score", "metadata", "hash"]):
                        raise ValueError("Each block must contain all required fields.")
                return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return []

    def analyze_transaction(self, transaction):
        """Analyze transaction using Hugging Face sentiment analysis."""
        sentiment = self.sentiment_analyzer(transaction)
        return sentiment[0]['score']  # Use the sentiment score as a placeholder for AI validation

    def add_block(self, transactions, metadata=""):
        """Add a new block to the blockchain."""
        if not self.blockchain:
            self.initialize_blockchain()

        last_block = self.blockchain[-1]
        block_id = last_block["block_id"] + 1

        ai_scores = [self.analyze_transaction(tx) for tx in transactions]
        avg_score = sum(ai_scores) / len(ai_scores) if ai_scores else 1.0

        new_block = Block(
            block_id=block_id,
            previous_hash=last_block["hash"],
            transactions=transactions,
            ai_validation_score=avg_score,
            metadata=metadata
        )
        self.blockchain.append(new_block.to_dict())
        self.save_blockchain()

    def save_blockchain(self):
        """Save blockchain to JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(self.blockchain, f, indent=4)
        print(f"Blockchain saved to {self.file_path}.")

    def print_blockchain(self):
        """Print the current blockchain."""
        for block in self.blockchain:
            print(json.dumps(block, indent=4))

if __name__ == "__main__":
    # Initialize the Blockchain JSON Manager
    blockchain_manager = BlockchainJSONManager()

    # Initialize the blockchain or load existing one
    blockchain_manager.initialize_blockchain()

    # Add new blocks
    blockchain_manager.add_block(["Alice sends 5 tokens to Bob"], metadata="First transaction")
    blockchain_manager.add_block(["Bob sends 3 tokens to Charlie"], metadata="Second transaction")

    # Print the blockchain
    blockchain_manager.print_blockchain()