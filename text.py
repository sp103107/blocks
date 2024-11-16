import hashlib
import json

blockchain = [
    # Add your JSON data here
]

def calculate_hash(block_data):
    data = block_data.copy()
    data.pop('hash', None)
    block_string = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

# Validate blockchain
def validate_blockchain(blockchain):
    for i in range(len(blockchain)):
        block = blockchain[i]
        # Validate hash
        calculated_hash = calculate_hash(block)
        if block["hash"] != calculated_hash:
            print(f"Hash mismatch at block {block['block_id']}")
            return False
        # Validate previous hash
        if i > 0 and block["previous_hash"] != blockchain[i - 1]["hash"]:
            print(f"Previous hash mismatch at block {block['block_id']}")
            return False
        # Validate timestamp
        if i > 0 and block["timestamp"] < blockchain[i - 1]["timestamp"]:
            print(f"Timestamp error at block {block['block_id']}")
            return False
    print("Blockchain is valid!")
    return True

# Run validation
validate_blockchain(blockchain)