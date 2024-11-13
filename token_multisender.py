"""
Name: Token multisender
Description: Token multisender 
    - 3 mode: 
        1. 
        2. 
        3. 
Author: Belp2801
Created: 09.11.2024
"""

import customtkinter
from customtkinter import filedialog    
from tkinter import messagebox
import os, time, datetime
import csv, json

from baseclass import wallet
from baseclass import network

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class TabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.tabs = ["Type 1: 1 to n", "Type 2: n to 1", "Type 3: n to n"]
        # create 
        for tab in self.tabs:
            self.add(tab)

        self.init_data()
        self.init_vars()
        self.init_ctk_vars()
        self.build_widgets()

    def init_data(self):
        pass

    def init_vars(self):
        self.address_vars = []
        self.private_key_vars = []
        self.columns_vars = []
        self.file_vars = []

    def init_ctk_vars(self):
        for i in range(len(self.tabs)):
            self.address_vars.append(customtkinter.StringVar())
            self.private_key_vars.append(customtkinter.StringVar())
            self.columns_vars.append(customtkinter.StringVar())
            self.file_vars.append(customtkinter.StringVar())

    # region widgets
    def build_widgets(self):
        for i, tab in enumerate(self.tabs):
            self.build_tab_view(i, self.tab(tab))

    def build_tab_view(self, i, tab):
        self.build_address_widgets(i, tab)

    def build_address_widgets(self, i, tab):
        # Address and Private
        if i == 0:
            self.address_label = customtkinter.CTkLabel(tab, width=108, anchor="w", text="From Address (*):")
            self.address_entry = customtkinter.CTkEntry(tab, textvariable=self.address_vars[i], width=360, border_width=0)
            self.address_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.address_entry.grid(row=2, column=1, padx=5, pady=5, sticky="e")

            self.private_key_label = customtkinter.CTkLabel(tab, width=108, anchor="w", text="Private Key (*):")
            self.private_key_entry = customtkinter.CTkEntry(tab, textvariable=self.private_key_vars[i], width=360, border_width=0)
            self.private_key_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
            self.private_key_entry.grid(row=3, column=1, padx=5, pady=5, sticky="e")

        elif i == 1:
            self.address_label = customtkinter.CTkLabel(tab, width=108, anchor="w", text="To Address (*):")
            self.address_entry = customtkinter.CTkEntry(tab, textvariable=self.address_vars[i], width=360, border_width=0)
            self.address_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.address_entry.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        csv_columns_label = customtkinter.CTkLabel(tab, width=108, anchor="w", text="Columns: ")
        csv_columns_entry = customtkinter.CTkEntry(
            tab, width=360, border_width=0, state="disabled", textvariable=self.columns_vars[i]
        )
        csv_sample_button = customtkinter.CTkButton(
            tab, command=self.get_sample_file, width=80, text="Sample", hover=True
        )
        csv_columns_label.grid(row=0, column=0, padx=5, pady=4, sticky="e")
        csv_columns_entry.grid(row=0, column=1, padx=5, pady=5)
        csv_sample_button.grid(row=0, column=2, padx=5, pady=4)
        
        csv_upload_label = customtkinter.CTkLabel(tab, width=108, anchor="w", text="File (*): ")
        csv_upload_entry = customtkinter.CTkEntry(tab, width=360, border_width=0, textvariable=self.file_vars[i])
        csv_upload_button = customtkinter.CTkButton(
            tab, width=80, text="Select", command=self.handle_select_file
        )
        csv_upload_label.grid(row=1, column=0, padx=5, pady=4, sticky="e")
        csv_upload_entry.grid(row=1, column=1, padx=5, pady=4)
        csv_upload_button.grid(row=1, column=2, padx=5, pady=4)

    # endregion

    # region utils
    def get_current_tab_index(self):
        return self.index(self.get())
    
    def handle_get_csv_columns(self, tab, mode):    
        if tab == 0:
            if mode == 1 or mode == 2:
                return ["to_address"]
            elif mode == 3:
                return ["to_address", "value"]
        elif tab == 1:
            if mode == 1 or mode == 2:
                return ["from_address", "private_key"]
            elif mode == 3:
                return ["from_address", "private_key", "value"]
        elif tab == 2:
            if mode == 1 or mode == 2:
                return ["from_address", "private_key", "to_address"]
            elif mode == 3:
                return ["from_address", "private_key", "to_address", "value"]                  
                
    def handle_set_columns_vars(self, mode):
        for i in range(len(self.tabs)):
            columns = self.handle_get_csv_columns(i, mode)
            self.columns_vars[i].set(f"[{', '.join(columns)}]")
        
    def get_sample_file(self):
        current_tab = self.get_current_tab_index()
        columns = self.handle_get_csv_columns(current_tab, self.master.mode_var.get())
        filepath = f"acc_type_{current_tab}_{self.master.mode_var.get()}.csv"
        values = {key: "" for key in columns}
        
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(values.keys())
            writer.writerow(values.values())

        answer = messagebox.askquestion("Success", "Success! Do you want to open sample file?") 
        if answer == 'yes':
            os.startfile(filepath)

    def handle_select_file(self):
        _success = False
        current_tab = self.get_current_tab_index()
        while not _success:
            file_path = filedialog.askopenfilenames()
            if len(file_path) != 0 and not ".csv" in file_path[0]:
                messagebox.showerror(
                    "Wrong file format!", "Please select .csv!"
                )
            else:
                _success = True
                if len(file_path) != 0:
                    self.file_vars[current_tab].set(file_path[0])

    # endregion


class TokenMultiSender(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Token MultiSender")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.init_constants()
        self.init_data()
        self.init_ctk_vars()

        self.build_widgets()
        self.handle_get_network()

        self.tab_view.handle_set_columns_vars(self.mode_var.get())
    # region init
    def init_constants(self):
        pass

    def init_data(self):
        # networks
        self.networks = {}
        self.load_network_data()
        self.load_abi()
        # token types
        self.token_types = ["TOKEN", "NFT"]
        # modes
        self.modes = {1: "All", 2: "Value", 3: "Custom in file"} 

    def load_abi(self):
        with open('./data/abi.json', 'r') as f:
            self.abi = json.load(f)

    def load_network_data(self):
        with open("./data/networks.csv", "r") as f:
            reader = csv.DictReader(f)
            for line in reader:
                self.networks[line["name"]] = line

    def init_ctk_vars(self):
        self.network_var = customtkinter.StringVar(value=sorted(self.networks.keys())[0])
        self.token_type_var = customtkinter.StringVar()

        self.mode_var = customtkinter.IntVar()
        self.mode_var.set(1)
        self.value_var = customtkinter.DoubleVar()

        self.token_address_var = customtkinter.StringVar()
        self.unit_var = customtkinter.StringVar()
        self.columns_var = customtkinter.StringVar()

    # endregion

    # region build ui
    def build_widgets(self):
        self.build_type_frame()
        self.build_token_data_frame()
        self.build_tab_views()
        self.build_footers()

    def build_type_frame(self):
        self.type_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.type_frame.pack(padx=5, pady=(5, 0), fill="both", expand=True)

        self.build_network_widgets()
        self.build_token_type_widgets()

        self.network_frame.pack(side=customtkinter.LEFT)
        self.token_type_frame.pack(side=customtkinter.RIGHT)

    def build_network_widgets(self):
        def on_change_network(choice):
            self.handle_get_network()
        # Network
        self.network_frame = customtkinter.CTkFrame(self.type_frame, corner_radius=5, bg_color="transparent", fg_color="transparent")
        self.network_label = customtkinter.CTkLabel(self.network_frame, width=108, anchor="w", text="Network:")
        self.network_combobox = customtkinter.CTkOptionMenu(
            self.network_frame, 
            variable=self.network_var, 
            values=sorted(self.networks.keys()),
            fg_color=["#F9F9FA", "#343638"],
            text_color=["#000", "#fff"],
            command=on_change_network
        )
        self.network_combobox.set(sorted(self.networks.keys())[0])

        self.network_label.grid(row=0, column=0, padx=(16, 5), pady=8, sticky="w")
        self.network_combobox.grid(row=0, column=1, padx=5, pady=8, sticky="w")

    def build_token_type_widgets(self):
        # Token type
        self.token_type_frame = customtkinter.CTkFrame(self.type_frame, corner_radius=5, bg_color="transparent", fg_color="transparent")
        self.token_type_label = customtkinter.CTkLabel(self.token_type_frame, text="Token Type:")
        self.token_type_combobox = customtkinter.CTkOptionMenu(
            self.token_type_frame, 
            variable=self.token_type_var, 
            values=self.token_types,
            fg_color=["#F9F9FA", "#343638"],
            text_color=["#000", "#fff"]
        )
        self.token_type_combobox.set(self.token_types[0])

        self.token_type_label.grid(row=0, column=2, padx=(16, 5), pady=8, sticky="e")
        self.token_type_combobox.grid(row=0, column=3, padx=(16, 18), pady=8, sticky="e")

    def build_token_data_frame(self):
        self.token_data_frame = customtkinter.CTkFrame(self)
        self.token_data_frame.pack(padx=5, pady=(5, 0), fill="both", expand=True)

        self.build_token_address_widgets()
        # self.build_unit_widgets()
        self.build_mode_widgets()

    def build_mode_widgets(self):
        # Mode
        def on_select_mode(choice):
            for key, value in self.modes.items():
                if value == choice:
                    self.mode_var.set(key)

            self.tab_view.handle_set_columns_vars(self.mode_var.get())
            if self.mode_var.get() == 2:
                self.build_value_widgets()
            else:
                self.value_label.grid_forget()
                self.value_entry.grid_forget()
            
        self.mode_label = customtkinter.CTkLabel(self.token_data_frame, width=108, anchor="w", text="Mode (*):")
        self.mode_combobox = customtkinter.CTkOptionMenu(
            self.token_data_frame, 
            values=list(self.modes.values()),
            command=on_select_mode,
            fg_color=["#F9F9FA", "#343638"],
            text_color=["#000", "#fff"]
        )
        self.mode_combobox.set(list(self.modes.values())[0])
        self.mode_label.grid(row=2, column=0, padx=(16, 5), pady=5, sticky="w")
        self.mode_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def build_value_widgets(self):
        self.value_label = customtkinter.CTkLabel(self.token_data_frame, width=96, anchor="e", text="Value:")
        self.value_entry = customtkinter.CTkEntry(self.token_data_frame, width=65, justify=customtkinter.RIGHT, textvariable=self.value_var, border_width=0)

        self.value_label.grid(row=2, column=2, padx=(32, 5), pady=5, sticky="e")
        self.value_entry.grid(row=2, column=3, padx=(5, 0), pady=5, sticky="w")

    def build_unit_widgets(self):
        self.unit_label = customtkinter.CTkLabel(self.token_data_frame, text=f"Token: {self.unit_var.get()}")
        self.unit_label.grid(row=2, column=4, padx=5, pady=5)

    def build_token_address_widgets(self):
        # Token address
        self.token_address_label = customtkinter.CTkLabel(self.token_data_frame, width=108, anchor="w",  text="Token address:")
        self.token_address_entry = customtkinter.CTkEntry(self.token_data_frame, textvariable=self.token_address_var, width=360, border_width=0)
        self.token_address_button = customtkinter.CTkButton(self.token_data_frame, text="Check", width=80, command=self.handle_check_token_address)
        self.token_address_label.grid(row=1, column=0, padx=(16, 5), pady=(8, 5), sticky="w")
        self.token_address_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=(8, 5), sticky="w")
        self.token_address_button.grid(row=1, column=4, padx=5, pady=(8, 5), sticky="w")
        
    def build_tab_views(self):
        self.tab_view = TabView(master=self)
        self.tab_view.pack(padx=5, pady=(0, 0), fill="both", expand=True)

        for tab in self.tab_view.tabs:
            self.build_transfer_button(self.tab_view.tab(tab))

    def build_transfer_button(self, tab):
        self.transfer_button_frame = customtkinter.CTkFrame(tab)
        self.transfer_button_frame.place(x=432, y=160)
        
        self.transfer_button = customtkinter.CTkButton(self.transfer_button_frame, text="Transfer", command=self.transfer)
        self.transfer_button.pack()
    
    def build_footers(self):
        self.footers = customtkinter.CTkLabel(self, text="@Powered by: Belp2801")
        self.footers.pack(padx=5, pady=4)
    # endregion
    
    # region utils
    def handle_get_network(self):
        self.network = network.Network(self.networks, self.network_var.get())
        self.unit_var.set(self.network.token)
        
    def handle_set_unit(self):
        self.unit_label.configure(text=f"Token: {self.unit_var.get()}")

    def handle_check_token_address(self):
        self.handle_get_network()
        self.network.init_w3()
        address = self.token_address_var.get().strip()
        if address == "":
            messagebox.showerror("Error!", "Enter token address and try again!")
            return
        try:
            contract = self.network.w3.eth.contract(address=address, abi=self.abi)
            _name = contract.functions.name().call()
            _symbol = contract.functions.symbol().call()
            self.unit_var.set(_symbol)
            messagebox.showinfo("Success!", 
                                "\n".join([
                                    f"Get token data success:", "",
                                    f" >> Address: {address}", "",
                                    f" >> Name   : {_name}", "",
                                    f" >> Symbol : {_symbol}"
                                ]))
        except Exception as e:
            print(e)
            if "401" in str(e):
                messagebox.showerror("RPC Error!", "Check RPC url and try again!")
            else:
                messagebox.showerror("Address not found!", "Check token address and try again!")
            return
    
    def get_current_tab_index(self):
        return self.tab_view.index(self.tab_view.get())

    def current_time(self):
        return datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    def load_transfer_data(self, current_tab, file):
        transfer_data = []
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for i, line in enumerate(reader):
                if i == 0:
                    pass
                else:
                    transfer_data.append(line)

        return transfer_data

    def handle_get_value(self, mode, row):
        # All
        if mode == 1:
            pass
        # value
        elif mode == 2:
            return self.value_var.get()
        # Custom
        elif mode == 3:
            return row['value']

    def handle_set_transfer_data(self, transfer_data):
        current_tab = self.get_current_tab_index()

        tab_view = self.tab_view
        mode = self.mode_var.get()
        if current_tab == 1:
            _address = tab_view.address_vars[current_tab].get().strip()
            _private_key = tab_view.private_key_vars[current_tab].get().strip()
            _wallet = wallet.Wallet(_address, _private_key, self.network)
            _nonce = wallet.get_nonce()
            for row in transfer_data:
                row['from_address'] = tab_view.address_vars[current_tab].get().strip()
                row['private_key'] = tab_view.private_key_vars[current_tab].get().strip()
                row['wallet'] = _wallet
                row['nonce'] = _nonce
                row['value'] = self.handle_get_value(mode, row)
                _nonce += 1
        elif current_tab == 2:
            for row in transfer_data:
                _wallet = wallet.Wallet(row['from_wallet'], row['private_key'], self.network)
                row['to_address'] = tab_view.address_vars[current_tab].get().strip()
                row['wallet'] = _wallet
                row['nonce'] = _wallet.get_nonce()
                row['value'] = self.handle_get_value(mode, row)
                
        elif current_tab == 3:
            for row in transfer_data:
                _wallet = wallet.Wallet(row['from_wallet'], row['private_key'], self.network)
                row['wallet'] = _wallet
                row['nonce'] = _wallet.get_nonce()
                row['value'] = self.handle_get_value(mode, row)

        return transfer_data

    # endregion

    # region run
    def validate_before_transfer(self):
        return True

    def handle_error(self, error):
        return error

    def write_error_file(self, error_rows):
        error_filepath = f"error_{self.current_time()}.csv"
        with open(error_filepath, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow('from_address', 'to_address', 'error')
            writer.writerow(error_rows)
            
    
    def transfer_token(self, transfer_data):
        _error_count = 0
        _error_rows = []

        _token_address = self.token_address_var.get().strip()
        mode = self.mode_var.get()
        for row in transfer_data:
            try:
                _wallet = row['wallet']
                _to_address = row['to_address']
                _nonce = row['nonce']
                _value = row['value']

                if mode == 1:
                    _wallet.transfer_token(_to_address, _value, nonce=_nonce, mode="all")
                else:
                    _wallet.transfer_token(_to_address, _value, nonce=_nonce, mode="custom")
            except Exception as error:
                _error_count += 1
                _error_rows.append({
                    'from_address': row['from_address'],
                    'to_address': row['to_address'],
                    'error': self.handle_error,
                })

        self.write_error_file(_error_rows)

    def transfer(self):
        is_valid = self.validate_before_transfer()
        if not is_valid:
            return
        
        self.handle_get_network()
        self.network.init_w3()

        if self.token_address_var.get():
            self.network.load_contract(self.token_address_var.get().strip(), self.abi)

        print(self.network.gas_price)

        current_tab = self.get_current_tab_index()

        file = self.tab_view.file_vars[current_tab].get()

        transfer_data = self.load_transfer_data(current_tab, file)
        transfer_data = self.handle_set_transfer_data(transfer_data)

        self.transfer_token(transfer_data)
        
    # endregion


if __name__ == "__main__":
    app = TokenMultiSender()
    app.mainloop()
    
