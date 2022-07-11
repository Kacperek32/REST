import json

class bibliotekus:
    def __init__(self):
        try:
            with open("biblioteku.json", "r") as f:
                self.bibliotekus = json.load(f)
        except FileNotFoundError:
            self.bibliotekus = []

    def all(self):
        return self.bibliotekus

    def get(self, id):
        biblioteku = [biblioteku for biblioteku in self.all() if biblioteku['id'] == id]
        if biblioteku:
            return biblioteku[0]
        return []

    def create(self, data):
        self.bibliotekus.append(data)
        self.save_all()

    def save_all(self):
        with open("biblioteku.json", "w") as f:
            json.dump(self.bibliotekus, f)

    def update(self, id, data):
        biblioteku = self.get(id)
        if biblioteku:
            index = self.bibliotekus.index(biblioteku)
            self.bibliotekus[index] = data
            self.save_all()
            return True
        return False


    def delete(self, id):
        biblioteku = self.get(id)
        if biblioteku:
            self.bibliotekus.remove(biblioteku)
            self.save_all()
            return True
        return False


bibliotekus = bibliotekus()