from spl.token.instructions import close_account, CloseAccountParams

from solana.rpc.types import TokenAccountOpts
from solana.rpc.api import RPCException
from solana.transaction import Transaction

from solders.pubkey import Pubkey
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price

from raydium.create_close_account import  fetch_pool_keys, sell_get_token_account,get_token_account, make_swap_instruction
from utils.birdeye import getSymbol
from utils.webhook import sendWebhook
from raydium.async_txn import execute_tx

from configparser import ConfigParser

import time, os ,sys, asyncio


LAMPORTS_PER_SOL = 1000000000

        # ctx ,     TOKEN_TO_SWAP_SELL,  keypair
def sell(solana_client, TOKEN_TO_SWAP_SELL, payer):



    config = ConfigParser()
    config.read(os.path.join(sys.path[0], 'data', 'config.ini'))
    GAS_PRICE =  config.getint("INVESTMENT", "computeUnitPriceMicroLamports")
    GAS_LIMIT =  config.getint("INVESTMENT", "computeUnitLimitRaydium")


    token_symbol, _ = getSymbol(TOKEN_TO_SWAP_SELL)


    mint1 = Pubkey.from_string(TOKEN_TO_SWAP_SELL)
    sol = Pubkey.from_string("So11111111111111111111111111111111111111112")

    """Get swap token program id"""
    print("1. Get TOKEN_PROGRAM_ID...")

    """Get Pool Keys"""
    print("2. Get Pool Keys...")
    pool_keys = fetch_pool_keys(str(mint1))
    if pool_keys == "failed":
        sendWebhook(f"a|Sell Pool ERROR {token_symbol}",f"[Raydium]: Pool Key Not Found")
        return "failed"

    if str(pool_keys['base_mint']) != "So11111111111111111111111111111111111111112":
        mint = pool_keys['base_mint']
    else:
        mint = pool_keys['quote_mint']

    TOKEN_PROGRAM_ID = solana_client.get_account_info_json_parsed(mint).value.owner

    txnBool = True
    while txnBool:
        """Get Token Balance from wallet"""
        print("3. Get oken Balance from wallet...")

        balanceBool = True
        while balanceBool:
            tokenPk = mint

            accountProgramId = solana_client.get_account_info_json_parsed(tokenPk)
            programid_of_token = accountProgramId.value.owner

            accounts = solana_client.get_token_accounts_by_owner_json_parsed(payer.pubkey(),TokenAccountOpts(program_id=programid_of_token)).value
            for account in accounts:
                mint_in_acc = account.account.data.parsed['info']['mint']
                if mint_in_acc == str(mint):
                    amount_in = int(account.account.data.parsed['info']['tokenAmount']['amount'])
                    print("3.1 Token Balance [Lamports]: ",amount_in)
                    break
            if int(amount_in) > 0:
                balanceBool = False
            else:
                print("No Balance, Retrying...")
                time.sleep(2)

        """Get token accounts"""
        print("4. Get token accounts for swap...")
        swap_token_account = sell_get_token_account(solana_client, payer.pubkey(), mint)
        WSOL_token_account, WSOL_token_account_Instructions = get_token_account(solana_client,payer.pubkey(), sol)
        
        if swap_token_account == None:
            print("swap_token_account not found...")
            return "failed"

        else:
            """Make swap instructions"""
            print("5. Create Swap Instructions...")
            instructions_swap = make_swap_instruction(  amount_in, 
                                                        swap_token_account,
                                                        WSOL_token_account,
                                                        pool_keys, 
                                                        mint, 
                                                        solana_client,
                                                        payer
                                                    )

            """Close wsol account"""
            print("6.  Create Instructions to Close WSOL account...")
            params = CloseAccountParams(account=WSOL_token_account, dest=payer.pubkey(), owner=payer.pubkey(), program_id=TOKEN_PROGRAM_ID)
            closeAcc =(close_account(params))

            """Create transaction and add instructions"""
            print("7. Create transaction and add instructions to Close WSOL account...")
            swap_tx = Transaction(fee_payer=payer.pubkey())
            signers = [payer]

            swap_tx.add(set_compute_unit_limit(GAS_LIMIT)) #my default limit
            swap_tx.add(set_compute_unit_price(GAS_PRICE))

            if WSOL_token_account_Instructions != None:
                swap_tx.add(WSOL_token_account_Instructions)
            swap_tx.add(instructions_swap)
            swap_tx.add(closeAcc)



            loop1 = asyncio.new_event_loop()
            txn = loop1.run_until_complete(execute_tx(token_symbol,swap_tx, payer, None, signers))
            loop1.close()
            txnBool = False
            return txn