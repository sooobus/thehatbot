import random
from collections import deque
import time

class Circle(object):
    def __init__(self, players_number, words_storage, sender, uid, keyboard, transit_keyboard, check_status, is_pair=False, players_names=[], circle_limit=None, words_limit=None):
    #TODO uniq names
        assert(1 < players_number <= 20)
        self.players = players_names
        if len(players_names) < players_number:
            with open("names") as names_f:
                self.players += list(map(str.strip, random.sample(names_f.readlines(), players_number - len(self.players))))
        self.players = self.players[:players_number]
        self.players_num = players_number
        self.is_pair = is_pair
        self.circle_limit = circle_limit
        self.words_limit = words_limit
        self.w_storage = words_storage
        self.explained = {}
        self.count = [[ 0 ] * players_number] * players_number
        self.sender = sender
        self.uid = uid
        self.keyboard = keyboard
        self.transit_keyboard = transit_keyboard
        self.check_status = check_status

    def show(self):
        print(len(self.players))
        print(self.players)

    def add_explained(self, word, time, finished):
        if word in self.explained:
            self.explained[word]['time'] += time
            self.explained[word]['finished'] = finished
        else:
            self.explained[word] = {"time": time, "finished": finished}

    def make_turn(self, ind, shift):
        self.sender(self.uid, self.players[ind] + " объясняет к " + self.players[(ind + shift) % self.players_num], reply_markup=self.keyboard)

        word = self.hat.pop()
        t0 = time.time()
        pre = time.time()
        print("t0", str(t0))
        cnt = 0
        self.sender(self.uid, word, reply_markup=self.keyboard)
        while(time.time() - t0 < 20.0):
            time.sleep(0.5)
            #print(check_status(uid))
            if self.check_status(self.uid):
                cnt += 1
                self.add_explained(word, time.time() - pre, True) 
                if not len(self.hat):
                    return cnt
                word = self.hat.pop()
                pre = time.time()
                self.sender(self.uid, word, reply_markup=self.keyboard)
            print(time.time() - t0)
        fintime = time.time()
        self.sender(self.uid, "Время!", reply_markup=self.keyboard)
        time.sleep(3)
        self.sender(self.uid, "Стоп", reply_markup=self.transit_keyboard)
        if self.check_status(self.uid):
            print('Помечено угаданным')
            cnt += 1
            self.add_explained(word, fintime - pre, True)
        else:
            self.add_explained(word, fintime - pre, False)
        return cnt

#на каждом круге обновляем список партнёров
    def individual_play(self):
        #def check_status():
        #    ans = input()
        #    if ans == '+':
        #        return True
        #    else:
        #        return False

#TODO апель
        if self.circle_limit:
            self.words_limit = cicle_limit * self.players_num * 6
        else:
            self.circle_limit = 1000
            if not self.words_limit:
                self.words_limit = 100

        self.hat = deque(self.w_storage.take_hat(self.words_limit))
        if self.is_pair:
            shift = self.players_num // 2
        else:
            shift = 1
        circle_cnt = 0
        expl_cnt = 0
        while circle_cnt < self.circle_limit and len(self.hat) > 0:
            ind = expl_cnt % self.players_num
            input()
            self.count[ind][(ind + shift) % self.players_num] += self.make_turn(ind, shift)
            expl_cnt += 1
            if expl_cnt % self.players_num == 0 and not self.is_pair:
                circle_cnt += 1
                shift += 1
                shift %= self.players_num
                if shift == 0:
                    shift += 1

        return self.count, self.explained

