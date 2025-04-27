from icecream import ic

from constants.constants import ErrorsParams


class RegexController:
    def __init__(self):
        pass

    def prepare_data(self, data: str):
        ic("---------------------------------")
        ic("POOLS TO REGEX")
        ic("---------------------------------")
        pools = []
        numbers = []
        groups = []
        try:
            temp = data.split(",")
            for elem in temp:
                if " - " in elem:
                    for number in elem.split(" - "):
                        pools.append(number.strip())
                else:
                    if "-" in elem:
                        numbers.append("".join(elem.strip().split("-")))
                    else:
                        numbers.append(elem.strip())

            if len(numbers) != 0:
                numbers = sorted(list(set(numbers)))
                groups = []
                start = numbers[0]
                prev = start

                for num in numbers[1:]:
                    if prev[0] != "0":
                        if (
                            num == str(int(prev) + 1)
                            and len(str(num)) == len(str(prev))
                            and str(num)[0] == str(prev)[0]
                        ):
                            prev = num
                        else:
                            groups.append((str(start), str(prev)))
                            start = num
                            prev = start
                    else:
                        if (
                            num == ("0" + str(int(prev) + 1))
                            and len(str(num)) == len(str(prev))
                            and str(num)[0] == str(prev)[0]
                        ):
                            prev = num
                        else:
                            groups.append((str(start), str(prev)))
                            start = num
                            prev = start
                groups.append((str(start), str(prev)))

            if len(pools) != 0:
                if len(pools) % 2 == 0:
                    for i in range(0, len(pools), 2):
                        groups.append((pools[i], pools[i + 1]))

            sorted_groups = sorted(groups, key=lambda x: int(x[0]))

        except Exception as e:
            raise Exception(ErrorsParams.ERROR_POOLS_VALIDATE) from e
        else:
            ic(sorted_groups)
            ic(numbers)
            ic(pools)
            return sorted_groups
