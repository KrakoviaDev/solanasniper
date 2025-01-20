import base58 
from solders.keypair import Keypair

def get_wallet_from_private_key_bs58(private_key_bs58: str) -> Keypair:
    private_key_bytes = base58.b58decode(private_key_bs58)
    wallet = Keypair.from_bytes(private_key_bytes)
    return wallet
 
