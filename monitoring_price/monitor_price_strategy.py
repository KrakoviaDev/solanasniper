import time, os,sys 
from utils.computePrice import getSymbol, get_investment_worth, getQuoteToken 
from utils.alreadyBought import getSettings    
from configparser import ConfigParser       
     
"""      
Only Take Profit 
"""     

LAMPORTS_PER_SOL = 1000000000

def getInvestAmount(payer,ctx, desired_token_address):
    config = ConfigParser()
    config.read(os.path.join(sys.path[0], 'data', 'config.ini'))

    invest_ratio =  float(config.get("INVESTMENT", "invest_ratio"))
    # invest_amount_sol =  float(config.get("INVESTMENT", "invest_amount_in_sol"))

    Config_settings = getSettings(desired_token_address)
    invest_amount_sol = Config_settings['invest_amount_sol']
    
    
    if invest_ratio == 0: 
        amount_of_sol_to_swap = invest_amount_sol
    else:
        currBalance = ctx.get_balance(payer.pubkey()).value
        balanceAfterRatio = currBalance * (invest_ratio / 100)
        amount_of_sol_to_swap = currBalance - balanceAfterRatio
    
    return amount_of_sol_to_swap



def limit_order(ctx,payer,tokenBalanceLamports,desired_token_address, take_profit_ratio, execution_time, txB, amm_type):

    # if amm_type == "R":
    investment = getInvestAmount(payer,ctx, desired_token_address)
    # else:
    #     investment = bought_token_price

    token_symbol, _ = getSymbol(desired_token_address)
    sell_limit_token_worth = investment  *  take_profit_ratio

    print("-" * 79)
    print(f"| {'Token Amount':<12} | {'Sell Limit Worth':<12} |  {'Tx Buy':<50} |")
    print("-" * 79)
    print(f"|{tokenBalanceLamports} | {sell_limit_token_worth:.12f}  {txB:<50} |")
    print("-" * 79)

    sendWebhook(f"msg_b|BUY INFO {token_symbol}",f"Token Amount: {tokenBalanceLamports}\n**Sell Limit Worth: {sell_limit_token_worth:.4f}**\nTotal Buy Execution time: {execution_time:.1f} seconds\nBuy TXN: https://solscan.io/tx/{txB} |")

    # LOOP = CHECK IF PRICE >= SELL LIMIT
    priceLow = True
    # while priceLow and isTimePassed(time_limit) == False:
    while priceLow:
        # Check if time limit has been passed for the token bought or not
        if amm_type == "R":
            current_worth = get_investment_worth(ctx,payer,desired_token_address, tokenBalanceLamports)
        else:
            # bought_token_curr_price = get_price(desired_token_address)
            current_worth = getQuoteToken(desired_token_address, tokenBalanceLamports)
            
        
        
        print("-" * 79)
        print(f"| {'token_symbol'} | {'current_worth':<12} | {'Sell Limit Worth':<12} |  {'Tx Buy':<50} |")
        print(f"|{token_symbol} | {current_worth:.12f} | {sell_limit_token_worth:.12f}  {txB:<50} |")

        if current_worth  >= sell_limit_token_worth:
            print(f"Price limit reached: {current_worth}")
            sendWebhook(f"m_a|Limit Order INFO {token_symbol}",f"Price limit reached: {current_worth:.4f} |")
            priceLow = False # break the loop
        else:
            time.sleep(15)

    return priceLow


"""
Only Trailing Stop loss
"""
def trailing_stop_loss_func(ctx,payer,tokenBalanceLamports,desired_token_address, trailing_stop_ratio, execution_time, txB, amm_type):
    token_symbol, _ = getSymbol(desired_token_address)
    # if amm_type == "R":
    initial_investment = getInvestAmount(payer,ctx, desired_token_address)
    # else:
    #     investment = bought_token_price
    # Set initial trailing stop loss limit
    trailing_ratio_of_Price = (trailing_stop_ratio / 100) * initial_investment
    initial_trailing_stop_loss_token_price = initial_investment - trailing_ratio_of_Price


    
    print("-" * 79)
    print(f"| {'Token amount':<12} | {'Initial Trailing Stop Loss Limit':<12} |  {'Tx Buy':<50} |")
    print("-" * 79)
    print(f"|{tokenBalanceLamports:.12f} | {initial_trailing_stop_loss_token_price:.12f} | {txB:<50} |")
    print("-" * 79)

    sendWebhook(f"msg_b|BUY [TRAILING] INFO {token_symbol}"
                ,f"Token amount: {tokenBalanceLamports}\n" \
                f"**Initial Trailing Stop Loss Limit: {initial_trailing_stop_loss_token_price:.4f}**\n" \
                f"Total Buy Execution time: {execution_time:.1f} seconds\n" \
                f"Buy TXN: https://solscan.io/tx/{txB} |")

    # LOOP = CHECK IF PRICE >= SELL LIMIT 
    priceLow = True
    # while priceLow and isTimePassed(time_limit) == False:
    time.sleep(5)
    print(f"+|+ {'Trailing Stop Loss [Update]':<12} +|+")
    print("-" * 50)
    startingPrice=initial_investment

    trailing_ratio_of_Price = (trailing_stop_ratio / 100) * startingPrice
    latest_sell_stop_loss_token_price = startingPrice - trailing_ratio_of_Price 
    while priceLow:

        if amm_type == "R":
            bought_token_curr_price = get_investment_worth(ctx,payer,desired_token_address, tokenBalanceLamports)
        else:
            # bought_token_curr_price = get_price(desired_token_address)
            bought_token_curr_price = getQuoteToken(desired_token_address, tokenBalanceLamports)



        print(f"=|= {'SYMBOL':<12} =|= {'Token Amount':<12} =|= {'Current Worth':<12} =|= {'Latest Trailing Stop Loss Limit':<12} =|=")
        print("-" * 79)
        print(f"=|= {token_symbol:<12} =|= {tokenBalanceLamports} =|= {bought_token_curr_price:.12f} =|= {latest_sell_stop_loss_token_price:.12f} =|=")
        print("-" * 50)
        # if time limit has been passed for the token bought or not
        if bought_token_curr_price  <= latest_sell_stop_loss_token_price:
            print(f"Trailing Price limit reached: {bought_token_curr_price:.12f}")
            priceLow = False # break the loop
        elif bought_token_curr_price > startingPrice:
            
            trailing_ratio_of_Price = (trailing_stop_ratio / 100) * bought_token_curr_price
            latest_sell_stop_loss_token_price = bought_token_curr_price - trailing_ratio_of_Price 

            startingPrice = bought_token_curr_price
        else:
            time.sleep(15)


    print("-" * 79)
    print(f"| {'Token amount':<12} | {'Latest Trailing Stop Loss Limit':<12} |  {'Tx Buy':<50} |")
    print("-" * 79)
    print(f"|{tokenBalanceLamports} | {latest_sell_stop_loss_token_price:.12f} | {txB:<50} |")
    print("-" * 79)

    sendWebhook(f"m_a|BUY [TRAILING] INFO {token_symbol}",
                f"Token Amount: {tokenBalanceLamports}\n" \
                f"**Latest Trailing Stop Loss Limit: {latest_sell_stop_loss_token_price:.4f}**\n" \
                f"Total Buy Execution time: {execution_time:.1f} seconds\n"\
                f"Buy TXN: https://solscan.io/tx/{txB} |")

    return priceLow







"""
Trailing Stop + Take Profit
"""
def take_profit_and_trailing_stop(ctx,payer,tokenBalanceLamports,desired_token_address, trailing_stop_ratio, take_profit_ratio, execution_time, txB, amm_type):
    # if amm_type == "R":

    initial_investment = getInvestAmount(payer,ctx, desired_token_address)
    
    token_symbol, _ = getSymbol(desired_token_address)
    
    # CALCULATE SELL LIMIT
    sell_limit_token_price = initial_investment  *  take_profit_ratio

    # Set initial trailing stop loss limit
    trailing_ratio_of_Price = (trailing_stop_ratio / 100) * initial_investment
    initial_trailing_stop_loss_token_price = initial_investment - trailing_ratio_of_Price
    
    print("-" * 79)
    print(f"| {'Tokens Amount':<12} | {'Sell Limit Price':<12} | {'Initial Trailing Stop Loss Limit':<12} |  {'Tx Buy':<50} |")
    print("-" * 79)
    print(f"|{tokenBalanceLamports:.12f} | {sell_limit_token_price:.12f} | {initial_trailing_stop_loss_token_price:.12f} | {txB:<50} |")
    print("-" * 79)

    sendWebhook(f"msg_b|BUY [TRAILING+Limit] INFO {token_symbol}",
                f"Token amount: {tokenBalanceLamports}\n\n" \
                f"**Sell Take Profit Limit: {sell_limit_token_price:.4f}**\n" \
                f"**Initial Trailing Stop Loss Limit: {initial_trailing_stop_loss_token_price:.4f}**\n\n" \
                f"Total Buy Execution time: {execution_time:.1f} seconds\nBuy TXN: https://solscan.io/tx/{txB} |")

    # LOOP = CHECK IF PRICE >= SELL LIMIT 
    priceLow = True
    # while priceLow and isTimePassed(time_limit) == False:
    time.sleep(5)
    print(f"+|+ {'TRAILING+Limit [Update]':<12} +|+")
    print("-" * 50)
    startingPrice=initial_investment

    trailing_ratio_of_Price = (trailing_stop_ratio / 100) * startingPrice
    latest_sell_stop_loss_token_price = startingPrice - trailing_ratio_of_Price
    Up = 0 
    while priceLow:

        if amm_type == "R":
            bought_token_curr_price = get_investment_worth(ctx,payer,desired_token_address, tokenBalanceLamports)
        else:
            # bought_token_curr_price = get_price(desired_token_address)
            bought_token_curr_price = getQuoteToken(desired_token_address, tokenBalanceLamports)

        # if time limit has been passed for the token bought or not
        if bought_token_curr_price  >= sell_limit_token_price:
            print(f"Sell limit reached: {bought_token_curr_price:.12f}")
            priceLow = False # break the loop
        elif bought_token_curr_price  <= latest_sell_stop_loss_token_price:
            print(f"Trailing Price limit reached: {bought_token_curr_price:.12f}")
            priceLow = False # break the loop
        elif bought_token_curr_price > startingPrice:
            
            trailing_ratio_of_Price = (trailing_stop_ratio / 100) * bought_token_curr_price
            latest_sell_stop_loss_token_price = bought_token_curr_price - trailing_ratio_of_Price 

            startingPrice = bought_token_curr_price
            
        if priceLow != False:
            print(f"=|= {'token_symbol':<12} =|=  {'Current Price':<12} =|= {'Sell Limit Price':<12} =|= {'Latest Trailing Stop Loss Limit':<12} =|======== {Up}")
            print("-" * 79)
            print(f"=|={token_symbol:<12} =|= {bought_token_curr_price:.12f} =|= {sell_limit_token_price:.12f} =|= {latest_sell_stop_loss_token_price:.12f} =|=")
            print("-" * 50)
            time.sleep(15)
            Up = Up + 1


    print("-" * 79)
    print(f"| {'Sell Worth':<12} | {'Sell Limit Price':<12} | {'Latest Trailing Stop Loss Limit':<12} |  {'Tx Buy':<50} |")
    print("-" * 79)
    print(f"|{bought_token_curr_price:.12f} | {sell_limit_token_price:.12f} | {latest_sell_stop_loss_token_price:.12f} | {txB:<50} |")
    print("-" * 79)

    sendWebhook(f"m_a|BUY [TRAILING+Limit] INFO {token_symbol}",
                f"Current Worth: {bought_token_curr_price:.4f} SOL\n" \
                f"**Sell Limit Price: {sell_limit_token_price:.4f}**\n" \
                f"**Latest Trailing Stop Loss Limit: {latest_sell_stop_loss_token_price:.4f}**\n"  \
                f"Total Buy Execution time: {execution_time:.1f} seconds\n" \
                f"Buy TXN: https://solscan.io/tx/{txB} |")


    return priceLow
 