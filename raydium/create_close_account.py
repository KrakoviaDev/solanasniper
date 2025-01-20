from spl.token.instructions import create_associated_token_account, get_associated_token_address 

from solders.pubkey import Pubkey
from solders.instruction import Instruction
   
from solana.rpc.types import TokenAccountOpts  
from solana.transaction import AccountMeta 

from solana.rpc.api import Client
from solana.rpc.commitment import Commitment

from utils.storing_pools import storePool_info, getPool_info 

from raydium.layouts import SWAP_LAYOUT, POOL_INFO_LAYOUT

from utils.constants import RAY_V4, SERUM_PROGRAM_ID

import json,requests, time, os,sys, asyncio
from configparser import ConfigParser
from utils.new_pools_list import check
config = ConfigParser()
# using sys and os because sometimes this shitty config reader does not read from curr directory
config.read(os.path.join(sys.path[0], 'data', 'config.ini'))

# Infura settings - register at infura and get your mainnet url.
RPC_HTTPS_URL = config.get("RPC_URL", "rpc_url")
AUTH = config.get("kokiez_api", "pool_fetcher_auth")

ctx1 = Client(RPC_HTTPS_URL, commitment=Commitment("confirmed"), timeout=30,blockhash_cache=True)



def make_simulate_pool_info_instruction(accounts, mint, ctx):
        keys = [
            AccountMeta(pubkey=accounts["amm_id"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["authority"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["base_vault"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["quote_vault"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["lp_mint"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["market_id"], is_signer=False, is_writable=False),    
            AccountMeta(pubkey=accounts['event_queue'], is_signer=False, is_writable=False),    
        ]
        data = POOL_INFO_LAYOUT.build(
            dict(
                instruction=12,
                simulate_type=0
            )
        )
        return Instruction(RAY_V4, data, keys)




def make_swap_instruction(amount_in: int, token_account_in: Pubkey.from_string, token_account_out: Pubkey.from_string,
                              accounts: dict, mint, ctx, owner) -> Instruction:
        
        
        tokenPk = mint
        accountProgramId = ctx.get_account_info_json_parsed(tokenPk)
        TOKEN_PROGRAM_ID = accountProgramId.value.owner
        
        keys = [
            AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["amm_id"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["authority"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["target_orders"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["base_vault"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["quote_vault"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=SERUM_PROGRAM_ID, is_signer=False, is_writable=False), 
            AccountMeta(pubkey=accounts["market_id"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["bids"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["asks"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["market_base_vault"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["market_quote_vault"], is_signer=False, is_writable=True),
            AccountMeta(pubkey=accounts["market_authority"], is_signer=False, is_writable=False),
            AccountMeta(pubkey=token_account_in, is_signer=False, is_writable=True),  #UserSourceTokenAccount 
            AccountMeta(pubkey=token_account_out, is_signer=False, is_writable=True), #UserDestTokenAccount 
            AccountMeta(pubkey=owner.pubkey(), is_signer=True, is_writable=False) #UserOwner 
        ]

        data = SWAP_LAYOUT.build(
            dict(
                instruction=9,
                amount_in=int(amount_in),
                min_amount_out=0
            )
        )
        return Instruction(RAY_V4, data, keys)

def get_token_account(ctx, 
                      owner: Pubkey.from_string, 
                      mint: Pubkey.from_string):
    try:
        account_data = ctx.get_token_accounts_by_owner(owner, TokenAccountOpts(mint))
        return account_data.value[0].pubkey, None
    except:
        swap_associated_token_address = get_associated_token_address(owner, mint)
        swap_token_account_Instructions = create_associated_token_account(owner, owner, mint)
        return swap_associated_token_address, swap_token_account_Instructions

def sell_get_token_account(ctx, 
                      owner: Pubkey.from_string, 
                      mint: Pubkey.from_string):
    try:
        account_data = ctx.get_token_accounts_by_owner(owner, TokenAccountOpts(mint))
        return account_data.value[0].pubkey
    except:
        print("Mint Token Not found")
        return None


def extract_pool_info(pools_list, mint):
    for pool in pools_list:
        if pool['baseMint'] == mint and pool['quoteMint'] == 'So11111111111111111111111111111111111111112':
            return pool
        elif pool['quoteMint'] == mint and pool['baseMint'] == 'So11111111111111111111111111111111111111112':
            return pool
    raise Exception(f'{mint} pool not found!')


def fetch_pool_keys(mint: str):
    # newPOOL = check(mint)
    """Get pool from already bought json"""
    amm_info = getPool_info(mint)
    print('-----111111---amm_info ',amm_info)
    if amm_info != None:
        return {
                    'amm_id': Pubkey.from_string(amm_info['amm_id']),
                    'authority': Pubkey.from_string(amm_info['authority']),
                    'base_mint': Pubkey.from_string(amm_info['base_mint']),
                    'base_decimals': amm_info['base_decimals'],
                    'quote_mint': Pubkey.from_string(amm_info['quote_mint']),
                    'quote_decimals': amm_info['quote_decimals'],
                    'lp_mint': Pubkey.from_string(amm_info['lp_mint']),
                    'open_orders': Pubkey.from_string(amm_info['open_orders']),
                    'target_orders': Pubkey.from_string(amm_info['target_orders']),
                    'base_vault': Pubkey.from_string(amm_info['base_vault']),
                    'quote_vault': Pubkey.from_string(amm_info['quote_vault']),
                    'market_id': Pubkey.from_string(amm_info['market_id']),
                    'market_base_vault': Pubkey.from_string(amm_info['market_base_vault']),
                    'market_quote_vault': Pubkey.from_string(amm_info['market_quote_vault']),
                    'market_authority': Pubkey.from_string(amm_info['market_authority']),
                    'bids': Pubkey.from_string(amm_info['bids']),
                    'asks': Pubkey.from_string(amm_info['asks']),
                    'event_queue': Pubkey.from_string(amm_info['event_queue']),
                    'pool_open_time' : amm_info['pool_open_time']
            } 
    try:
        # if newPOOL == False:
        #     pair_address = None
        #     res = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{mint}").json()['pairs']
        #     for pair in res:
        #         if pair['baseToken']['address'] == mint and pair['quoteToken']['address'] == 'So11111111111111111111111111111111111111112' and pair['dexId'] ==  'raydium':
        #             pair_address = Pubkey.from_string(pair['pairAddress'])
        #             break
        # else:
        #     pair_address = mint
        a = time.time()
        resp = requests.get('https://api.raydium.io/v2/sdk/liquidity/mainnet.json', stream=True)
        pools = resp.json()
        official = pools['official']
        unofficial = pools['unOfficial']
        all_pools = official + unofficial           
        amm_info = extract_pool_info(all_pools, mint)
        print('---amm_info--- : ', amm_info)
        if amm_info != None and "error" not in str(amm_info) and "Too Many Requests" not in str(amm_info):
            print("Total time taken to get pool info: ",time.time() - a)
            storePool_info(mint, amm_info)
            return {
                'amm_id': Pubkey.from_string(amm_info['id']),
                'authority': Pubkey.from_string(amm_info['authority']),
                'base_mint': Pubkey.from_string(amm_info['baseMint']),
                'base_decimals': amm_info['baseDecimals'],
                'quote_mint': Pubkey.from_string(amm_info['quoteMint']),
                'quote_decimals': amm_info['quoteDecimals'],
                'lp_mint': Pubkey.from_string(amm_info['lpMint']),
                'open_orders': Pubkey.from_string(amm_info['openOrders']),
                'target_orders': Pubkey.from_string(amm_info['targetOrders']),
                'base_vault': Pubkey.from_string(amm_info['baseVault']),
                'quote_vault': Pubkey.from_string(amm_info['quoteVault']),
                'market_id': Pubkey.from_string(amm_info['marketId']),
                'market_base_vault': Pubkey.from_string(amm_info['marketBaseVault']),
                'market_quote_vault': Pubkey.from_string(amm_info['marketQuoteVault']),
                'market_authority': Pubkey.from_string(amm_info['marketAuthority']),
                'bids': Pubkey.from_string(amm_info['marketBids']),
                'asks': Pubkey.from_string(amm_info['marketAsks']),
                'event_queue': Pubkey.from_string(amm_info['marketEventQueue']),
                'pool_open_time' : time.time()
                }
        return 'failed'
    except Exception as e:
        print("Fetch pool error : ", e)
        return 'failed'
 