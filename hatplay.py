import random
from collections import deque
import time

class Circle(object):
    def __init__(self, players_number, is_pair=False, players_names=[], circle_limit=None, words_limit=None):
    #TODO uniq names
        assert(1 < players_number <= 20)
        self.players = players_names
        if len(players_names) < players_number:
            with open("names") as names_f:
                self.players += list(map(str.strip, random.sample(names_f.readlines(), players_number - len(self.players))))
        self.players = self.players[:players_number]
        self.is_pair = is_pair
        self.circle_limit = circle_limit
        self.words_limit = words_limit
        self.w_storage = WordsStorage(config.storage_filename)

    def show(self):
        print(len(self.players))
        print(self.players)

#на каждом круге обновляем список партнёров
    def individual_play(self):

        explained = {}
        def add_explained(word, time, finished):
            if word in explained:
                explained[word]['time'] += time
            else:
                explained[word]['time'] = time
            explained[word]['finished'] = finished

        def make_turn():
             print(player_names[ind] + " объясняет к " player_names[(ind + shift) % players_num])

            timer.start()
            word = hat.pop()
            t0 = time.clock()
            pre = time.clock()
            cnt = 0
            print(word)
            while(time.clock() - t0 < 20.0):
                sleep(0.5)
                if check_status():
                    cnt += 1
                    add_explained(word, time.clock() - pre, True) 
                    word = hat.pop()
                    pre = time.clock()
                    print(word)
            print("Время!")
            sleep(3)
                if check_status():
                    cnt += 1
                    add_explained(word, time.clock() - pre)
            return cnt
#TODO апель
        players_num = len(self.players)
        count = [[ 0 ] * players_num] * players_num
        if self.circle_limit:
            self.words_limit = cicle_limit * players_num * 6
        hat = deque(self.w_storage.take_hat(self.words_limit))
        shift = 1
        circle_cnt = 0
        expl_cnt = 0
        while circle_cnt < self.cicle_limit and words_queue.size()
            ind = expl_cnt % players_num
            count[ind][(ind + shift) % players_num] += make_turn()
            expl_cnt += 1
            if expl_cnt % players_num == 0:
                cicle_cnt += 1
                shift += 1
                shift %= players_num
                if shift == 0:
                    shift += 1

#game = Circle(circle_limit=10
