from construct import Bytes, Int8ul, Int64ul, BytesInteger
from construct import Struct as cStruct 

"""Thanks to v0idum for creating layouts in python""" 
 

POOL_INFO_LAYOUT = cStruct( 
    "instruction" / Int8ul,
    "simulate_type" / Int8ul
)
 
SWAP_LAYOUT = cStruct(
    "instruction" / Int8ul,
    "amount_in" / Int64ul,
    "min_amount_out" / Int64ul
) 