import customtkinter as ctk

from infrastructure.gui.command_frame import CommandFrame
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

        self.dataframe = DataFrame(self)
        self.commandframe = CommandFrame(self, self.gui_adapter)
