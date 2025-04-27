import tkinter.messagebox as messagebox

from constants.constants import ErrorsParams


class GUIAdapter:
    def __init__(self, parent):
        self.parent = parent

    def show_askyesno(self, title, message) -> bool:
        answer = messagebox.askyesno(title, message)
        return answer

    def show_error(self, title=ErrorsParams.ERROR_WINDOW_NAME, message="Error"):
        messagebox.showerror(title, message)
