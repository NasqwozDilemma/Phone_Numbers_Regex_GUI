from constants.constants import ErrorsParams
from domains.domains import PhoneNumbersData


class PoolPresentator:
    def __init__(self):
        pass

    def prepare_data(self, phone_numbers_data: PhoneNumbersData):
        try:
            result = ", ".join(phone_numbers_data.data_list)
        except Exception as e:
            raise Exception(ErrorsParams.ERROR_PREPARE_POOLS) from e
        else:
            return result
