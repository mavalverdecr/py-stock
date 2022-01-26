#py-stock
#Valver-Dev - Manu Valverde
#December 2021

class Item:
    def __init__(self, id, name, category, uds):
        
        self.id = id
        self.name = name
        self.category = category
        self.uds = uds

    def __repr__(self) -> str:
        return f"({self.id}, {self.name}, {self.category}, {self.uds})"