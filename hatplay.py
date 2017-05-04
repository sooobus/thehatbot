import random
from collections import deque
import time

class Circle(object):
    def __init__(self, players_number, words_storage, is_pair=False, players_names=[], circle_limit=None, words_limit=None):
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
        self.w_storage = words_storage

    def show(self):
        print(len(self.players))
        print(self.players)

#на каждом круге обновляем список партнёров
    def individual_play(self, check_status, uid, sender, keyboard, transit_keyboard):
        #def check_status():
        #    ans = input()
        #    if ans == '+':
        #        return True
        #    else:
        #        return False

        explained = {}
        def add_explained(word, time, finished):
            if word in explained:
                explained[word]['time'] += time
                explained[word]['finished'] = finished
            else:
                explained[word] = {"time": time, "finished": finished}

        def make_turn():
            sender(uid, self.players[ind] + " объясняет к " + self.players[(ind + shift) % players_num], reply_markup=keyboard)

            word = hat.pop()
            t0 = time.time()
            pre = time.time()
            print("t0", str(t0))
            cnt = 0
            sender(uid, word, reply_markup=keyboard)
            while(time.time() - t0 < 20.0):
                time.sleep(0.5)
                #print(check_status(uid))
                if check_status(uid):
                    cnt += 1
                    add_explained(word, time.time() - pre, True) 
                    if not len(hat):
                        return cnt
                    word = hat.pop()
                    pre = time.time()
                    sender(uid, word, reply_markup=keyboard)
                print(time.time() - t0)
            fintime = time.time()
            sender(uid, "Время!", reply_markup=keyboard)
            time.sleep(3)
            sender(uid, "Стоп", reply_markup=transit_keyboard)
            if check_status(uid):
                print('Помечено угаданным')
                cnt += 1
                add_explained(word, fintime - pre, True)
            else:
                add_explained(word, fintime - pre, False)
            return cnt
#TODO апель
        players_num = len(self.players)
        count = [[ 0 ] * players_num] * players_num
        if self.circle_limit:
            self.words_limit = cicle_limit * players_num * 6
        else:
            self.circle_limit = 1000
            if not self.words_limit:
                self.words_limit = 100

        hat = deque(self.w_storage.take_hat(self.words_limit))
        shift = 1
        circle_cnt = 0
        expl_cnt = 0
        while circle_cnt < self.circle_limit and len(hat) > 0:
            ind = expl_cnt % players_num
            input()
            count[ind][(ind + shift) % players_num] += make_turn()
            expl_cnt += 1
            if expl_cnt % players_num == 0:
                circle_cnt += 1
                shift += 1
                shift %= players_num
                if shift == 0:
                    shift += 1

        return count, explained

