from web3 import Web3
from .network import Network

# Class Wallet

class Wallet:
    def __init__(self, address, private_key, network):
        self.address = address
        self.private_key = private_key
        self.network = network

    # Lấy số dư của ví
    def get_balance(self):
        if self.network.contract == None:
            self.balance = self.network.w3.eth.get_balance(self.address)
        else:
            self.balance = self.network.contract.functions.balanceOf.call(self.address)
        return self.balance

    # Lấy số transaction đã confirm
    def get_nonce(self):
        self.nonce = self.network.w3.eth.get_transaction_count(self.address)
        return self.nonce

    # Tính toán số token tối đa có thể chuyển
    def calculate_max_value(self, gas, gasPrice):
        self.get_balance()
        value = self.balance - gas * gasPrice
        return value


    def build_transaction(self, recipient_address, nonce, value):
        # Build the transaction
        if self.network.contract == None:
            tx = {
                "gasPrice": self.network.get_gas_price(),
                "nonce": nonce,
                "chainId": self.network.chain_id,
                "to": recipient_address,
                "value": int(self.network.w3.to_wei(value, "ether")),
            }
        else:
            tx = self.network.contract.functions.transfer(
                recipient_address, value
            ).build_transaction(
                {
                    "gasPrice": self.network.get_gas_price(),
                    "nonce": nonce,
                    "chainId": self.network.chain_id,
                }
            )

        if self.network.gas == 0:
            self.network.gas = self.network.w3.eth.estimate_gas(tx) * 2
            
        tx.update({"gas": self.network.gas})

        return tx

    # Chuyển token
    def transfer_token(self, recipient_address, value, nonce=-1, type="custom"):
        if nonce == -1:
            nonce = self.get_nonce()

        tx = self.build_transaction(recipient_address, value, nonce)

        if type == "custom":
            pass
        if type == "all":
            value = self.calculate_max_value(self.network.gas, self.network.gas_price)
            tx.update({"value": value})

        #print(tx)

        # Sign the transaction
        signed_tx = self.network.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key
        )

        # Send the transaction
        tx_hash = self.network.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print(
            f"Send {value} {self.network.token} from {self.address} to {recipient_address}"
        )
