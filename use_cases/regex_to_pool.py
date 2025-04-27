import itertools
import re
from concurrent.futures import ProcessPoolExecutor, as_completed

from icecream import ic

from constants.constants import ErrorsParams
from domains.domains import PhoneNumbersData


class PoolManager:
    def __init__(self):
        pass

    @staticmethod
    def generate_numbers_static(regex: str) -> list:
        """
        Генерация номеров из регулярного выражения.
        Если обнаружен набор цифр, образующих непрерывный диапазон (например: 1, 2, 3, 4),
        то для каждого префикса вместо перебора всех вариантов создаётся интервал вида (min, max).
        """
        ic("---------------------------------")
        ic("Регулярное выражение:", regex)
        if re.search(r"[a-zA-Zа-яА-ЯёЁ]", regex):
            raise ValueError(f"Некорректное выражение: {regex}")

        cleaned_regex = regex.strip("^$")
        regex_parts_pattern = r"\d|\[\d[-\d]*\]|\.|\{\d+(?:,\d+)?\}"
        regex_parts = re.findall(regex_parts_pattern, cleaned_regex)
        ic("Части регулярки:", regex_parts)

        # Определяем индексы, где присутствует {n} или {m,n}
        repeat_quantifier_indexes = {
            index for index, part in enumerate(regex_parts) if part.startswith("{") and part.endswith("}")
        }

        number_list = []

        for part_index, regex_part in enumerate(regex_parts):
            if regex_part.startswith("{") and regex_part.endswith("}"):
                continue

            # Если список префиксов пуст (например, регулярка начинается не с одиночной цифры),
            # инициализируем его пустой строкой
            if not number_list:
                number_list = [""]

            if len(regex_part) == 1 and regex_part != ".":
                # Обработка одиночных цифр
                updated_number_list = []
                for current_prefix in number_list:
                    if isinstance(current_prefix, tuple):
                        updated_number_list.append((current_prefix[0] + regex_part, current_prefix[1] + regex_part))
                    else:
                        updated_number_list.append(current_prefix + regex_part)
                number_list = updated_number_list

            elif "[" in regex_part or "." in regex_part:
                # Обработка диапазона в квадратных скобках или точки (.)
                range_values = []
                if "." in regex_part:
                    range_values = [str(digit) for digit in range(10)]
                else:
                    bracket_content = regex_part.strip("[]")
                    if "-" in bracket_content:
                        value_pattern = r"\d-\d|\d"
                        parts_in_brackets = re.findall(value_pattern, bracket_content)
                        for part_item in parts_in_brackets:
                            if "-" in part_item:
                                start_digit, end_digit = part_item.split("-")
                                range_values.extend(
                                    [str(digit) for digit in range(int(start_digit), int(end_digit) + 1)]
                                )
                            else:
                                range_values.append(part_item)
                    else:
                        range_values = list(bracket_content)
                ic("Диапазоны значений:", range_values)
                updated_number_list = []

                if part_index + 1 in repeat_quantifier_indexes:
                    # Обработка повторов, например, [1-4]{2} или [1-4]{2,3}
                    repeat_specifier = regex_parts[part_index + 1].strip("{}")
                    if "," in repeat_specifier:
                        min_repeat, max_repeat = map(int, repeat_specifier.split(","))
                    else:
                        min_repeat = max_repeat = int(repeat_specifier)
                    numeric_values = sorted(set(int(value) for value in range_values))
                    is_contiguous = numeric_values == list(
                        range(numeric_values[0], numeric_values[0] + len(numeric_values))
                    )
                    for rep in range(min_repeat, max_repeat + 1):
                        if is_contiguous:
                            min_digit = str(numeric_values[0])
                            max_digit = str(numeric_values[-1])
                            for prefix in number_list:
                                if isinstance(prefix, tuple):
                                    updated_number_list.append(
                                        (
                                            prefix[0] + min_digit * rep,
                                            prefix[1] + max_digit * rep,
                                        )
                                    )
                                else:
                                    updated_number_list.append(
                                        (
                                            prefix + min_digit * rep,
                                            prefix + max_digit * rep,
                                        )
                                    )
                        else:
                            for prefix in number_list:
                                base_prefix = prefix[0] if isinstance(prefix, tuple) else prefix
                                for combination in itertools.product(range_values, repeat=rep):
                                    updated_number_list.append(base_prefix + "".join(combination))
                else:
                    # Обработка группы без повторения:
                    # Например, ^1[12]2$
                    for prefix in number_list:
                        base_prefix = prefix[0] if isinstance(prefix, tuple) else prefix
                        for value in range_values:
                            updated_number_list.append(base_prefix + value)
                number_list = updated_number_list

        return number_list

    def regex_to_pool(self, phone_numbers_data: PhoneNumbersData) -> PhoneNumbersData:
        """
        Преобразует список регулярных выражений в строку диапазонов номеров.
        Для ускорения генерации номеров выполняется параллельно при помощи ProcessPoolExecutor.
        """
        try:
            result_numbers = set()

            with ProcessPoolExecutor(max_workers=2) as executor:
                futures = {
                    executor.submit(PoolManager.generate_numbers_static, reg): reg
                    for reg in phone_numbers_data.data_list
                }
                for future in as_completed(futures):
                    try:
                        numbers = future.result()
                        result_numbers.update(numbers)
                    except Exception as e:
                        raise e
            ic(result_numbers)
            phone_numbers_data.data_list = list(result_numbers)
        except Exception as e:
            raise Exception(ErrorsParams.ERROR_CONVERT_TO_POOLS) from e
        else:
            return phone_numbers_data
