import customtkinter as ctk

from infrastructure.gui.command_frame import CommandFrame
from infrastructure.gui.compare_data_frame import CompareDataFrame
from infrastructure.gui.compare_command_frame import CompareCommandFrame
from infrastructure.gui.data_frame import DataFrame
from interface_adapters.gui_adapters.gui_adapter import GUIAdapter


class MainFrame(ctk.CTkFrame):
    """
    Основной фрейм.
    """

    def __init__(self, parent, gui_adapter: GUIAdapter):
        super().__init__(parent, fg_color="white")
        self.pack(fill="both", expand=True)
        self.parent = parent
        self.gui_adapter = gui_adapter

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=0, pady=0)

        self.tabview.add("Преобразование")
        self.tabview.add("Сравнение")
        self.tabview.set("Преобразование")

        self.data_frame = DataFrame(self.tabview.tab("Преобразование"))
        self.command_frame = CommandFrame(self.tabview.tab("Преобразование"), self.gui_adapter)
        self.compare_data_frame = CompareDataFrame(self.tabview.tab("Сравнение"))
        self.compare_command_frame = CompareCommandFrame(self.tabview.tab("Сравнение"), self.gui_adapter)
