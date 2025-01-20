from solana.rpc.api import Client
from solders.pubkey import Pubkey

def check_sol_balance(public_key_str: str) -> float:
    solana_client = Client("https://api.mainnet-beta.solana.com")  
    public_key = Pubkey.from_string(public_key_str)
    balance_response = solana_client.get_balance(public_key)  
     
    # Adjusted line to use the correct attribute access method
    sol_balance = balance_response.value / 1e9
    
    return sol_balance
 