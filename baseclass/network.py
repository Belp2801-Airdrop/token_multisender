from web3 import Web3
import os

# Class Network

class Network:
    def __init__(self, network_dictionary, chain):
        self.network_dictionary = network_dictionary
        self.chain = chain
        self.get_data_of_chain(chain)
        # self.init_w3()
        self.gas = 21000 * 5
        self.gas_price = 0
        self.contract  = None
        self.w3 = None
        print("Get network data success!")

    # Lấy dữ liệu của chain
    # NXHinh 29.07.2024
    def get_data_of_chain(self, chain):
        self.name = self.network_dictionary[chain]["name"]
        self.token = self.network_dictionary[chain]["token"]
        self.rpc_url = self.network_dictionary[chain]["rpc_url"]
        self.scan_url = self.network_dictionary[chain]["scan_url"]
        self.chain_id = self.network_dictionary[chain]["chain_id"]

    # Hàm khởi tạo network
    def init_w3(self):
        if self.w3 == None:
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            self.get_gas_price()
        

    # Load contract
    def load_contract(self, contract_address, abi):
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)

    # Lấy gas_price
    def get_gas_price(self):
        if self.gas_price == 0:
            self.gas_price = self.w3.eth.gas_price
        return self.gas_price

    

