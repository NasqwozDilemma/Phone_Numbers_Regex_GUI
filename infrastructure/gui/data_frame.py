import tkinter as tk

import customtkinter as ctk
from constants.constants import ErrorsParams
from constants.constants import DataFrameParams


class DataFrame(ctk.CTkFrame):
    """
    Фрейм с элементами для данных.
    """  # noqa: RUF002

    def __init__(self, parent):
        super().__init__(parent, fg_color="whitesmoke")
        self.pack(padx=20, pady=10, fill="both")
        self.parent = parent

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.create_elements()

    def copy_text(self, field):
        try:
            text = field.get("sel.first", "sel.last")
            self.parent.parent.clipboard_clear()
            self.parent.parent.clipboard_append(text)
            self.parent.parent.update()
        except Exception as e:
            self.parent.gui_adapter.show_error(message=ErrorsParams.ERROR_COPY_TEXT)
            raise e

    def paste_text(self, field):
        try:
            text = self.parent.parent.clipboard_get()
            if field.tag_ranges("sel"):
                field.delete("sel.first", "sel.last")
            field.insert("insert", text)
        except Exception as e:
            self.parent.gui_adapter.show_error(message=ErrorsParams.ERROR_PASTE_TEXT)
            raise e

    def cut_text(self, field):
        try:
            self.copy_text(field)
            field.delete("sel.first", "sel.last")
        except Exception as e:
            self.parent.gui_adapter.show_error(message=ErrorsParams.ERROR_CUT_TEXT)
            raise e

    def undo_text(self, field):
        try:
            field.edit_undo()
        except Exception as e:
            self.parent.gui_adapter.show_error(message=ErrorsParams.ERROR_UNDO_TEXT)
            raise e

    def on_ctrl_key(self, event, field):
        if event.keycode == 67:  # Ctrl+C
            self.copy_text(field)
            return "break"
        elif event.keycode == 86:  # Ctrl+V
            self.paste_text(field)
            return "break"
        elif event.keycode == 88:  # Ctrl+X
            self.cut_text(field)
            return "break"
        elif event.keycode == 90:  # Ctrl+Z
            self.undo_text(field)
            return "break"

    def bind_events(self, widget, field):
        widget.bind("<Control-Key>", lambda e: self.on_ctrl_key(e, field))

    def create_elements(self):
        self.pools_label = ctk.CTkLabel(self, text=DataFrameParams.POOL)
        self.pools_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="s")
        self.pools_text = ctk.CTkTextbox(self, font=("", 14), wrap=tk.WORD, height=625, width=800, undo=True)
        self.pools_text.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="n")
        self.bind_events(self.pools_text, self.pools_text)

        self.regexp_label = ctk.CTkLabel(self, text=DataFrameParams.REGEXP)
        self.regexp_label.grid(row=0, column=1, padx=10, pady=(5, 0), sticky="s")
        self.regexp_text = ctk.CTkTextbox(self, font=("", 14), wrap=tk.WORD, height=625, width=800, undo=True)
        self.regexp_text.grid(row=1, column=1, padx=10, pady=(0, 20), sticky="n")
        self.bind_events(self.regexp_text, self.regexp_text)
