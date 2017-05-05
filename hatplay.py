import random
from collections import deque
import time
import numpy as np


class Circle(object):
    def __init__(
            self,
            players_number,
            words_storage,
            sender,
            uid,
            keyboard,
            transit_keyboard,
            check_status,
            is_pair=False,
            players_names=[],
            circle_limit=None,
            words_limit=None,
            complexity=(0.0, 1.01)):
        if (not (1 < players_number <= 20)):
            players_number = 2
        if is_pair and players_number % 2 != 0:
            players_number += 1
        self.players = players_names
        if len(players_names) < players_number:
            with open("names") as names_f:
                self.players += list(map(str.strip,
                                         random.sample(
                                            names_f.readlines(),
                                            players_number -
                                            len(self.players))))
        self.players = self.players[:players_number]
        self.players_num = players_number
        self.is_pair = is_pair
        self.circle_limit = circle_limit
        self.words_limit = words_limit
        self.w_storage = words_storage
        self.explained = {}
        self.count = [0] * players_number
        self.sender = sender
        self.uid = uid
        self.keyboard = keyboard
        self.transit_keyboard = transit_keyboard
        self.check_status = check_status

        if self.circle_limit:
            self.words_limit = cicle_limit * self.players_num * 6
        else:
            self.circle_limit = 1000
            if not self.words_limit:
                self.words_limit = 100

        self.hat = deque(self.w_storage.take_hat(
            self.words_limit,
            complexity_lower=complexity[0],
            complexity_upper=complexity[1]))

        if self.is_pair:
            self.shift = self.players_num // 2
        else:
            self.shift = 1
        self.circle_cnt = 0
        self.expl_cnt = 0

    def show(self):
        print(len(self.players))
        print(self.players)

    def add_explained(self, word, time, finished):
        if word in self.explained:
            self.explained[word]['time'] += time
            self.explained[word]['finished'] = finished
        else:
            self.explained[word] = {"time": time, "finished": finished}

    def make_turn(self):
        ind = self.expl_cnt % self.players_num
        self.sender(
            self.uid,
            self.players[ind] + " => " +
            self.players[(ind + self.shift) % self.players_num],
            reply_markup=self.keyboard)

        word = self.hat.pop()
        t0 = time.time()
        pre = time.time()
        print("t0", str(t0))
        cnt = 0
        self.sender(self.uid, word, reply_markup=self.keyboard)
        got_error = False
        while(time.time() - t0 < 20.0):
            time.sleep(0.5)
            # print(check_status(uid))
            stat = self.check_status(self.uid)
            if stat:
                cnt += 1
                self.add_explained(word, time.time() - pre, True)
                if not len(self.hat):
                    break
                word = self.hat.pop()
                pre = time.time()
                self.sender(self.uid, word, reply_markup=self.keyboard)
            elif stat is None:
                print("Caught error")
                self.add_explained(word, time.time() - pre, False)
                self.hat.insert(random.randrange(len(self.hat)), word)
                caught_error = True
                break

            print(time.time() - t0)
        if not caught_error:
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
                self.hat.insert(random.randrange(len(self.hat)), word)
        else:
            self.sender(self.uid, "Стоп", reply_markup=self.transit_keyboard)
        self.count[ind] += cnt
        self.count[(ind + self.shift) % self.players_num] += cnt
        print(self.count)

    def next_turn(self):  # return True, if ok, False, if finished
        self.expl_cnt += 1
        if self.expl_cnt % self.players_num == 0 and not self.is_pair:
            self.circle_cnt += 1
            self.shift += 1
            self.shift %= self.players_num
            if self.shift == 0:
                self.shift += 1
        if self.circle_cnt < self.circle_limit and len(self.hat) > 0:
            return True
        else:
            return False

    def results(self):
        print(self.count)
        return zip(self.players, self.count), self.explained

