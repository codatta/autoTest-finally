# scripts/derive_key.py
# 从环境变量 MNEMONIC 派生以太坊私钥与地址（默认派生路径 m/44'/60'/0'/0/0）
# 使用 eth-account 的 HD 派生（若可用）。

import os
import sys

mnemonic = os.environ.get('MNEMONIC')
if not mnemonic:
    print('MNEMONIC env var not set', file=sys.stderr)
    sys.exit(2)

# sanitize whitespace
mnemonic = ' '.join(mnemonic.split())

try:
    from eth_account import Account
    # Some versions provide from_mnemonic or from_mnemonic, try common names
    try:
        acct = Account.from_mnemonic(mnemonic)
    except Exception:
        # Alternative API: Account.from_mnemonic with passphrase and account_path
        acct = Account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")
    priv = acct.key.hex()
    addr = acct.address
    print(priv)
    print(addr)
except Exception as e:
    print('Error deriving key:', e, file=sys.stderr)
    sys.exit(3)

