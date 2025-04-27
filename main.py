import multiprocessing
import os

from icecream import ic
# from icecream import install

from infrastructure.gui.main_window import App


# install()
# ic.configureOutput(includeContext=True)
# ic.configureOutput(contextAbsPath=True)
ic.disable()


def main():
    App()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
    os._exit(1)
