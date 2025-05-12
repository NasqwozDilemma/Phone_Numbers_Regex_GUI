import re

from icecream import ic

from constants.constants import ErrorsParams, SpecialSymbolsParams
from domains.domains import PhoneNumbersData


class RegexManager:
    def __init__(self):
        pass

    def regex_from_all_nulls(
        self, common_prefix: str, start_suffix: str, end_suffix: str, caret_symbol: str, dollar_symbol: str
    ):
        """Преобразует диапазон номеров, начинающийся с нулей, в регулярное выражение."""  # noqa: RUF002
        regex_parts = []
        for i in range(len(end_suffix)):
            if len(end_suffix[i:]) == 1:
                if start_suffix[i] == end_suffix[i]:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{end_suffix[0:i]}"
                        f"{start_suffix[i]}{dollar_symbol}"
                    )
                else:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{end_suffix[0:i]}"
                        f"[{int(start_suffix[i])}-{int(end_suffix[i])}]{dollar_symbol}"
                    )
            else:
                if start_suffix[i] == end_suffix[i]:
                    continue
                elif len(end_suffix[i:]) - 1 == 1:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{end_suffix[0:i]}"
                        f"[{int(start_suffix[i])}-{int(end_suffix[i]) - 1}][0-9]{dollar_symbol}"
                    )
                elif int(start_suffix[i]) == int(end_suffix[i]) - 1:
                    if f"{{{len(end_suffix[i:]) - 1}}}" == "{1}":
                        regex_parts.append(
                            f"{caret_symbol}{re.escape(common_prefix)}"
                            f"{end_suffix[0:i]}"
                            f"{int(start_suffix[i])}"
                            f"[0-9]{dollar_symbol}"
                        )
                    else:
                        regex_parts.append(
                            f"{caret_symbol}{re.escape(common_prefix)}"
                            f"{end_suffix[0:i]}"
                            f"{int(start_suffix[i])}"
                            f"[0-9]{{{len(end_suffix[i:]) - 1}}}{dollar_symbol}"
                        )
                else:
                    if f"{{{len(end_suffix[i:]) - 1}}}" == "{1}":
                        regex_parts.append(
                            f"{caret_symbol}{re.escape(common_prefix)}"
                            f"{end_suffix[0:i]}"
                            f"[{int(start_suffix[i])}-{int(end_suffix[i]) - 1}]"
                            f"[0-9]{dollar_symbol}"
                        )
                    else:
                        regex_parts.append(
                            f"{caret_symbol}{re.escape(common_prefix)}"
                            f"{end_suffix[0:i]}"
                            f"[{int(start_suffix[i])}-{int(end_suffix[i]) - 1}]"
                            f"[0-9]{{{len(end_suffix[i:]) - 1}}}{dollar_symbol}"
                        )
        return regex_parts

    def regex_to_all_nines(
        self, common_prefix: str, start_suffix: str, end_suffix: str, caret_symbol: str, dollar_symbol: str
    ):
        """Преобразует диапазон номеров, заканчивающийся на девятки,
        в регулярное выражение."""
        internal_end_suffix_all_nulls_temp = False
        for i in end_suffix[1:]:
            if int(i) == 0:
                internal_end_suffix_all_nulls_temp = True
            else:
                internal_end_suffix_all_nulls_temp = False
                break
        new_common_prefix = f"{common_prefix}{start_suffix[0]}"
        new_start_suffix = f"{start_suffix[1:]}"
        new_end_suffix = f'{"9" * (len(end_suffix[1:]))}'
        regex_parts = []
        for i in range(len(new_start_suffix) - 1, -1, -1):
            if len(new_start_suffix[i:]) == 1:
                regex_parts.append(
                    f"{caret_symbol}{re.escape(new_common_prefix)}"
                    f"{new_start_suffix[0:i]}"
                    f"[{int(new_start_suffix[i])}-9]{dollar_symbol}"
                )
                ic(1)
                ic(regex_parts)
            elif len(new_start_suffix[i:]) - 1 == 1:
                regex_parts.append(
                    f"{caret_symbol}{re.escape(new_common_prefix)}"
                    f"{new_start_suffix[0:i]}"
                    f"[{int(new_start_suffix[i]) + 1}-9][0-9]{dollar_symbol}"
                )
                ic(2)
                ic(regex_parts)
            else:
                if f"{{{len(new_start_suffix) - 1}}}" == "{1}":
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(start_suffix[:i])}"
                        f"{str(int(start_suffix[i]))}"
                        f"[{int(new_start_suffix[i]) + 1}-"
                        f"{int(new_end_suffix[i])}]"
                        f"[0-9]{dollar_symbol}"
                    )
                    ic(3)
                    ic(regex_parts)
                else:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(start_suffix[:i])}"
                        f"{str(int(start_suffix[i]))}"
                        f"[{int(new_start_suffix[i]) + 1}-"
                        f"{int(new_end_suffix[i])}]"
                        f"[0-9]{{{len(new_start_suffix) - i - 1}}}{dollar_symbol}"
                    )
                    ic(4)
                    ic(new_start_suffix)
                    ic(regex_parts)
        digits_count = int(end_suffix[0]) - int(start_suffix[0])
        if internal_end_suffix_all_nulls_temp is True:
            for i in range(digits_count - 1):
                if f"{{{len(end_suffix[1:])}}}" == "{1}":
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(int(start_suffix[0]) + i + 1)}"
                        f"[0-9]{dollar_symbol}"
                    )
                    ic(5)
                    ic(regex_parts)
                else:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(int(start_suffix[0]) + i + 1)}"
                        f"[0-9]{{{len(end_suffix[1:])}}}{dollar_symbol}"
                    )
                    ic(6)
                    ic(regex_parts)
        else:
            for i in range(digits_count):
                if f"{{{len(end_suffix[1:])}}}" == "{1}":
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(int(start_suffix[0]) + i + 1)}"
                        f"[0-9]{dollar_symbol}"
                    )
                    ic(7)
                    ic(regex_parts)
                else:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(int(start_suffix[0]) + i + 1)}"
                        f"[0-9]{{{len(end_suffix[1:])}}}{dollar_symbol}"
                    )
                    ic(8)
                    ic(regex_parts)
        return regex_parts

    def range_to_regex(self, start: str, end: str, separator: str, caret_symbol: str, dollar_symbol: str):
        """Преобразует диапазон номеров в регулярное выражение."""
        start_suffix_all_nulls = False
        internal_start_suffix_all_nulls = False
        internal_start_suffix_all_nines = False
        internal_end_suffix_all_nulls = False
        internal_end_suffix_all_nines = False
        end_suffix_all_nines = False
        all_internal_suffix_all_nulls = False
        two_character_number = False

        if start == end:
            return f"{caret_symbol}{re.escape(start)}{dollar_symbol}"

        regex_parts = []
        common_prefix = ""
        for i in range(len(start)):
            if start[i] == end[i]:
                common_prefix += start[i]
            else:
                break

        ic(common_prefix)
        start_suffix = start[len(common_prefix) :]
        ic(start_suffix)
        end_suffix = end[len(common_prefix) :]
        ic(end_suffix)

        # 'start_suffix_all_nulls'
        for i in start_suffix:
            if int(i) == 0:
                start_suffix_all_nulls = True
            else:
                start_suffix_all_nulls = False
                break
        ic(start_suffix_all_nulls)

        # 'internal_start_suffix_all_nulls'
        for i in start_suffix[1:]:
            if int(i) == 0:
                internal_start_suffix_all_nulls = True
            else:
                internal_start_suffix_all_nulls = False
                break
        ic(internal_start_suffix_all_nulls)

        # 'internal_start_suffix_all_nines'
        for i in start_suffix[1:]:
            if int(i) == 9:
                internal_start_suffix_all_nines = True
            else:
                internal_start_suffix_all_nines = False
                break
        ic(internal_start_suffix_all_nines)

        # 'end_suffix_all_nines'
        for i in end_suffix:
            if int(i) == 9:
                end_suffix_all_nines = True
            else:
                end_suffix_all_nines = False
                break
        ic(end_suffix_all_nines)

        # 'internal_end_suffix_all_nulls'
        for i in end_suffix[1:]:
            if int(i) == 0:
                internal_end_suffix_all_nulls = True
            else:
                internal_end_suffix_all_nulls = False
                break
        ic(internal_end_suffix_all_nulls)

        # 'internal_end_suffix_all_nines'
        for i in end_suffix[1:]:
            if int(i) == 9:
                internal_end_suffix_all_nines = True
            else:
                internal_end_suffix_all_nines = False
                break
        ic(internal_end_suffix_all_nines)

        # 'all_internal_suffix_all_nulls'
        if start_suffix[1:] == end_suffix[1:]:
            for i in start_suffix[1:]:
                if int(i) == 0:
                    all_internal_suffix_all_nulls = True
                else:
                    all_internal_suffix_all_nulls = False
                    break
            ic(all_internal_suffix_all_nulls)

        # 'two_character_number'
        if len(start) == 2:
            two_character_number = True
        ic(two_character_number)

        # 'two_character_number'
        if two_character_number:
            ic("two_character_number")
            regex_parts.append(
                f"{caret_symbol}{re.escape(common_prefix)}"
                f"[{int(start_suffix[0])}-{int(end_suffix[0])}]{dollar_symbol}"
            )
            return f"{separator}".join(regex_parts)

        # '000 000'
        if all_internal_suffix_all_nulls:
            ic("000 000")
            digits_count = int(end_suffix[0]) - int(start_suffix[0])
            for i in range(digits_count):
                if f"{{{len(start_suffix[1:])}}}" == f"{{{1}}}":
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}{str(int(start_suffix[0]) + i)}"
                        f"[0-9]{dollar_symbol}"
                    )
                else:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}{str(int(start_suffix[0]) + i)}"
                        f"[0-9]{{{len(start_suffix[1:])}}}{dollar_symbol}"
                    )
            regex_parts.append(
                f"{caret_symbol}{re.escape(common_prefix)}{end_suffix[0]}{start_suffix[1:]}{dollar_symbol}"
            )
            return f"{separator}".join(regex_parts)

        # '000 999'
        if start_suffix_all_nulls and end_suffix_all_nines:
            ic("000 999")
            if f"{{{len(start_suffix)}}}" == f"{{{1}}}":
                regex_parts.append(f"{caret_symbol}{re.escape(common_prefix)}[0-9]{dollar_symbol}")
            else:
                regex_parts.append(
                    f"{caret_symbol}{re.escape(common_prefix)}[0-9]{{{len(start_suffix)}}}{dollar_symbol}"
                )
            return f"{separator}".join(regex_parts)

        # 'internal 000 internal 999'
        if internal_start_suffix_all_nulls and internal_end_suffix_all_nines:
            ic("internal 000 internal 999")
            digits_count = int(end_suffix[0]) - int(start_suffix[0])
            for i in range(digits_count + 1):
                new_common_prefix = f"{common_prefix}{int(start_suffix[0]) + i}"
                new_start_suffix = f'{"0" * len(start_suffix[1:])}'
                new_end_suffix = f'{"9" * len(end_suffix[1:])}'
                if f"{{{len(new_start_suffix)}}}" == f"{{{1}}}":
                    regex_parts.append(f"{caret_symbol}{re.escape(new_common_prefix)}[0-9]{dollar_symbol}")
                else:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(new_common_prefix)}[0-9]"
                        f"{{{len(new_start_suffix)}}}{dollar_symbol}"
                    )
            return f"{separator}".join(regex_parts)

        # '000 ___'
        if start_suffix_all_nulls or internal_start_suffix_all_nulls:
            ic("000 ___")
            regex_parts.extend(
                self.regex_from_all_nulls(common_prefix, start_suffix, end_suffix, caret_symbol, dollar_symbol)
            )
            return f"{separator}".join(regex_parts)

        # '999 000'
        if internal_start_suffix_all_nines and internal_end_suffix_all_nulls:
            ic("999 000")
            regex_parts.append(
                f"{caret_symbol}{re.escape(common_prefix)}{start_suffix[0]}{start_suffix[1:]}{dollar_symbol}"
            )
            new_common_prefix = f"{common_prefix}{end_suffix[0]}"
            new_start_suffix = f'{"0" * len(start_suffix[1:])}'
            new_end_suffix = f"{end_suffix[1:]}"
            digits_count = int(end_suffix[0]) - int(start_suffix[0]) - 1
            for i in range(digits_count):
                if f"{{{len(start_suffix[1:])}}}" == f"{{{1}}}":
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(int(start_suffix[0]) + i + 1)}"
                        f"[0-9]{dollar_symbol}"
                    )
                else:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(int(start_suffix[0]) + i + 1)}"
                        f"[0-9]{{{len(start_suffix[1:])}}}{dollar_symbol}"
                    )
            regex_parts.append(
                f"{caret_symbol}{re.escape(common_prefix)}{end_suffix[0]}{end_suffix[1:]}{dollar_symbol}"
            )
            return f"{separator}".join(regex_parts)

        # '999 999'
        if internal_start_suffix_all_nines and internal_end_suffix_all_nines:
            ic("999 999")
            regex_parts.append(
                f"{caret_symbol}{re.escape(common_prefix)}{start_suffix[0]}{start_suffix[1:]}{dollar_symbol}"
            )
            new_common_prefix = f"{common_prefix}{end_suffix[0]}"
            new_start_suffix = f'{"0" * len(start_suffix[1:])}'
            new_end_suffix = f"{end_suffix[1:]}"
            digits_count = int(end_suffix[0]) - int(start_suffix[0])
            for i in range(digits_count):
                if f"{{{len(end_suffix[1:])}}}" == f"{{{1}}}":
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(int(start_suffix[0]) + i + 1)}"
                        f"[0-9]{dollar_symbol}"
                    )
                else:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{str(int(start_suffix[0]) + i + 1)}"
                        f"[0-9]{{{len(end_suffix[1:])}}}{dollar_symbol}"
                    )
            return f"{separator}".join(regex_parts)

        # '999 ___'
        if internal_start_suffix_all_nines:
            ic("999 ___")
            regex_parts.append(
                f"{caret_symbol}{re.escape(common_prefix)}{start_suffix[0]}{start_suffix[1:]}{dollar_symbol}"
            )
            new_common_prefix = f"{common_prefix}{end_suffix[0]}"
            new_start_suffix = f'{"0" * len(start_suffix[1:])}'
            new_end_suffix = f"{end_suffix[1:]}"
            regex_parts.extend(
                self.regex_from_all_nulls(
                    new_common_prefix, new_start_suffix, new_end_suffix, caret_symbol, dollar_symbol
                )
            )
            return f"{separator}".join(regex_parts)

        # '___ 000'
        if not start_suffix_all_nulls and internal_end_suffix_all_nulls:
            ic("___ 000")
            regex_parts.extend(
                self.regex_to_all_nines(common_prefix, start_suffix, end_suffix, caret_symbol, dollar_symbol)
            )
            regex_parts.append(
                f'{caret_symbol}{re.escape(common_prefix)}{end_suffix[0]}'
                f'{"0" * (len(end_suffix[1:]))}{dollar_symbol}'
            )
            return f"{separator}".join(regex_parts)

        # '___ 999'
        if (
            not internal_start_suffix_all_nulls
            and not internal_start_suffix_all_nines
            and internal_end_suffix_all_nines
        ):
            ic("___ 999")
            regex_parts.extend(
                self.regex_to_all_nines(common_prefix, start_suffix, end_suffix, caret_symbol, dollar_symbol)
            )
            return f"{separator}".join(regex_parts)

        # '___ ___'
        if not start_suffix_all_nulls:
            ic("___ ___")
            for i in range(len(start_suffix) - 1, -1, -1):
                if len(start_suffix[i:]) == 1:
                    if len(start_suffix) == len(end_suffix) == 1:
                        if int(start_suffix[i]) == int(end_suffix[i]) - 1:
                            regex_parts.append(
                                f"{caret_symbol}{re.escape(common_prefix)}"
                                f"{start_suffix[0:i]}"
                                f"[{int(start_suffix[i])}{int(end_suffix[i])}]{dollar_symbol}"
                            )
                        else:
                            regex_parts.append(
                                f"{caret_symbol}{re.escape(common_prefix)}"
                                f"{start_suffix[0:i]}"
                                f"[{int(start_suffix[i])}-{int(end_suffix[i])}]{dollar_symbol}"
                            )
                    else:
                        regex_parts.append(
                            f"{caret_symbol}{re.escape(common_prefix)}"
                            f"{start_suffix[0:i]}"
                            f"[{int(start_suffix[i])}-9]{dollar_symbol}"
                        )
                elif len(start_suffix[i:]) - 1 == 1:
                    regex_parts.append(
                        f"{caret_symbol}{re.escape(common_prefix)}"
                        f"{start_suffix[0:i]}"
                        f"[{int(start_suffix[i]) + 1}-9][0-9]{dollar_symbol}"
                    )
                elif len(start_suffix[i:]) < len(start_suffix):
                    if f"{{{len(start_suffix) - i - 1}}}" == f"{{{1}}}":
                        regex_parts.append(
                            f"{caret_symbol}{re.escape(common_prefix)}"
                            f"{start_suffix[0:i]}"
                            f"[{int(start_suffix[i]) + 1}-9]"
                            f"[0-9]{dollar_symbol}"
                        )
                    else:
                        regex_parts.append(
                            f"{caret_symbol}{re.escape(common_prefix)}"
                            f"{start_suffix[0:i]}"
                            f"[{int(start_suffix[i]) + 1}-9]"
                            f"[0-9]{{{len(start_suffix) - i - 1}}}{dollar_symbol}"
                        )
                else:
                    digits_count = int(end_suffix[0]) - int(start_suffix[0]) - 1
                    for i in range(digits_count):
                        if f"{{{len(start_suffix) - 1}}}" == f"{{{1}}}":
                            regex_parts.append(
                                f"{caret_symbol}{re.escape(common_prefix)}"
                                f"{int(start_suffix[0]) + i + 1}"
                                f"[0-9]{dollar_symbol}"
                            )
                        else:
                            regex_parts.append(
                                f"{caret_symbol}{re.escape(common_prefix)}"
                                f"{int(start_suffix[0]) + i + 1}"
                                f"[0-9]{{{len(start_suffix) - 1}}}{dollar_symbol}"
                            )
                    new_start = f"{common_prefix}{end_suffix[0]}{'0' * (len(end_suffix[1:]))}"
                    new_end = f"{common_prefix}{end_suffix}"
                    regex_parts.append(self.range_to_regex(new_start, new_end, separator, caret_symbol, dollar_symbol))
        return f"{separator}".join(regex_parts)

    def pools_to_regex(self, phone_numbers_data: PhoneNumbersData, separator: str, unuse_special_symbols: bool):
        """
        Основная функция для преобразования пулов телефонных номеров
        в строку регулярного выражения.
        """

        try:
            if unuse_special_symbols is True:
                caret_symbol = ""
                dollar_symbol = ""
            else:
                caret_symbol = SpecialSymbolsParams.CARET
                dollar_symbol = SpecialSymbolsParams.DOLLAR

            ic(phone_numbers_data.data_list)
            regex_list = [
                self.range_to_regex(start, end, separator, caret_symbol, dollar_symbol)
                for start, end in phone_numbers_data.data_list
            ]
            ic(regex_list)

            split_regex_list = []
            for element in regex_list:
                split_regex_list.extend(element.split(separator))
            ic(split_regex_list)

            phone_numbers_data.data_list = split_regex_list
        except Exception as e:
            raise Exception(ErrorsParams.ERROR_CONVERT_TO_REGEX) from e
        else:
            return phone_numbers_data
