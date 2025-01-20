
import time,os,sys 
from solana.rpc.async_api import AsyncClient 
from solana.rpc.commitment import Commitment 

from solana.rpc.api import RPCException 
from configparser import ConfigParser  
from utils.webhook import sendWebhook
 
config = ConfigParser()
# using sys and os because sometimes this shitty config reader does not read from curr directory
config.read(os.path.join(sys.path[0], 'data', 'config.ini'))


# RPC settings - register at RPC and get your mainnet url.
RPC_HTTPS_URL = config.get("RPC_URL", "rpc_url")



async def execute_tx(token_symbol,swap_tx, payer, Wsol_account_keyPair, signers):
        
    solana_client = AsyncClient(RPC_HTTPS_URL, commitment=Commitment("confirmed"), timeout=30,blockhash_cache=True)
        
    try:
        start_time = time.time()

        txnBool = True
        while txnBool:
            try:
                print("7. Execute Transaction...")
                start_time = time.time()
                if Wsol_account_keyPair != None:
                    txn = await solana_client.send_transaction(swap_tx, payer, Wsol_account_keyPair)
                else:
                    txn = await solana_client.send_transaction(swap_tx, *signers)

                txid_string_sig = txn.value

                print("8. Confirm transaction...")
                checkTxn = True
                while checkTxn:
                    try:
                        status = await solana_client.get_transaction(txid_string_sig,"json")
                        # FeesUsed = (status.value.transaction.meta.fee) / 1000000000
                        if status.value.transaction.meta.err == None:
                            # print(f"[TXN] Transaction Fees: {FeesUsed:.10f} SOL")

                            execution_time = time.time() - start_time
                            print("[TXN] Transaction Success",txn.value)
                            print(f"Execution time: {execution_time} seconds")

                            txnBool = False
                            checkTxn = False
                            sendWebhook(f"e|TXN Success",f"[Raydium] TXN Execution time: {execution_time}")
                            return txid_string_sig
                        
                        else:
                            print("Transaction Failed")
                            execution_time = time.time() - start_time
                            print(f"Execution time: {execution_time} seconds")
                            checkTxn = False

                    except Exception as e:
                        # sendWebhook(f"e|TXN ERROR {token_symbol}",f"[Raydium]: {e}")
                        # print(f"Sleeping... {e}\nRetrying...")
                        pass

            except RPCException as e:
                print(f"Error: [{e.args[0].message}]...\nRetrying...")
                sendWebhook(f"e|TXN ERROR {token_symbol}",f"[Raydium]: {e.args[0].data.logs}")

            except Exception as e:
                sendWebhook(f"e|TXN Exception ERROR {token_symbol}",f"[Raydium]: {e.args[0].message}")
                print(f"Error: [{e}]...\nEnd...")
                txnBool = False
                return "failed"
    except:
        print("Main Swap error Raydium... retrying...")

