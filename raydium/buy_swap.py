from spl.token.instructions import close_account, CloseAccountParams
from spl.token.client import Token
from spl.token.core import _TokenCore
  
from solana.rpc.commitment import Commitment 
 
from solders.pubkey import Pubkey 
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price


from raydium.async_txn import execute_tx
from raydium.create_close_account import get_token_account,fetch_pool_keys, get_token_account, make_swap_instruction
from utils.birdeye import getSymbol
from utils.webhook import sendWebhook
from configparser import ConfigParser
from utils.new_pools_list import check


import os ,sys, asyncio, time

LAMPORTS_PER_SOL = 1000000000


def buy(solana_client, TOKEN_TO_SWAP_BUY, payer, amount):
    config = ConfigParser()
    config.read(os.path.join(sys.path[0], 'data', 'config.ini'))
    GAS_PRICE =  config.getint("INVESTMENT", "computeUnitPriceMicroLamports")
    GAS_LIMIT =  config.getint("INVESTMENT", "computeUnitLimitRaydium")
    EARLY_BUY =  config.getint("INVESTMENT", "WHEN_TO_BUY")
    token_symbol, SOl_Symbol = getSymbol(TOKEN_TO_SWAP_BUY)
    # pair_or_mint  = Pubkey.from_string(TOKEN_TO_SWAP_BUY)
    pool_keys = fetch_pool_keys(TOKEN_TO_SWAP_BUY)
    if pool_keys == "failed":
        sendWebhook(f"a|BUY Pool ERROR {token_symbol}",f"[Raydium]: Pool Key Not Found")
        return "failed"
    if str(pool_keys['base_mint']) != "So11111111111111111111111111111111111111112":
        mint = pool_keys['base_mint']
    else:
        mint = pool_keys['quote_mint']

        
    """
    Calculate amount
    """
    amount_in = int(amount * LAMPORTS_PER_SOL)
    # slippage = 0.1
    # lamports_amm = amount * LAMPORTS_PER_SOL
    # amount_in =  int(lamports_amm - (lamports_amm * (slippage/100)))

    txnBool = True
    while txnBool:
        try:
            """Get swap token program id"""
            print("1. Get TOKEN_PROGRAM_ID...")
            accountProgramId = solana_client.get_account_info_json_parsed(mint)
            TOKEN_PROGRAM_ID = accountProgramId.value.owner

            """
            Set Mint Token accounts addresses
            """
            print("2. Get Mint Token accounts addresses...")
            swap_associated_token_address,swap_token_account_Instructions  = get_token_account(solana_client, payer.pubkey(), mint)


            """
            Create Wrap Sol Instructions
            """
            print("3. Create Wrap Sol Instructions...")
            balance_needed = Token.get_min_balance_rent_for_exempt_for_account(solana_client)
            WSOL_token_account, swap_tx, payer, Wsol_account_keyPair, opts, = _TokenCore._create_wrapped_native_account_args(TOKEN_PROGRAM_ID, payer.pubkey(), payer,amount_in,
                                                                False, balance_needed, Commitment("confirmed"))
            """
            Create Swap Instructions
            """
            print("4. Create Swap Instructions...")
            instructions_swap = make_swap_instruction(  amount_in, 
                                                        WSOL_token_account,
                                                        swap_associated_token_address,
                                                        pool_keys, 
                                                        mint, 
                                                        solana_client,
                                                        payer
                                                    )


            print("5. Create Close Account Instructions...")
            params = CloseAccountParams(account=WSOL_token_account, dest=payer.pubkey(), owner=payer.pubkey(), program_id=TOKEN_PROGRAM_ID)
            closeAcc =(close_account(params))


            print("6. Add instructions to transaction...")

            swap_tx.add(set_compute_unit_limit(GAS_LIMIT)) # my default limit
            swap_tx.add(set_compute_unit_price(GAS_PRICE))

            if swap_token_account_Instructions != None:
                swap_tx.add(swap_token_account_Instructions)
            swap_tx.add(instructions_swap)
            swap_tx.add(closeAcc)

            if check(TOKEN_TO_SWAP_BUY):
                open_time = pool_keys['pool_open_time']
                sleep_total = open_time - time.time()
                if sleep_total > EARLY_BUY:
                    sleep_sleep = sleep_total - EARLY_BUY
                    sendWebhook(f"a|BUY Pool",f"[Raydium]:\nTime Remaining to pool open: {sleep_total} seconds.\nSleep Time: {sleep_sleep} seconds...")
                    print(f"Sleeping for {sleep_sleep}")
                    time.sleep(sleep_sleep)
                    print("sending Buy")
                else:
                    sendWebhook(f"a|BUY Pool ERROR {token_symbol}",f"[Raydium]: Pool is already open, no use buying...")
                    return "failed"

            loop1 = asyncio.new_event_loop()
            tx = loop1.run_until_complete(execute_tx(token_symbol,swap_tx, payer, Wsol_account_keyPair, None))
            loop1.close()
            return tx
        except:
            txnBool = False
            return "failed"
