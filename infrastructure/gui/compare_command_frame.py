from tkinter import END, BooleanVar
from typing import Union

import customtkinter as ctk
from icecream import ic

from constants.constants import CompareCommandFrameParams
from domains.domains import PhoneNumbersData
from interface_adapters.controllers.regex_to_pool_controller import RegexController
from interface_adapters.presentators.pool_to_regex_presentator import RegexPresentator
from interface_adapters.presentators.regex_to_pool_presentator import PoolPresentator
from use_cases.optimization_regex_to_pool import PoolOptimizer
from use_cases.regex_to_pool import PoolManager


class CompareCommandFrame(ctk.CTkFrame):
    """
    Фрейм с элементами управления для сравнения регулярных выражений.
    """  # noqa: RUF002

    def __init__(self, parent, gui_adapter):
        super().__init__(parent, fg_color="whitesmoke")

        self.pack(padx=20, pady=10, fill="both", side="bottom")
        self.parent = parent
        self.gui_adapter = gui_adapter

        self.regex_controller = RegexController()

        self.pool_manager = PoolManager()

        self.pool_optimizer = PoolOptimizer()

        self.regex_presentator = RegexPresentator()
        self.pool_presentator = PoolPresentator()

        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.display_pools_status = BooleanVar()

        self.create_elements()

    def expand(self, entries: list[Union[str, tuple[str, str]]]) -> list[str]:
        numbers: list[str] = []
        for entry in entries:
            if isinstance(entry, tuple):
                start_str, end_str = entry
                width = len(start_str)
                start, end = int(start_str), int(end_str)
                for n in range(start, end + 1):
                    numbers.append(str(n).zfill(width))
            else:
                numbers.append(entry)
        return numbers

    def compare_regexs_execute(self):
        self.parent.master.master.compare_data_frame.left_result_text.delete("1.0", END)
        self.parent.master.master.compare_data_frame.right_result_text.delete("1.0", END)

        left_separator = self.left_separator_entry.get()
        if left_separator == "":
            left_separator = "|"
        right_separator = self.right_separator_entry.get()
        if right_separator == "":
            right_separator = "|"

        try:
            left_phone_numbers_data = PhoneNumbersData([])
            right_phone_numbers_data = PhoneNumbersData([])

            left_regexes = self.regex_controller.prepare_data(
                self.parent.master.master.compare_data_frame.left_regexp_text.get("1.0", "end-1c"), left_separator
            )
            right_regexes = self.regex_controller.prepare_data(
                self.parent.master.master.compare_data_frame.right_regexp_text.get("1.0", "end-1c"), right_separator
            )

            left_diff_regexes = list((set(left_regexes)).difference(set(right_regexes)))
            right_diff_regexes = list((set(right_regexes)).difference(set(left_regexes)))

            left_phone_numbers_data.data_list = left_diff_regexes
            right_phone_numbers_data.data_list = right_diff_regexes

            if self.display_pools_status.get() is False:
                left_regexp_result = self.regex_presentator.prepare_data(left_phone_numbers_data, left_separator)
                right_regexp_result = self.regex_presentator.prepare_data(right_phone_numbers_data, right_separator)

                self.parent.master.master.compare_data_frame.left_result_text.insert("1.0", left_regexp_result)
                self.parent.master.master.compare_data_frame.right_result_text.insert("1.0", right_regexp_result)
            else:
                left_pools = self.pool_manager.regex_to_pool(left_phone_numbers_data)
                right_pools = self.pool_manager.regex_to_pool(right_phone_numbers_data)

                left_expand_phone_numbers = set(self.expand(left_pools.data_list))
                right_expand_phone_numbers = set(self.expand(right_pools.data_list))

                left_phone_numbers_data.data_list = sorted(
                    left_expand_phone_numbers.difference(right_expand_phone_numbers)
                )
                right_phone_numbers_data.data_list = sorted(
                    right_expand_phone_numbers.difference(left_expand_phone_numbers)
                )

                ic(left_phone_numbers_data.data_list)
                ic(right_phone_numbers_data.data_list)

                left_optimized_pools = self.pool_optimizer.execute_optimize(left_phone_numbers_data)
                right_optimized_pools = self.pool_optimizer.execute_optimize(right_phone_numbers_data)

                ic(left_optimized_pools.data_list)
                ic(right_optimized_pools.data_list)

                left_result = self.pool_presentator.prepare_data(left_optimized_pools)
                right_result = self.pool_presentator.prepare_data(right_optimized_pools)

                self.parent.master.master.compare_data_frame.left_result_text.insert("1.0", left_result)
                self.parent.master.master.compare_data_frame.right_result_text.insert("1.0", right_result)
        except Exception as e:
            self.gui_adapter.show_error(message=e)
            raise e

    def clear_fields(self):
        self.parent.master.master.compare_data_frame.left_regexp_text.delete("1.0", END)
        self.parent.master.master.compare_data_frame.right_regexp_text.delete("1.0", END)
        self.parent.master.master.compare_data_frame.left_result_text.delete("1.0", END)
        self.parent.master.master.compare_data_frame.right_result_text.delete("1.0", END)
        self.left_separator_entry.delete(0, END)
        self.right_separator_entry.delete(0, END)
        self.display_pools_status.set(False)

    def create_elements(self):
        self.left_separator_label = ctk.CTkLabel(self, text=CompareCommandFrameParams.LEFT_SEPARATOR)
        self.left_separator_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="s")
        self.left_separator_entry = ctk.CTkEntry(self, height=32)
        self.left_separator_entry.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="n")

        compare_regexps_button = ctk.CTkButton(
            self,
            width=600,
            height=32,
            text=CompareCommandFrameParams.COMMAND_COMPARE_REGEXPS_BUTTON,
            command=lambda: self.compare_regexs_execute(),
        )
        compare_regexps_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.pools_checkbutton = ctk.CTkCheckBox(
            self,
            variable=self.display_pools_status,
            onvalue=True,
            offvalue=False,
            text=CompareCommandFrameParams.DISPLAY_POOLS,
        )
        self.pools_checkbutton.grid(row=1, column=1, padx=10, pady=(0, 5), sticky="n")

        clear_button = ctk.CTkButton(
            self, width=600, height=32, text=CompareCommandFrameParams.CLEAR_BUTTON_TEXT, command=self.clear_fields
        )
        clear_button.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="nsew")

        self.right_separator_label = ctk.CTkLabel(self, text=CompareCommandFrameParams.RIGHT_SEPARATOR)
        self.right_separator_label.grid(row=0, column=2, padx=10, pady=(5, 0), sticky="s")
        self.right_separator_entry = ctk.CTkEntry(self, height=32)
        self.right_separator_entry.grid(row=1, column=2, padx=10, pady=(0, 5), sticky="n")
