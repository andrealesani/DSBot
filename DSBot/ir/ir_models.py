
class IRMod():
    def __init__(self, name, model, description):
        self.name = name
        self.model = model
        self.description = description

    def __str__(self):
        return f'{self.name} : {self.description}'