import re
from collections import defaultdict
from typing import Optional

from icecream import ic

from constants.constants import ErrorsParams, SpecialSymbolsParams
from domains.domains import PhoneNumbersData


class RegexOptimizer:
    def __init__(self):
        pass

    def merge_similar_strings(self, patterns: list):
        """
        Оптимизирует список регулярных выражений.
        Для тех паттернов, где можно объединить выражения по диапазону при отличиях только в одном диапазоне цифр.
        Остальные выражения остаются без изменений.
        """

        grouped = defaultdict(list)

        unmatched = []
        for pattern in patterns:
            match = re.match(r"^(.*?)(\[\d+(?:-?\d+)?\])(.*)$", pattern)
            if match:
                prefix, bracket_content, suffix = match.groups()
                grouped[(prefix, suffix)].append(bracket_content)
            else:
                unmatched.append(pattern)

        new_unmatched = []
        for pattern in unmatched:
            merged = False
            for prefix, suffix in grouped.keys():
                if suffix is None:
                    continue
                if pattern.startswith(prefix) and pattern.endswith(suffix):
                    # Определяем "среднюю" часть – она должна быть ровно одной цифрой.
                    mid = pattern[len(prefix) : len(pattern) - len(suffix)] if suffix else pattern[len(prefix) :]
                    if re.fullmatch(r"\d", mid):
                        grouped[(prefix, suffix)].append(f"[{mid}]")
                        merged = True
                        break
            if not merged:
                new_unmatched.append(pattern)

        for pattern in new_unmatched:
            grouped[(pattern, None)].append(None)

        merged_patterns = []
        for (prefix, suffix), bracket_contents in grouped.items():
            range_values = []
            if None in bracket_contents:
                merged_patterns.append(prefix + (suffix or ""))
            else:
                for range_elem in bracket_contents:
                    range_elem = range_elem.strip("[]")
                    if "-" in range_elem:
                        start, end = range_elem.split("-")
                        range_values.extend([str(i) for i in range(int(start), int(end) + 1)])
                    else:
                        range_values.extend([str(i) for i in range_elem])
                range_values = sorted(set(range_values), key=lambda x: int(x))

                if not range_values:
                    merged_patterns.append(prefix + (suffix or ""))
                    continue

                ranges = [(range_values[0], range_values[0])]
                for number in range_values[1:]:
                    start, end = ranges[-1]
                    if int(number) == int(end) + 1:
                        ranges[-1] = (start, number)
                    else:
                        ranges.append((number, number))

                merged_digits = ""
                for range_elem in ranges:
                    if int(range_elem[0]) == int(range_elem[1]) - 1:
                        merged_digits += f"{range_elem[0]}{range_elem[1]}"
                    elif int(range_elem[0]) == int(range_elem[1]):
                        merged_digits += f"{range_elem[0]}"
                    else:
                        merged_digits += f"{range_elem[0]}-{range_elem[1]}"

                merged_patterns.append(f"{prefix}[{merged_digits}]{suffix}")

        return merged_patterns

    def merge_full_range_strings(self, patterns: list[str]) -> list[str]:
        """
        Оптимизирует список регулярных выражений.
        Для тех паттернов, где можно объединить выражения по полным диапазонам цифр.
        Остальные выражения остаются без изменений.
        """

        def compute_total_length(pat: str) -> int:
            """
            Подсчитывает количество цифр, которые матчатся паттерном.
            Например, '[0-9]{3}' считается за 3 цифры.
            """
            s = pat.strip("^$")
            length = 0
            i = 0
            while i < len(s):
                if s[i] == "[":
                    j = s.find("]", i)
                    if j == -1:
                        i += 1
                        continue
                    length += 1  # конструкция в квадратных скобках соответствует 1 цифре по умолчанию
                    i = j + 1
                    if i < len(s) and s[i] == "{":
                        k = s.find("}", i)
                        if k != -1:
                            try:
                                count = int(s[i + 1 : k])
                            except ValueError:
                                count = 1
                            length += count - 1
                            i = k + 1
                elif s[i].isdigit():
                    length += 1
                    i += 1
                else:
                    i += 1
            return length

        def compute_min_full(pat: str) -> str:
            """
            Вычисляет минимальное число (строку цифр), которое может матчиться паттерном.
            Для конструкции вида [X-Y] выбирается минимальная цифра (X).
            Если после скобок идёт квантификатор, то выбранная цифра повторяется нужное число раз.
            """
            s = pat.strip("^$")
            res = ""
            i = 0
            while i < len(s):
                if s[i] == "[":
                    j = s.find("]", i)
                    if j == -1:
                        i += 1
                        continue
                    content = s[i + 1 : j]
                    digits = []
                    k = 0
                    while k < len(content):
                        if (
                            k + 2 < len(content)
                            and content[k].isdigit()
                            and content[k + 1] == "-"
                            and content[k + 2].isdigit()
                        ):
                            digits.append(int(content[k]))  # минимальное значение диапазона
                            k += 3
                        elif content[k].isdigit():
                            digits.append(int(content[k]))
                            k += 1
                        else:
                            k += 1
                    min_digit = str(min(digits)) if digits else "0"
                    res += min_digit
                    i = j + 1
                    if i < len(s) and s[i] == "{":
                        k = s.find("}", i)
                        if k != -1:
                            try:
                                count = int(s[i + 1 : k])
                            except ValueError:
                                count = 1
                            res += min_digit * (count - 1)
                            i = k + 1
                elif s[i].isdigit():
                    res += s[i]
                    i += 1
                else:
                    i += 1
            return res

        def compute_max_full(pat: str) -> str:
            """
            Аналогично compute_min_full, но выбирается максимальная цифра для каждого диапазона.
            """
            s = pat.strip("^$")
            res = ""
            i = 0
            while i < len(s):
                if s[i] == "[":
                    j = s.find("]", i)
                    if j == -1:
                        i += 1
                        continue
                    content = s[i + 1 : j]
                    digits = []
                    k = 0
                    while k < len(content):
                        if (
                            k + 2 < len(content)
                            and content[k].isdigit()
                            and content[k + 1] == "-"
                            and content[k + 2].isdigit()
                        ):
                            digits.append(int(content[k + 2]))  # максимальное значение диапазона
                            k += 3
                        elif content[k].isdigit():
                            digits.append(int(content[k]))
                            k += 1
                        else:
                            k += 1
                    max_digit = str(max(digits)) if digits else "9"
                    res += max_digit
                    i = j + 1
                    if i < len(s) and s[i] == "{":
                        k = s.find("}", i)
                        if k != -1:
                            try:
                                count = int(s[i + 1 : k])
                            except ValueError:
                                count = 1
                            res += max_digit * (count - 1)
                            i = k + 1
                elif s[i].isdigit():
                    res += s[i]
                    i += 1
                else:
                    i += 1
            return res

        def longest_common_prefix(strs: list[str]) -> str:
            """
            Находит самый длинный общий префикс в группе строк.
            """
            if not strs:
                return ""
            prefix = strs[0]
            for s in strs[1:]:
                while not s.startswith(prefix):
                    prefix = prefix[:-1]
                    if not prefix:
                        return ""
            return prefix

        def merge_full_range_regex(patterns: list[str]) -> Optional[str]:
            """
            Если список паттернов покрывает полный диапазон для изменяющейся части числа,
            возвращает объединённое регулярное выражение.
            Если объединить не удаётся, то возвращается None.
            """
            min_vals = [compute_min_full(p) for p in patterns]
            max_vals = [compute_max_full(p) for p in patterns]
            total_length = len(min_vals[0])
            if any(len(x) != total_length for x in min_vals):
                return None

            common_prefix = longest_common_prefix(min_vals)
            fixed_len = len(common_prefix)
            var_len = total_length - fixed_len
            if var_len <= 0:
                return None

            intervals = sorted(zip(min_vals, max_vals), key=lambda x: int(x[0]))
            merged_min, merged_max = intervals[0]
            current_max = int(merged_max)
            for mn, mx in intervals[1:]:
                if int(mn) == current_max + 1:
                    current_max = int(mx)
                    merged_max = mx
                else:
                    return None  # интервалы не идут подряд

            # Выделяем переменную часть после общего префикса
            merged_min_var = merged_min[fixed_len:]
            merged_max_var = merged_max[fixed_len:]
            full_min = "0" * var_len
            full_max = "9" * var_len
            if merged_min_var == full_min and merged_max_var == full_max:
                return f"^{common_prefix}[0-9]{{{var_len}}}$"
            else:
                return None

        def group_merge_candidates(candidates: list[str]) -> list[str]:
            """
            Принимает список паттернов (одной группы по total_length),
            сортирует их по compute_min_full и пытается объединить подряд идущие,
            для которых merge_full_range_regex возвращает объединённое выражение.
            Если объединить для группы не удаётся, то паттерны остаются как есть.
            Возвращается список, состоящий из объединённых выражений и оставшихся паттернов.
            """
            items = [(pat, int(compute_min_full(pat))) for pat in candidates]
            items.sort(key=lambda x: x[1])
            merged_results = []
            i = 0
            while i < len(items):
                group = [items[i][0]]
                j = i + 1
                # Расширяем группу, добавляя следующих кандидатов, пока объединение группы возможно.
                while j < len(items):
                    new_group = [*group, items[j][0]]
                    if merge_full_range_regex(new_group) is not None:
                        group = new_group
                        j += 1
                    else:
                        break
                if len(group) > 1:
                    merged_expr = merge_full_range_regex(group)
                    if merged_expr is not None:
                        merged_results.append(merged_expr)
                    else:
                        merged_results.extend(group)
                    i = j
                else:
                    merged_results.append(items[i][0])
                    i += 1
            return merged_results

        candidate_groups = defaultdict(list)
        others = []

        # Разделяем входные паттерны: кандидаты для объединения (те, где встречаются квадратные скобки)
        # и остальные.
        for pat in patterns:
            if "[" in pat and "]" in pat:
                try:
                    total_len = compute_total_length(pat)
                    candidate_groups[total_len].append(pat)
                except Exception:
                    others.append(pat)
            else:
                others.append(pat)

        optimized = []
        for _, group in candidate_groups.items():
            merged_candidates = group_merge_candidates(group)
            optimized.extend(merged_candidates)
        optimized.extend(others)
        return optimized

    def find_groups_with_one_token_diff(self, regex_list: list):
        """
        Находит группы регулярных выражений, которые отличаются ровно в одном токене,
        исключая токены вида {} из сравнения.

        Алгоритм:
        1. Токенизируем каждое регулярное выражение, при этом захватываем как обычные токены
            (одиночные цифры, диапазоны вида [x] или [x-y], точку), так и токены вида {число}.
        2. При создании масок (замене токена на маркер "*") для группировки, если токен относится к виду {число},
            пропускаем его – таким образом, группы не формируются по различиям в фигурных скобках.
        """  # noqa: RUF002

        import re
        from collections import defaultdict

        regex_parts_pattern = r"\d|\[\d[-\d]*\]|\.|\{\d\}"

        tokenized = {}
        for regex in regex_list:
            tokens = re.findall(regex_parts_pattern, regex)
            tokenized[regex] = tokens

        masks = defaultdict(list)
        curly_pattern = re.compile(r"\{\d+\}")
        for regex, tokens in tokenized.items():
            for i, token in enumerate(tokens):
                if curly_pattern.fullmatch(token):  # Если токен вида {число} – пропускаем его
                    continue
                masked_tokens = tokens.copy()
                masked_tokens[i] = "*"
                mask_tuple = tuple(masked_tokens)
                masks[mask_tuple].append(regex)

        chosen_mask = {}
        for regex, tokens in tokenized.items():
            best_mask = None
            best_group_size = 0
            best_index = -1
            for i, token in enumerate(tokens):
                if curly_pattern.fullmatch(token):
                    continue
                masked_tokens = tokens.copy()
                masked_tokens[i] = "*"
                mask_tuple = tuple(masked_tokens)
                group = masks[mask_tuple]
                if len(group) > 1:
                    # Выбираем маску, дающую наибольшую группу, а при равенстве – с заменой, находящейся правее
                    if len(group) > best_group_size or (len(group) == best_group_size and i > best_index):
                        best_mask = mask_tuple
                        best_group_size = len(group)
                        best_index = i
            if best_mask is not None:
                chosen_mask[regex] = best_mask

        groups = defaultdict(list)
        for regex in regex_list:
            if regex in chosen_mask:
                groups[tuple(chosen_mask[regex])].append(regex)
            else:
                groups[regex].append(regex)

        return list(groups.values())

    def merge_one_diff_regex_patterns(self, regex_list: list, use_dot: bool, caret_symbol: str, dollar_symbol: str):
        """
        Оптимизирует список регулярных выражений.
        1. Производит замену вида "[a-a]" на "a"
        2. При необходимости заменяет "[0-9]" на точку.
        3. Группирует регулярки, которые отличаются ровно в одном токене, исключая токены вида {}, и объединяет их,
            используя объединение отличающегося токена.
        """
        def merge_token_group(tokens: list) -> str:
            """
            Объединяет список токенов, которые могут быть одиночными цифрами (например, "4")
            или диапазонами (например, "[5-9]") в один объединённый токен.
            Пример: ["4", "[5-9]"] -> ["[4-9]"]
            """

            def extract_digits(token):
                if re.fullmatch(r"\d", token):
                    return [token]
                m = re.fullmatch(r"\[(\d)(?:-(\d))?\]", token)
                if m:
                    start = m.group(1)
                    end = m.group(2)
                    if end:
                        return [str(d) for d in range(int(start), int(end) + 1)]
                    else:
                        return [start]
                return [token]  # Если формат не соответствует ожидаемому – возвращаем токен как есть.

            extracted = []
            for token in tokens:
                extracted.extend(extract_digits(token))
            extracted = sorted(set(extracted), key=lambda x: x)
            if len(extracted) == 1:
                return extracted[0]

            if all(ch.isdigit() for ch in extracted):
                groups = []
                current_group = []
                for ch in extracted:
                    if not current_group:
                        current_group = [ch]
                    else:
                        if int(ch) == int(current_group[-1]) + 1:
                            current_group.append(ch)
                        else:
                            groups.append(current_group)
                            current_group = [ch]
                if current_group:
                    groups.append(current_group)
                merged_parts = ""
                for group in groups:
                    if len(group) == 1:
                        merged_parts += group[0]
                    else:
                        if int(group[0]) == int(group[-1]) - 1:
                            merged_parts += f"{group[0]}{group[-1]}"
                        else:
                            merged_parts += f"{group[0]}-{group[-1]}"
                return f"[{merged_parts}]"
            else:
                return "[" + "".join(extracted) + "]"

        def find_common_pattern(patterns: list) -> str:
            """
            Объединяет список паттернов, предполагая, что они отличаются ровно в одном токене.
            """
            token_pattern = re.compile(r"\d|\[\d[-\d]*\]|\.|\{\d\}")
            tokenized = [token_pattern.findall(p) for p in patterns]
            if not tokenized:
                return ""
            token_len = len(tokenized[0])
            if any(len(tokens) != token_len for tokens in tokenized):
                raise ValueError("Паттерны имеют разное число токенов!")

            common_tokens = []
            for i in range(token_len):
                tokens_at_i = [tokens[i] for tokens in tokenized]
                if all(t == tokens_at_i[0] for t in tokens_at_i):
                    common_tokens.append(tokens_at_i[0])
                else:
                    merged = merge_token_group(tokens_at_i)
                    common_tokens.append(merged)
            return "".join(common_tokens)

        # 1. Замена [a-a] на a
        single_symbol_regex = r"\[([0-9])-([0-9])\]"
        regex_list = [
            re.sub(
                single_symbol_regex,
                lambda m: m.group(1) if m.group(1) == m.group(2) else m.group(0),
                regex,
            )
            for regex in regex_list
        ]

        # 2. Замена [0-9] на точку, если нужно
        if use_dot:
            regex_list = [re.sub(r"\[0-9\]", ".", regex) for regex in regex_list]

        # 3. Группировка регулярных выражений, отличающихся ровно в одном токене.
        groups = self.find_groups_with_one_token_diff(regex_list)
        optimized_list = []
        for group in groups:
            if len(group) > 1:
                cores = [regex.strip("^$") for regex in group]
                merged_core = find_common_pattern(cores)
                optimized_list.append(caret_symbol + merged_core + dollar_symbol)
            else:
                optimized_list.extend(group)
        return optimized_list

    def find_groups_with_curly_token_diff(self, regex_list: list) -> list:
        """
        Находит группы регулярных выражений, которые отличаются только значением внутри токена вида {число}.

        Ожидается, что каждое регулярное выражение содержит ровно один токен вида {число}.
        Если два или более выражения имеют одинаковые префикс и суффикс (то есть отличаются только числом
        внутри фигурных скобок), они объединяются в одну группу.
        """

        # Шаблон для поиска выражений вида: <префикс>{<число>}<суффикс>
        pattern = re.compile(r"^(.*)\{(\d+)\}(.*)$")
        groups = defaultdict(list)

        for regex in regex_list:
            match = pattern.fullmatch(regex)
            if match:
                prefix, _, suffix = match.groups()
                key = (prefix, suffix)
                groups[key].append(regex)
            else:
                # Если выражение не соответствует ожидаемому формату, группируем его отдельно
                groups[regex].append(regex)

        return list(groups.values())

    def combine_curly_token_group(self, group: list) -> list:
        """
        Объединяет группу регулярных выражений, отличающихся только числом внутри токена {число}.

        Если числа в токенах образуют непрерывный диапазон (например, 2, 3, 4),
        возвращается объединённое регулярное выражение с токеном вида {от,до} (например, {2,4}).
        Если числа не образуют непрерывный диапазон, возвращается исходный список выражений без изменений.

        Ожидается, что все регулярные выражения в группе имеют одинаковые префикс и суффикс.
        """  # noqa: RUF002

        import re

        pattern = re.compile(r"^(.*)\{(\d+)\}(.*)$")
        numbers = []
        prefix = None
        suffix = None

        for regex in group:
            match = pattern.fullmatch(regex)
            if not match:
                return group
            p, num, s = match.groups()
            if prefix is None and suffix is None:
                prefix, suffix = p, s
            else:
                # Если префикс или суффикс не совпадают, объединять нельзя
                if prefix != p or suffix != s:
                    return group
            numbers.append(int(num))

        # Если в группе всего одно выражение или чисел нет — объединять не нужно
        if len(numbers) <= 1:
            return group

        numbers = sorted(set(numbers))
        # Проверяем, образуют ли числа непрерывный диапазон
        if numbers[-1] - numbers[0] == len(numbers) - 1:
            combined_regex = f"{prefix}{{{numbers[0]},{numbers[-1]}}}{suffix}"
            return [combined_regex]
        else:
            return group

    def merge_repeat_range_regex_patterns(self, regex: str, caret_symbol: str, dollar_symbol: str):
        """Оптимизация повторяющихся логических элементов регулярных выражений."""

        element_pattern = re.compile(r"(\[.*?\]|\.|[^\[\].]+)")

        optimized_list = []

        if caret_symbol == "^" and dollar_symbol == "$":
            match = re.match(r"^\^(.+)\$$", regex)
        else:
            match = re.match(r"^(.+)$", regex)

        if match:
            main_body = match.group(1)

            elements = element_pattern.findall(main_body)

            optimized_elements = []
            repeat_count = 1

            for i in range(len(elements)):
                if i > 0 and elements[i] == elements[i - 1]:
                    repeat_count += 1
                else:
                    if repeat_count > 1:
                        optimized_elements.append(f"{elements[i - 1]}{{{repeat_count}}}")
                    elif i > 0:
                        optimized_elements.append(elements[i - 1])
                    repeat_count = 1

            if repeat_count > 1:
                optimized_elements.append(f"{elements[-1]}{{{repeat_count}}}")
            else:
                optimized_elements.append(elements[-1])

            optimized_regex = caret_symbol + "".join(optimized_elements) + dollar_symbol
            optimized_list.append(optimized_regex)

        return optimized_list

    def execute_optimize(self, phone_numbers_data: PhoneNumbersData, use_dot: bool, unuse_special_symbols: bool):
        if unuse_special_symbols is True:
            caret_symbol = ""
            dollar_symbol = ""
        else:
            caret_symbol = SpecialSymbolsParams.CARET
            dollar_symbol = SpecialSymbolsParams.DOLLAR

        optimized_list = []
        try:
            merged_similar_strings = self.merge_similar_strings(phone_numbers_data.data_list)
            ic(merged_similar_strings)
            merged_full_range_strings = self.merge_full_range_strings(merged_similar_strings)
            ic(merged_full_range_strings)
            list_similar_strings = self.find_groups_with_one_token_diff(merged_full_range_strings)
            ic(list_similar_strings)

            # Цикл для уменьшения списка списков похожих регулярных выражений до длины каждого элемента равной одному
            while any(len(sublist) > 1 for sublist in list_similar_strings):
                temp_optimized_list = []
                for similar_strings in list_similar_strings:
                    optimized_result = self.merge_one_diff_regex_patterns(
                        similar_strings, use_dot, caret_symbol, dollar_symbol
                    )
                    ic(optimized_result)
                    temp_optimized_list.extend(optimized_result)

                list_similar_strings = self.find_groups_with_one_token_diff(temp_optimized_list)
            ic("---", list_similar_strings)

            temp_list_similar_strings = []
            for regex_list in list_similar_strings:
                # 1. Замена [a-a] на a
                single_symbol_regex = r"\[([0-9])-([0-9])\]"
                regex_list = [
                    re.sub(
                        single_symbol_regex,
                        lambda m: m.group(1) if m.group(1) == m.group(2) else m.group(0),
                        regex,
                    )
                    for regex in regex_list
                ]
                temp_list_similar_strings.append(regex_list)

            if use_dot:
                # 2. Замена [0-9] на точку, если нужно
                for regex_list in temp_list_similar_strings:
                    index = temp_list_similar_strings.index(regex_list)
                    regex_list = [re.sub(r"\[0-9\]", ".", regex) for regex in regex_list]
                    temp_list_similar_strings[index] = regex_list

            list_similar_curly_strings = self.find_groups_with_curly_token_diff(
                [regex for sub_list in temp_list_similar_strings for regex in sub_list]
            )
            res_list_similar_strings = []
            for temp_temp_list_similar_string in list_similar_curly_strings:
                res_list_similar_strings.extend(self.combine_curly_token_group(temp_temp_list_similar_string))
            ic(res_list_similar_strings)

            for similar_strings in res_list_similar_strings:
                similar_strings = self.merge_repeat_range_regex_patterns(similar_strings, caret_symbol, dollar_symbol)
                optimized_list.extend(similar_strings)
            ic(optimized_list)

            phone_numbers_data.data_list = optimized_list
        except Exception as e:
            raise Exception(ErrorsParams.ERROR_OPTIMIZE_REGEX) from e
        else:
            return phone_numbers_data
