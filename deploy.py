from solcx import compile_standard, install_solc
import json
from web3 import Web3

# reading solidity file
with open("./simpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# print("Installing...")
# install_solc("0.8.10")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.10",
)

# add compiled code to new file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# print(compiled_sol)

# get the bytecode of compiled json
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["simpleStorage"]["evm"][
    "bytecode"
]["object"]

# get the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["simpleStorage"]["abi"]


# connecting to goerli using metamask
w3 = Web3(
    Web3.HTTPProvider(
        "https://eth-goerli.g.alchemy.com/v2/kD-0wKg6VppcSBK69zrDBWgZ2u8De0QQ"
    )
)
chain_id = 5
my_address = "0xCb1ec569877d8CBF1dC3474890636BEd5AE2bE0f"
private_key = "0xde7517afd632df312ba9a509ed9480207983bb8a295aff07138cd1b16425aec0"

# create the contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get nonce value
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

"""build a transaction; sign a transaction; send the transaction"""
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# print(transaction)
print("deploying contract")
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("contract deployed")
# print(tx_receipt)


# working with the contract need contract address and contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.storeNumber(9).call())
print("storing number")
store_transaction = simple_storage.functions.storeNumber(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        # "to": "0xf387ff10d153C4594f794aB75204A37ffc63277C",
        "nonce": nonce + 1,
    }
)
signed_store_tx = w3.eth.account.sign_transaction(store_transaction, private_key)
store_tx_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
storetx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)
print("number stored: ")
