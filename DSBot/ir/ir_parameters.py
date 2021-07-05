
class IRPar():
    def __init__(self, name, value, description):
        self.name = name
        self.value = value
        self.description = description
    def __str__(self):
        return f'{self.name} = {self.value} ({self.description})'