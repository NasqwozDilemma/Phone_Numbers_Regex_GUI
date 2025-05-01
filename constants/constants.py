class MainWindowParams:
    MAIN_WINDOW_NAME = "Преобразование телефонных номеров в регулярные выражения"
    ICON_PATH = "./config/reg_exp.ico"
    MIN_WIDTH = 1800
    MIN_HEIGHT = 900


class ErrorsParams:
    ERROR_WINDOW_NAME = "Ошибка"
    ERROR_POOLS_VALIDATE = "Ошибка в веденных наборах телефонных номеров."
    ERROR_REGEX_VALIDATE = "Ошибка в веденных наборах регулярных выражений."
    ERROR_CONVERT_TO_POOLS = "Ошибка при преобразовании в телефонные номера."
    ERROR_CONVERT_TO_REGEX = "Ошибка при преобразовании в регулярные выражения."
    ERROR_OPTIMIZE_POOLS = "Ошибка при оптимизации телефонных номеров."
    ERROR_OPTIMIZE_REGEX = "Ошибка при оптимизации регулярных выражений."
    ERROR_PREPARE_POOLS = "Ошибка в конечной подготовке телефонных номеров."
    ERROR_PREPARE_REGEX = "Ошибка в конечной подготовке регулярных выражений."
    ERROR_COPY_TEXT = "Ошибка при копировании текста."
    ERROR_PASTE_TEXT = "Ошибка при вставке текста."
    ERROR_CUT_TEXT = "Ошибка при вырезании текста."
    ERROR_UNDO_TEXT = "Ошибка при отмене последней операции."


class DataFrameParams:
    POOL = "Номера телефонов (пулы номеров указываются через дефис, отделенный пробелами с двух сторон)"
    REGEXP = "Регулярные выражения"


class CommandFrameParams:
    COMMAND_POOL_TO_REGEXP_BUTTON = "Преобразовать в регулярные выражения"
    COMMAND_REGEXP_TO_POOL_BUTTON = "Преобразовать в номера"
    CLEAR_BUTTON_TEXT = "Очистка полей"
    SEPARATOR = "Разделитель"
    DOT = "Использовать точку вместо диапазона"
    SPECIAL_SYMBOLS = "Убрать специальные символы (^ и $)"


class CompareDataFrameParams:
    LEFT_REGEXP = "Регулярные выражения"
    RIGHT_REGEXP = "Регулярные выражения"
    LEFT_RESULT = "Отличия в первом регулярном выражении"
    RIGHT_RESULT = "Отличия во втором регулярном выражении"


class CompareCommandFrameParams:
    COMMAND_COMPARE_REGEXPS_BUTTON = "Сравнить регулярные выражения"
    CLEAR_BUTTON_TEXT = "Очистка полей"
    LEFT_SEPARATOR = "Разделитель в первом регулярном выражении"
    RIGHT_SEPARATOR = "Разделитель во втором регулярном выражении"
    DISPLAY_POOLS = "Отобразить различия в виде телефонных номеров"


class SpecialSymbolsParams:
    CARET = "^"
    DOLLAR = "$"
