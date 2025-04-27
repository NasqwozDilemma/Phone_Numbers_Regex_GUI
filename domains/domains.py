from dataclasses import dataclass


@dataclass
class PhoneNumbersData:
    def __init__(self, data_list: list):
        self.data_list = data_list
