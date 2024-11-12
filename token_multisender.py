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
from tkinter import messagebox
import os, time, datetime
import csv

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
        csv_upload_entry = customtkinter.CTkEntry(tab, width=360, border_width=0)
        csv_upload_button = customtkinter.CTkButton(
            tab, width=80, text="Select"
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
                return ["to_address", "amount"]
        elif tab == 1:
            if mode == 1 or mode == 2:
                return ["from_address", "private_key"]
            elif mode == 3:
                return ["from_address", "private_key", "amount"]
        elif tab == 2:
            if mode == 1 or mode == 2:
                return ["from_address", "private_key", "to_address"]
            elif mode == 3:
                return ["from_address", "private_key", "to_address", "amount"]                  
                
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
        self.abi = [{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]  

        # token types
        self.token_types = ["TOKEN", "NFT"]
        # modes
        self.modes = {1: "All", 2: "Amount", 3: "Custom in file"} 

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
        
        self.transfer_button = customtkinter.CTkButton(self.transfer_button_frame, text="Transfer", command=self.transfer_token)
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

    # endregion

    # region run
    def transfer_token(self):
        pass
    # endregion


if __name__ == "__main__":
    app = TokenMultiSender()
    app.mainloop()
    
