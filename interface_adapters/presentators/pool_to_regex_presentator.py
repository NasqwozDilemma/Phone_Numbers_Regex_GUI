from constants.constants import ErrorsParams
from domains.domains import PhoneNumbersData


class RegexPresentator:
    def __init__(self):
        pass

    def regex_sort_key(self, regex: str) -> tuple:
        def parse_digit_class(class_str: str) -> set:
            """
            Извлекает все допустимые цифры из строки внутри квадратных скобок.
            """
            allowed = set()

            i = 0
            while i < len(class_str):
                if (
                    i + 2 < len(class_str)
                    and class_str[i].isdigit()
                    and class_str[i + 1] == "-"
                    and class_str[i + 2].isdigit()
                ):
                    start = int(class_str[i])
                    end = int(class_str[i + 2])
                    allowed.update(range(start, end + 1))
                    i += 3
                elif class_str[i].isdigit():
                    allowed.add(int(class_str[i]))
                    i += 1
                else:
                    i += 1
            return allowed

        regex = regex.strip("^$")
        result = []

        i = 0
        while i < len(regex):
            if regex[i] == "[":
                j = regex.find("]", i)
                if j == -1:
                    i += 1
                    continue
                class_content = regex[i + 1 : j]
                allowed = parse_digit_class(class_content)
                min_digit = min(allowed) if allowed else 0
                if j + 1 < len(regex) and regex[j + 1] == "{":
                    k = regex.find("}", j + 1)
                    if k != -1:
                        try:
                            quantifier = int(regex[j + 2 : k])
                        except ValueError:
                            quantifier = 1
                        result.extend([min_digit] * quantifier)
                        i = k + 1
                        continue
                # Если квантификатора нет, считаем один символ
                result.append(min_digit)
                i = j + 1
            elif regex[i].isdigit():
                while i < len(regex) and regex[i].isdigit():
                    result.append(int(regex[i]))
                    i += 1
            else:
                i += 1
        return tuple(result)

    def prepare_data(self, phone_numbers_data: PhoneNumbersData, separator: str):
        try:
            prepared_data = sorted(set(phone_numbers_data.data_list), key=self.regex_sort_key)
        except Exception as e:
            raise Exception(ErrorsParams.ERROR_PREPARE_REGEX) from e
        else:
            return f"{separator}".join(prepared_data)
