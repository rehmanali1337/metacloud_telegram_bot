from models.types import NumberInfo


class NumberData:
    def __init__(self, number) -> None:
        assert isinstance(number, str)
        if contains_non_digit(number):
            number = non_digitize(number)
        self.number = number

    def is_int(self):
        if '.' in self.number:
            return False
        if not self.number.isdigit():
            return False
        return True

    def is_float(self):
        if '.' in self.number:
            number = self.number.split('.')[0]
            fraction = self.number.split('.')[1]
            if not number.isdigit():
                return False
            if not fraction.isdigit():
                return False
            return True
        return False

    def number_len(self):
        if '.' not in self.number:
            return len(self.number)
        else:
            return len(self.number.split('.')[0])

    def fraction_len(self):
        if '.' in self.number:
            return len(self.number.split('.')[1])
        return 0

    def floated_version(self):
        assert self.is_float()
        fractions = self.fraction_len()
        return f"%.{fractions}f" % float(self.number)

    def int_version(self):
        assert self.is_int()
        return int(self.number)


def contains_non_digit(number: str):
    assert isinstance(number, str)
    if '.' in number:
        data = number.split('.')
        try:
            assert data[0].isdigit()
            assert data[1].isdigit()
            return False
        except AssertionError:
            return True
    return True


def non_digitize(s: str):
    assert isinstance(s, str)
    n = ''.join(i for i in s if i.isdigit() or i == '.')
    return n
