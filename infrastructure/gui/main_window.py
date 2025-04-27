import customtkinter as ctk

from constants.constants import MainWindowParams
from infrastructure.gui.main_frame import MainFrame
from interface_adapters.gui_adapters.gui_adapter import GUIAdapter


class WindowSettings:
    """
    Передача настроек главного окна в конструктор окна.
    """

    min_width_window = MainWindowParams.MIN_WIDTH
    min_height_window = MainWindowParams.MIN_HEIGHT
    window_icon = MainWindowParams.ICON_PATH
    can_resize_width = False
    can_resize_height = False


class WindowFactory:
    """
    Конструктор окна.
    """

    @staticmethod
    def create_window(window_settings, window_name):
        window = ctk.CTk()
        window.title(window_name)

        ctk.set_appearance_mode("Light")
        # Modes: 'System' (standard), 'Dark', 'Light'
        ctk.set_default_color_theme("dark-blue")
        # Themes: 'blue' (standard), 'green', 'dark-blue'

        if window_settings.min_width_window is not None and window_settings.min_height_window is not None:
            window.minsize(window_settings.min_width_window, window_settings.min_height_window)
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (window_settings.min_width_window / 2))
            y_cordinate = int((screen_height / 2) - (window_settings.min_height_window / 2))
            window.geometry(
                f"{window_settings.min_width_window}"
                f"x{window_settings.min_height_window}"
                f"+{x_cordinate}+{y_cordinate}"
            )

        if window_settings.window_icon is not None:
            window.iconbitmap(window_settings.window_icon)

        window.resizable(window_settings.can_resize_width, window_settings.can_resize_height)
        return window

    @staticmethod
    def destroy(window):
        window.destroy()


class App:
    """
    Главное окно.
    """

    def __init__(self):
        window_settings = WindowSettings()
        app = WindowFactory.create_window(window_settings, MainWindowParams.MAIN_WINDOW_NAME)

        self.gui_adapter = GUIAdapter(self)
        self.frame = MainFrame(app, self.gui_adapter)

        app.mainloop()
