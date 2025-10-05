class Phobia:       #Phobia კლასის აღწერა.
    def __init__(self, name, age, programme, year, phobia, fear_level):
        self.name = name
        self.age = age
        self.programme = programme
        self.year = year
        self.phobia = phobia
        self.fear_level = fear_level

    def __str__(self):
        return f"{self.name}, {self.age} years old, Phobia: {self.phobia}"

    def as_tuple(self):
        return (self.name, self.age, self.programme, self.year, self.phobia, self.fear_level)
