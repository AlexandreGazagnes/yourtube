class Name:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hello {self.name}!")

    def __len__(self):
        return 10 * len(self.name)


class Int(int):
    def __init__(self, value) -> None:
        super().__init__()

    def __len__(self):
        return str(self).__len__()
