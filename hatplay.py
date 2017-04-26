import random

class Circle(object):
    def __init__(self, players_number, is_pair=False, players_names=[], circle_limit=None, words_limit=None):
        assert(1 < players_number <= 20)
        self.players = players_names
        if len(players_names) < players_number:
            with open("names") as names_f:
                self.players += list(map(str.strip, random.sample(names_f.readlines(), players_number - len(self.players))))
        self.players = self.players[:players_number]
        self.is_pair = is_pair
        self.circle_limit = circle_limit
        self.words_limit = words_limit
        self.hat = ...

    def show(self):
        print(len(self.players))
        print(self.players)



c = Circle(5)
c.show()
