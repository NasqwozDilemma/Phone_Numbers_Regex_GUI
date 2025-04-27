from icecream import ic

from constants.constants import ErrorsParams
from domains.domains import PhoneNumbersData


class PoolOptimizer:
    def __init__(self):
        pass

    def merge_ranges_from_numbers(self, numbers: list) -> list:
        """
        Объединяет перекрывающиеся или соседние диапазоны.
        """

        if not numbers:
            return []

        interval_list = []
        for number_item in numbers:
            if isinstance(number_item, tuple):
                lower_str, upper_str = number_item
            else:
                lower_str = upper_str = number_item
            lower_int = int(lower_str)
            upper_int = int(upper_str)
            width = len(lower_str)
            interval_list.append((lower_int, upper_int, width))

        interval_list.sort(key=lambda interval: interval[0])
        merged_intervals = []

        current_lower_int, current_upper_int, current_width = interval_list[0]
        for interval in interval_list[1:]:
            next_lower_int, next_upper_int, next_width = interval
            if next_width != current_width:
                merged_intervals.append(
                    (str(current_lower_int).zfill(current_width), str(current_upper_int).zfill(current_width))
                )
                current_lower_int, current_upper_int, current_width = next_lower_int, next_upper_int, next_width
                continue

            # Объединяем только если следующий номер непосредственно последовательный
            if next_lower_int <= current_upper_int + 1:
                current_upper_int = max(current_upper_int, next_upper_int)
            else:
                merged_intervals.append(
                    (str(current_lower_int).zfill(current_width), str(current_upper_int).zfill(current_width))
                )
                current_lower_int, current_upper_int = next_lower_int, next_upper_int

        merged_intervals.append(
            (str(current_lower_int).zfill(current_width), str(current_upper_int).zfill(current_width))
        )
        return merged_intervals

    def execute_optimize(self, phone_numbers_data: PhoneNumbersData):
        try:
            merged_ranges = self.merge_ranges_from_numbers(phone_numbers_data.data_list)
            ic("Диапазоны после совмещения номеров:", merged_ranges)
            result_ranges = []
            for start, end in sorted(merged_ranges, key=lambda x: (len(x[0]), x[0], x[1])):
                if start == end:
                    result_ranges.append(start)
                elif int(start) == int(end) - 1:
                    result_ranges.append(start)
                    result_ranges.append(end)
                else:
                    result_ranges.append(f"{start} - {end}")
            phone_numbers_data.data_list = result_ranges
        except Exception as e:
            raise Exception(ErrorsParams.ERROR_OPTIMIZE_POOLS) from e
        else:
            return phone_numbers_data
