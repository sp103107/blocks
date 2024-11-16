from blockchain.block_structure import Block

def create_genesis_block():
    return Block(
        block_id=0,
        previous_hash="0" * 64,
        transactions=[],
        ai_validation_score=0.0,
        metadata="Genesis Block"
    ).to_dict()