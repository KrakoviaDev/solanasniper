# from Wallet_Info import get_wallet_Info

from utils.alreadyBought import soldToken   
  
from utils.checkBalance import getBalance
from utils.computePrice import get_investment_worth 
from raydium.sell_swap import sell
from utils.birdeye import getSymbol
from monitoring_price.monitor_price_strategy import limit_order, trailing_stop_loss_func, take_profit_and_trailing_stop
from raydium.create_close_account import fetch_pool_keys
from utils.new_pools_list import check
import time

def raydium_swap(config, ctx, payer, desired_token_address, txB, execution_time, limit_order_sell_Bool, take_profit_ratio, trailing_stop_Bool, trailing_stop_ratio, Limit_and_Trailing_Stop_Bool):
    amm_type = "R"

    token_symbol, _ = getSymbol(desired_token_address)
    
    token = desired_token_address
    try:
        if check(desired_token_address) == True:
            pool_keys = fetch_pool_keys(desired_token_address)
            if str(pool_keys['base_mint']) != "So11111111111111111111111111111111111111112":
                token = str(pool_keys['base_mint'])
            else:
                token = str(pool_keys['quote_mint'])    
    except:
        pass
    tokenBalanceLamports = getBalance(token,ctx,payer)
    
    txB =  str(txB)   
    
    sell_NOW = True
    if limit_order_sell_Bool:
        sell_NOW = limit_order(ctx,payer,tokenBalanceLamports,desired_token_address, take_profit_ratio, execution_time, txB, amm_type)
    elif trailing_stop_Bool:
        sell_NOW = trailing_stop_loss_func(ctx,payer,tokenBalanceLamports,desired_token_address, trailing_stop_ratio, execution_time, txB, amm_type)

    elif Limit_and_Trailing_Stop_Bool:
        sell_NOW = take_profit_and_trailing_stop(ctx,payer,tokenBalanceLamports,desired_token_address, trailing_stop_ratio, take_profit_ratio, execution_time, txB, amm_type)

    # Call Sell Method - returns transaction hash (txS= tx for sell)
    if sell_NOW == False:
        bought_token_curr_price = get_investment_worth(ctx,payer,desired_token_address, tokenBalanceLamports)
        start_time = time.time()
        txS = sell(ctx, desired_token_address, payer)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Total Sell Execution time: {execution_time} seconds")

        if str(txS) != 'failed':
            txS =  str(txS)   

            print("-" * 79)
            print(f"| {'Sold Price':<15} | {'Tx Sell':<40} |")
            print("-" * 79)
            print(f"| {bought_token_curr_price:.12f} | {txS:<40} |")

            sendWebhook(f"msg_s|SELL INFO [Raydium] - {token_symbol}",f"Token Address: {desired_token_address}\nSold at: {bought_token_curr_price:.12f}\nTotal Sell Execution time: {execution_time} seconds\nSell TXN: https://solscan.io/tx/{txS}\n------------------- END -------------------")

            print("-" * 79)

            soldToken(desired_token_address)