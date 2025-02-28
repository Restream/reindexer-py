from hamcrest.core.base_matcher import BaseMatcher


class CloseToDict(BaseMatcher):
    def __init__(self, expected, delta):
        self.expected = expected
        self.delta = delta

    def _matches(self, actual):
        if not isinstance(actual, dict) or not isinstance(self.expected, dict):
            return False

        for key, expected_value in self.expected.items():
            if key not in actual:
                return False
            if not self.matches_values(expected_value, actual[key]):
                return False

        # Check if there are any redundant keys
        for key in actual:
            if key not in self.expected:
                return False

        return True

    def matches_values(self, expected_value, actual_value):
        if isinstance(expected_value, (int, float)):
            # If the value is a number, check with delta
            return expected_value - self.delta <= actual_value <= expected_value + self.delta
        elif isinstance(expected_value, list):
            # If the value is a list, check each element
            if not isinstance(actual_value, list) or len(actual_value) != len(expected_value):
                return False
            for i, expected_elem in enumerate(expected_value):
                if not self.matches_values(expected_elem, actual_value[i]):
                    return False
            return True
        elif isinstance(expected_value, dict):
            # If the value is a dictionary, compare entire dictionaries using the same method
            return CloseToDict(expected_value, self.delta)._matches(actual_value)
        else:
            # For other values check for strict equality
            return expected_value == actual_value

    def describe_to(self, description):
        description.append_text("a dictionary close to ").append_description_of(self.expected)


class CloseToItems(CloseToDict):
    def _matches(self, actual):
        if not isinstance(actual, list) or not isinstance(self.expected, list):
            return False

        if len(actual) != len(self.expected):
            return False

        for expected_dict, actual_dict in zip(self.expected, actual):
            if not CloseToDict(expected_dict, self.delta)._matches(actual_dict):
                return False

        return True

    def describe_to(self, description):
        description.append_text("a list of dictionaries close to ").append_description_of(self.expected)


def close_to_dict(expected, delta=0.01):
    """ Проверить, что 2 словаря приблизительно (с учетом дельты для числовых типов) равны друг другу
    :param expected: словарь для сравнения
    :param delta: дельта для приблизительного сравнения числовых типов
    """
    return CloseToDict(expected, delta)


def close_to_items(expected, delta=0.01):
    """ Проверить, что 2 списка словарей приблизительно (с учетом дельты для числовых типов) равны друг другу
    :param expected: список словарей для сравнения
    :param delta: дельта для приблизительного сравнения числовых типов
    """
    return CloseToItems(expected, delta)
