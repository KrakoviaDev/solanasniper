
from solders.signature import Signature

def get_pair_address_new_pool(ctx, sig):
    pair_address = False 
    try:
        sig1 = Signature.from_string(sig)
        instructions = ctx.get_transaction(sig1,encoding="jsonParsed", max_supported_transaction_version=0).value.transaction.transaction.message.instructions
        for ins in instructions:
            if "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8" in str(ins.program_id): 
                pair_address = str(ins.accounts[4])
        return pair_address 
    except:
        return pair_address