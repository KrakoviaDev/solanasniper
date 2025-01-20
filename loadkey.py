import json, os, sys  
import base58 
from solders.keypair import Keypair 

def load_keypair_from_file(filename): 
    curr = os.path.join(sys.path[0], 'data',  filename) 
    with open(curr, 'r') as file:  
        secret = json.load(file) 
        secret_key = bytes(secret)  
        # print(base58.b58encode(secrets_key))  
        return Keypair.from_bytes(secret_key) 
 