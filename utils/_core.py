from spl.token.instructions import close_account, CloseAccountParams, get_associated_token_address, 
    create_associated_token_account  
from solana.rpc.types import TokenAccountOpts 
from solana.rpc.api import RPCException 
from solana.transaction import Transaction 
from solana.rpc.api import Pubkey 
from spl.token.client import Token
from solana.rpc.commitment import Commitment 
from spl_token.core import _TokenCore
from utils._instructions import make_swap_instruction, get_token_account
from utils.layouts import MARKET_STATE_LAYOUT_V3, SPL_MINT_LAYOUT


def transfer_pool_keys_to_pk(pool_keys: dict):
    tf_pool_keys = {}
    for name, value in pool_keys.items():
        if isinstance(value, int):
            tf_pool_keys[name] = value
        else:
            tf_pool_keys[name] = Pubkey.from_string(value)

    return tf_pool_keys


async def buy(solana_client, token_mint, payer, amount, pool_keys):
    print("准备买入")
    if not all([solana_client, token_mint, payer, amount, pool_keys]):
        empty_parameters = [p for p in [solana_client, token_mint, payer, amount, pool_keys] if p is None]
        print(f"Not enough parameters: {empty_parameters}")
        return
    amount_in = int(amount * 1000000000)
    mint = Pubkey.from_string(token_mint)
    tf_pool_keys = transfer_pool_keys_to_pk(pool_keys)
    accountProgramId = solana_client.get_account_info_json_parsed(mint)
    TOKEN_PROGRAM_ID = accountProgramId.value.owner
    swap_associated_token_address, swap_token_account_Instructions = get_token_account(solana_client, payer.pubkey(),
                                                                                       mint)

    balance_needed = Token.get_min_balance_rent_for_exempt_for_account(solana_client)
    new_pair_pk, swap_tx, payer, new_pair, opts, = _TokenCore._create_wrapped_native_account_args(
        TOKEN_PROGRAM_ID, payer.pubkey(), payer, amount_in,
        False, balance_needed, Commitment("confirmed"))

    instructions_swap = make_swap_instruction(amount_in,
                                              new_pair_pk,
                                              swap_associated_token_address,
                                              tf_pool_keys,
                                              mint,
                                              solana_client,
                                              payer
                                              )

    params = CloseAccountParams(account=new_pair_pk, dest=payer.pubkey(), owner=payer.pubkey(),
                                program_id=TOKEN_PROGRAM_ID)
    closeAcc = (close_account(params))
    if swap_token_account_Instructions != None:
        swap_tx.add(swap_token_account_Instructions)
    swap_tx.add(instructions_swap)
    swap_tx.add(closeAcc)

    try:
        solana_client.send_transaction(swap_tx, payer, new_pair)
        print("买入成功")
        return True
    except:
        print("买入失败")
        return


async def sell(client, token_mint, payer, pool_keys):
    print("准备卖出")
    tokenPk = Pubkey.from_string(str(token_mint))
    sol = Pubkey.from_string("So11111111111111111111111111111111111111112")

    tf_pool_keys = transfer_pool_keys_to_pk(pool_keys)
    account_program_id = client.get_account_info_json_parsed(tokenPk)
    program_id_of_token = account_program_id.value.owner
    if not payer:
        return
    accounts = client.get_token_accounts_by_owner_json_parsed(payer.pubkey(), TokenAccountOpts(
        program_id=program_id_of_token)).value
    amount_in = 0
    for account in accounts:
        mint_in_acc = account.account.data.parsed['info']['mint']
        if mint_in_acc == str(tokenPk):
            amount_in = int(account.account.data.parsed['info']['tokenAmount']['amount'])
            break
    # 卖出数量判断
    if amount_in == 0:
        return
    account_data = client.get_token_accounts_by_owner(payer.pubkey(), TokenAccountOpts(tokenPk))
    if account_data.value:
        swap_token_account = account_data.value[0].pubkey
    else:
        return
    if not swap_token_account:
        return

    try:
        account_data = client.get_token_accounts_by_owner(payer.pubkey(), TokenAccountOpts(sol))
        wsol_token_account = account_data.value[0].pubkey
        wsol_token_account_Instructions = None
    except:
        wsol_token_account = get_associated_token_address(payer.pubkey(), sol)
        wsol_token_account_Instructions = create_associated_token_account(payer.pubkey(), payer.pubkey(), sol)

    instructions_swap = make_swap_instruction(amount_in, swap_token_account, wsol_token_account, tf_pool_keys, tokenPk,
                                              client, payer)
    params = CloseAccountParams(account=wsol_token_account, dest=payer.pubkey(), owner=payer.pubkey(),
                                program_id=program_id_of_token)
    closeAcc = close_account(params)
    swap_tx = Transaction()
    signers = [payer]
    if wsol_token_account_Instructions != None:
        swap_tx.add(wsol_token_account_Instructions)
    swap_tx.add(instructions_swap)
    swap_tx.add(closeAcc)
    try:
        client.send_transaction(swap_tx, *signers)
        return True
    except RPCException as e:
        print("卖出失败")
        return


def get_pool_infos(accounts, solana_client):
    # 用户余额校验部分省去
    baseMintAccount = solana_client.get_account_info(accounts[8])
    quoteMintAccount = solana_client.get_account_info(accounts[9])
    marketAccount = solana_client.get_account_info(accounts[16])
    if baseMintAccount == None or quoteMintAccount == None or marketAccount == None:
        raise Exception('get account info error')

    baseMintInfo = SPL_MINT_LAYOUT.parse(baseMintAccount.value.data)
    quoteMintInfo = SPL_MINT_LAYOUT.parse(quoteMintAccount.value.data)
    marketInfo = MARKET_STATE_LAYOUT_V3.parse(marketAccount.value.data)
    poolInfos = {
        "id": accounts[4].__str__(),
        "baseMint": accounts[8].__str__(),
        "quoteMint": accounts[9].__str__(),
        "lpMint": accounts[7].__str__(),
        "baseDecimals": baseMintInfo.decimals,
        "quoteDecimals": quoteMintInfo.decimals,
        "lpDecimals": baseMintInfo.decimals,
        'version': 4,
        'authority': accounts[5].__str__(),
        'openOrders': accounts[6].__str__(),
        'targetOrders': accounts[12].__str__(),
        'baseVault': accounts[10].__str__(),
        'quoteVault': accounts[11].__str__(),
        'marketVersion': 3,
        'marketProgramId': solana_client.get_account_info_json_parsed(accounts[16]).value.owner.__str__(),
        'marketId': accounts[16].__str__(),
        'marketAuthority': get_associated_token_address(marketInfo['ownAddress'], accounts[16]).__str__(),
        'marketBaseVault': Pubkey.from_bytes(marketInfo.baseVault).__str__(),
        'marketQuoteVault': Pubkey.from_bytes(marketInfo.quoteVault).__str__(),
        'marketBids': Pubkey.from_bytes(marketInfo.bids).__str__(),
        'marketAsks': Pubkey.from_bytes(marketInfo.asks).__str__(),
        'marketEventQueue': Pubkey.from_bytes(marketInfo.eventQueue).__str__()
    }
    return poolInfos
