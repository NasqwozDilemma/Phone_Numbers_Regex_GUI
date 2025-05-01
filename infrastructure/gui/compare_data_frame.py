import tkinter as tk

import customtkinter as ctk
from constants.constants import ErrorsParams
from constants.constants import CompareDataFrameParams


class CompareDataFrame(ctk.CTkFrame):
    """
    Фрейм с элементами для данных для сравнения регулярных выражений.
    """  # noqa: RUF002

    def __init__(self, parent):
        super().__init__(parent, fg_color="whitesmoke")
        self.pack(padx=20, pady=10, fill="both")
        self.parent = parent

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.create_elements()

    def copy_text(self, field):
        try:
            text = field.get("sel.first", "sel.last")
            self.parent.master.master.clipboard_clear()
            self.parent.master.master.parent.clipboard_append(text)
            self.parent.master.master.parent.update()
        except Exception as e:
            self.parent.master.master.gui_adapter.show_error(message=ErrorsParams.ERROR_COPY_TEXT)
            raise e

    def paste_text(self, field):
        try:
            text = self.parent.master.master.clipboard_get()
            if field.tag_ranges("sel"):
                field.delete("sel.first", "sel.last")
            field.insert("insert", text)
        except Exception as e:
            self.parent.master.master.gui_adapter.show_error(message=ErrorsParams.ERROR_PASTE_TEXT)
            raise e

    def cut_text(self, field):
        try:
            self.copy_text(field)
            field.delete("sel.first", "sel.last")
        except Exception as e:
            self.parent.master.master.gui_adapter.show_error(message=ErrorsParams.ERROR_CUT_TEXT)
            raise e

    def undo_text(self, field):
        try:
            field.edit_undo()
        except Exception as e:
            self.parent.master.master.gui_adapter.show_error(message=ErrorsParams.ERROR_UNDO_TEXT)
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
        self.left_regexp_label = ctk.CTkLabel(self, text=CompareDataFrameParams.LEFT_REGEXP)
        self.left_regexp_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="s")
        self.left_regexp_text = ctk.CTkTextbox(self, font=("", 14), wrap=tk.WORD, height=450, width=800, undo=True)
        self.left_regexp_text.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="n")
        self.bind_events(self.left_regexp_text, self.left_regexp_text)

        self.right_regexp_label = ctk.CTkLabel(self, text=CompareDataFrameParams.RIGHT_REGEXP)
        self.right_regexp_label.grid(row=0, column=1, padx=10, pady=(5, 0), sticky="s")
        self.right_regexp_text = ctk.CTkTextbox(self, font=("", 14), wrap=tk.WORD, height=450, width=800, undo=True)
        self.right_regexp_text.grid(row=1, column=1, padx=10, pady=(0, 20), sticky="n")
        self.bind_events(self.right_regexp_text, self.right_regexp_text)

        self.left_result_label = ctk.CTkLabel(self, text=CompareDataFrameParams.LEFT_RESULT)
        self.left_result_label.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="s")
        self.left_result_text = ctk.CTkTextbox(self, font=("", 14), wrap=tk.WORD, height=125, width=800, undo=True)
        self.left_result_text.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="n")
        self.bind_events(self.left_result_text, self.left_result_text)

        self.right_result_label = ctk.CTkLabel(self, text=CompareDataFrameParams.RIGHT_RESULT)
        self.right_result_label.grid(row=2, column=1, padx=10, pady=(5, 0), sticky="s")
        self.right_result_text = ctk.CTkTextbox(self, font=("", 14), wrap=tk.WORD, height=125, width=800, undo=True)
        self.right_result_text.grid(row=3, column=1, padx=10, pady=(0, 20), sticky="n")
        self.bind_events(self.right_result_text, self.right_result_text)
