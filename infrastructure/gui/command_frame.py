from tkinter import END, BooleanVar

import customtkinter as ctk

from constants.constants import CommandFrameParams
from domains.domains import PhoneNumbersData
from interface_adapters.controllers.pool_to_regex_controller import PoolController
from interface_adapters.controllers.regex_to_pool_controller import RegexController
from interface_adapters.presentators.pool_to_regex_presentator import RegexPresentator
from interface_adapters.presentators.regex_to_pool_presentator import PoolPresentator
from use_cases.optimization_pool_to_regex import RegexOptimizer
from use_cases.optimization_regex_to_pool import PoolOptimizer
from use_cases.pool_to_regex import RegexManager
from use_cases.regex_to_pool import PoolManager


class CommandFrame(ctk.CTkFrame):
    """
    Фрейм с элементами управления.
    """  # noqa: RUF002

    def __init__(self, parent, gui_adapter):
        super().__init__(parent, fg_color="whitesmoke")

        self.pack(padx=20, pady=10, fill="x", side="bottom")
        self.parent = parent
        self.gui_adapter = gui_adapter

        self.regex_controller = RegexController()
        self.pool_controller = PoolController()

        self.regex_manager = RegexManager()
        self.pool_manager = PoolManager()

        self.regex_optimizer = RegexOptimizer()
        self.pool_optimizer = PoolOptimizer()

        self.regex_presentator = RegexPresentator()
        self.pool_presentator = PoolPresentator()

        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.dot_status = BooleanVar()
        self.special_symbols_status = BooleanVar()

        self.create_elements()

    def pool_to_regex_execute(self):
        self.parent.master.master.data_frame.regexp_text.delete("1.0", END)

        separator = self.separator_entry.get()
        if separator == "":
            separator = "|"

        use_dot = self.dot_status.get()

        unuse_special_symbols = self.special_symbols_status.get()

        try:
            phone_numbers_data = PhoneNumbersData([])
            groups = self.pool_controller.prepare_data(
                self.parent.master.master.data_frame.pools_text.get("1.0", "end-1c")
            )
            phone_numbers_data.data_list = groups

            regexes = self.regex_manager.pools_to_regex(phone_numbers_data, separator, unuse_special_symbols)

            optimized_regexes = self.regex_optimizer.execute_optimize(regexes, use_dot, unuse_special_symbols)

            result = self.regex_presentator.prepare_data(optimized_regexes, separator)

            self.parent.master.master.data_frame.regexp_text.insert("1.0", result)
        except Exception as e:
            self.gui_adapter.show_error(message=e)
            raise e

    def regex_to_pool_execute(self):
        self.parent.master.master.data_frame.pools_text.delete("1.0", END)

        separator = self.separator_entry.get()
        if separator == "":
            separator = "|"

        try:
            phone_numbers_data = PhoneNumbersData([])
            regexes = self.regex_controller.prepare_data(
                self.parent.master.master.data_frame.regexp_text.get("1.0", "end-1c"), separator
            )
            phone_numbers_data.data_list = regexes

            pools = self.pool_manager.regex_to_pool(phone_numbers_data)

            optimized_pools = self.pool_optimizer.execute_optimize(pools)

            result = self.pool_presentator.prepare_data(optimized_pools)

            self.parent.master.master.data_frame.pools_text.insert("1.0", result)
        except Exception as e:
            self.gui_adapter.show_error(message=e)
            raise e

    def clear_fields(self):
        self.parent.master.master.data_frame.pools_text.delete("1.0", END)
        self.parent.master.master.data_frame.regexp_text.delete("1.0", END)
        self.separator_entry.delete(0, END)
        self.dot_status.set(False)

    def create_elements(self):
        pool_to_regexp_button = ctk.CTkButton(
            self,
            width=600,
            height=32,
            text=CommandFrameParams.COMMAND_POOL_TO_REGEXP_BUTTON,
            command=lambda: self.pool_to_regex_execute(),
        )
        pool_to_regexp_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        regexp_to_pool_button = ctk.CTkButton(
            self,
            width=600,
            height=32,
            text=CommandFrameParams.COMMAND_REGEXP_TO_POOL_BUTTON,
            command=lambda: self.regex_to_pool_execute(),
        )
        regexp_to_pool_button.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        clear_button = ctk.CTkButton(
            self, height=32, text=CommandFrameParams.CLEAR_BUTTON_TEXT, command=self.clear_fields
        )
        clear_button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="n")

        self.separator_label = ctk.CTkLabel(self, text=CommandFrameParams.SEPARATOR)
        self.separator_label.grid(row=1, column=1, padx=10, pady=(5, 0), sticky="s")
        self.separator_entry = ctk.CTkEntry(self, height=32)
        self.separator_entry.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="n")

        self.dot_checkbutton = ctk.CTkCheckBox(
            self, variable=self.dot_status, onvalue=True, offvalue=False, text=CommandFrameParams.DOT
        )
        self.dot_checkbutton.grid(row=2, column=2, padx=10, pady=(0, 5), sticky="n")

        self.special_symbols_checkbutton = ctk.CTkCheckBox(
            self,
            variable=self.special_symbols_status,
            onvalue=True,
            offvalue=False,
            text=CommandFrameParams.SPECIAL_SYMBOLS,
        )
        self.special_symbols_checkbutton.grid(row=2, column=3, padx=10, pady=(0, 5), sticky="n")
