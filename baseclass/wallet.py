import web3
from web3 import Web3
from .network import Network


from hexbytes import HexBytes

# Class Wallet

class Wallet:
    def __init__(self, address, private_key):
        self.address = Web3.to_checksum_address(address)
        self.private_key = private_key

    # Lấy số dư của ví
    def get_balance(self, network):
        if network.contract == None:
            self.balance = network.w3.eth.get_balance(self.address)
        else:
            print(network.contract)
            self.balance = network.contract.functions.balanceOf(self.address).call()
        return network.w3.from_wei(self.balance, 'ether')

    # Lấy số transaction đã confirm
    def get_nonce(self, network):
        self.nonce = network.w3.eth.get_transaction_count(self.address)
        return self.nonce

    # Tính toán số token tối đa có thể chuyển
    def calculate_max_value(self, network, gas, gasPrice):
        self.get_balance()
        if network.contract == None:
            value = self.balance - gas * gasPrice
        else:
            value = self.balance
        return network.w3.from_wei(value, "ether")
    
    def is_valid_evm_address(self, address):
        return Web3.is_address(address)

    def build_transaction(self, network, recipient_address, value, nonce, is_all=False):
        # Build the transactions
        value = int(network.w3.to_wei(float(value), "ether"))
        if network.contract == None:
            tx = {
                "gas": 0,
                "gasPrice": network.gas_price,
                "nonce": nonce,
                "chainId": int(network.chain_id),
                "to": HexBytes(recipient_address),
                "value": value,
            }
        else:
            tx = network.network.contract.functions.transfer(
                recipient_address, value
            ).build_transaction(
                {
                    "gas": 0,
                    "gasPrice": network.gas_price,
                    "nonce": nonce,
                }
            )

        gas = network.w3.eth.estimate_gas(tx)
        tx.update({'gas': gas})

        if is_all:
            value = value - tx['gas'] * network.gas_price * network.gas_multiple
            tx.update({'value': value})

        print(tx)

        return tx

    # Chuyển token
    def transfer_token(self, network, recipient_address, value, nonce=-1, type="custom"):
        if nonce == -1:
            nonce = self.get_nonce()
            
        is_valid_address = self.is_valid_evm_address(recipient_address)
        if not is_valid_address:
            raise f"Invalid address {recipient_address}!"

        tx = self.build_transaction(network, recipient_address, value, nonce, is_all=(type=="all"))

        # Sign the transaction
        signed_tx = network.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key
        )

        # Send the transaction
        tx_hash = network.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(
            f"Send {value} {network.token} from {self.address} to {recipient_address}"
        )
