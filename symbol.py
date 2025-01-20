async def _create_associated_token_account(token):
    # Create Associated token account for token to swap if not available
    token_associated_account = get_associated_token_address(
        WALLET.public_key,
        PublicKey(token)
    ) 
    opts = TxOpts(skip_preflight=True , max_retries=11)
    ata = await SOLANA_CLIENT.get_account_info(PublicKey(token_associated_account))
    if not ata.get('result').get('value'):
        try:
            instruction = create_associated_token_account(
                WALLET.public_key,
                WALLET.public_key,
                PublicKey(token)
            )
            txn = Transaction().add(instruction)
            txn.recent_blockhash = await SOLANA_CLIENT.get_recent_blockhash()
            await SOLANA_CLIENT.send_transaction(txn, WALLET, opts=opts)
        except Exception as e:
            print("Error occured while creating ata: ", str(e))
            return e
        
    else:
        print("Associated token account exists: ", ata)


async def swap(input, generatedRouteMap):
    # Check for any possible ARB opportunities
    while True:
        for token in generatedRouteMap[:150]:
            usdcToToken = await get_coin_quote(
                '',
                token,
                input
            )
            if usdcToToken.get('data'):
                tokenToUsdc = await get_coin_quote(
                    token,
                    '',
                    usdcToToken.get('data')[0].get('otherAmountThreshold')
                )

                if tokenToUsdc.get('data'):
                    if tokenToUsdc.get('data')[0].get('otherAmountThreshold') > input:
                        await _create_associated_token_account(token)
                        await serialized_swap_transaction(usdcToToken.get('data')[0], tokenToUsdc.get('data')[0])
                        profit = tokenToUsdc.get('data')[0].get('otherAmountThreshold') - input
                        print("Approx Profit made: ", profit / USDC_BASE)
    

if __name__ == '__main__':
    generatedRouteMap = get_route_map()
    asyncio.run(swap(INPUT_USDC_AMOUNT, generatedRouteMap))
 