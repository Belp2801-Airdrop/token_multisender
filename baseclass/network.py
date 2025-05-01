from web3 import Web3

# Class Network

class Network:
    def __init__(self, network_dictionary, chain):
        self.chain = chain
        self.get_data_of_chain(network_dictionary, chain)
        self.gas_price = 0
        self.contract = None
        self.init_w3()
        print(f"Active network: {chain}")

    # Lấy dữ liệu của chain
    # NXHinh 29.07.2024
    def get_data_of_chain(self, network_dictionary, chain):
        self.name = network_dictionary[chain]["name"]
        self.token = network_dictionary[chain]["token"]
        self.rpc_url = network_dictionary[chain]["rpc_url"]
        self.scan_url = network_dictionary[chain]["scan_url"]
        self.chain_id = network_dictionary[chain]["chain_id"]
        try:
            self.gas_multiple = int(network_dictionary[chain]["gas_multiple"])
        except:   
            self.gas_multiple = 1

    # Hàm khởi tạo network
    def init_w3(self):
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
    # Load contract
    def load_contract(self, contract_address, abi):
        if contract_address != "" and Web3.is_address(contract_address):
            self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
        else:
            self.contract = None

    # Lấy gas_price
    def get_gas_price(self):
        if self.gas_price == 0:
            self.gas_price = self.w3.eth.gas_price
        return self.gas_price

    

