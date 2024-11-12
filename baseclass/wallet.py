from web3 import Web3

# Class Wallet

class Wallet:
    def __init__(self, address, private_key, network):
        self.address = address
        self.private_key = private_key
        self.network = network

    # Lấy số dư của ví
    def get_balance(self):
        self.balance = self.network.w3.eth.get_balance(self.address)
        return self.balance

    # Lấy số transaction đã confirm
    def get_nonce(self):
        self.nonce = self.network.w3.eth.get_transaction_count(self.address)
        return self.nonce

    # Tính toán số token tối đa có thể chuyển
    def calculatate_max_amount(self, gas, gasPrice):
        self.get_balance()
        amount = self.balance - gas * gasPrice
        return amount

    # Chuyển token
    def transfer_token(self, recipient_address, amount, nonce=-1):
        if nonce == -1:
            nonce = self.get_nonce()

        # Build the transaction
        tx = {
            "gasPrice": self.network.get_gas_price(),
            "nonce": nonce,
            "chainId": self.network.chain_id,
            "to": recipient_address,
            "value": int(self.network.w3.to_wei(amount, "ether")),
        }

        if self.network.gas == 0:
            self.network.gas = self.network.w3.eth.estimate_gas(tx)
            print(self.network.gas)

        tx.update({"gas": self.network.gas})

        #print(tx)

        # Sign the transaction
        signed_tx = self.network.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key
        )

        # Send the transaction
        tx_hash = self.network.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print(
            f"Send {amount} {self.network.token} from {self.address} to {recipient_address}"
        )

    def multisend(self, list_address, amount):
        self.nonce = self.get_nonce()
        for address in list_address:
            self.transfer_token(address, amount, self.nonce)
            self.nonce += 1

    # Chuyển toàn bộ token
    def transfer_all_token(self, recipient_address):
        # Build the transaction
        tx = {
            "gasPrice": self.network.gas_price,
            "nonce": self.get_nonce(),
            "chainId": self.network.chain_id,
            "to": recipient_address,
        }
        if self.network.gas == 0:
            self.network.gas = self.network.w3.eth.estimate_gas(tx)
            print(self.network.gas)
        tx.update({"gas": self.network.gas})

        amount = self.calculatate_max_amount(self.network.gas, self.network.gas_price)
        tx.update({"value": amount})

        # Sign the transaction
        signed_tx = self.network.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key
        )

        print(
            f"Send {self.network.w3.from_wei(amount, 'ether')} {self.network.token} from {self.address} to {recipient_address}"
        )

        # Send the transaction
        tx_hash = self.network.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
