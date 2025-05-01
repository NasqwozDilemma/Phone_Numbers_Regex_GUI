from icecream import ic

from constants.constants import ErrorsParams


class RegexController:
    def __init__(self):
        pass

    def prepare_data(self, data: str, separator: str):
        ic("---------------------------------")
        ic("REGEX TO POOLS")
        ic("---------------------------------")
        try:
            regexes = data.split(separator)
        except Exception as e:
            raise Exception(ErrorsParams.ERROR_REGEX_VALIDATE) from e
        else:
            ic(regexes)
            return regexes
