import shelve
import pandas as pd
import numpy as np
import math
import random


class WordsStorage(object):
    def __init__(self, filename):
        self.storage = shelve.open(filename)

    def __exit__(self):
        self.storage.close()

    def has_word(self, word):
        return word in self.storage

    def show_stats(self):
        print("Can play with: ")
        print(len(self.storage))
        print("words")

    def add_word(self, word, complexity):
        if word not in self.storage:
            self.storage[word] = {
                'human': ((1/13) * complexity),
                'time': [],
                'complexity': ((1/13) * complexity)
                }

    def clear_storage(self):
        self.storage.clear()

    def add_from_csv(self, filename):
        words = pd.read_csv(filename,
                            header=None,
                            names=['word', 'complexity'],
                            delimiter=';')
        print(words.head(100))
        for word in words['word']:
            self.add_word(
                word,
                np.mean(np.array(words[
                    words['word'] == word]['complexity'].values)))

    def check_complexity(self, word):
        if word not in self.storage:
            return None
        return self.storage[word]['complexity']

    def add_time(self, word, time):
        time = min(time, 60.0)
        if word in self.storage:
            self.storage[word]['time'].append(time)
            time = self.storage[word]['time']
            meantime = sum(time) / len(time)
            normal_time = math.tanh(meantime / 30)
            l = min(10, len(time))
            self.storage[word]['complexity'] = self.storage[
                word]['human'] * (1 - 0.1 * l) + normal_time * (0.1 * l)

    def take_hat(self, size, complexity_lower=0.0, complexity_upper=1.1):
        # for smth in self.storage:
        #    print((self.storage[smth]['complexity']))
        hat = [word for word in self.storage if complexity_lower <=
               self.storage[word]['complexity'] < complexity_upper]

        if len(hat) > size:
            return random.sample(hat, size)
        else:
            return random.shuffle(hat)


class Reviewer(object):
    def __init__(self, filename, filename_new_words):
        self.storage = shelve.open(filename)
        self.new_words = shelve.open(filename_new_words)

    def __exit__(self):
        self.storage.close()

    def clear_storage(self):
        self.storage.clear()

    def add_word(self, word, playable_storage):
        if (word not in self.new_words) and (word not in self.storage) \
        and (not playable_storage.has_word(word)):
            self.new_words[word] = {"good": 0, "cnt": 0}
            return True
        else:
            return False

    def add_goodness_mark(self, word, mark):
        if word in self.new_words and 0 <= mark <= 2 \
        and self.new_words[word]["cnt"] < 3:
            self.new_words[word] = {
                "good": self.new_words[word]["good"] + mark,
                "cnt": self.new_words[word]["cnt"] + 1
                }
            return True
        else:
            return False

    def add_good_word(self, word):
        if word not in self.storage:
            self.storage[word] = []

    def transit_good(self):
        for word in self.new_words:
            if self.new_words[word]["cnt"] == 3 \
            and self.new_words[word]["good"] < 3:
                print(word)
                self.add_good_word(word)

    def add_mark(self, word, mark):
        if word in self.storage and 0 <= mark <= 12 \
        and len(self.storage[word]) < 3:
            self.storage[word] = self.storage[word] + [mark]
            print(self.storage[word])
            return True
        else:
            return False

    def show_marks(self, word):
        if word in self.storage:
            print(self.storage[word])

    def show_goodness_marks(self, word):
        if word in self.new_words:
            print(self.new_words[word])

    def transit_evaluated(self, playable_storage):
        for word in self.storage:
            if len(self.storage[word]) == 3:
                complexity = sum(self.storage[word])
                playable_storage.add_word(word, complexity)
                del self.storage[word]

    def get_not_checked(self, size):
        return [word for word in self.new_words
                if self.new_words[word]["cnt"] < 3][:size]

    def get_not_evaluated(self, size):
        return [word for word in self.storage
                if len(self.storage[word]) < 3][:size]

    def get_all_on_goodness_review(self):
        return list(self.new_words)

    def get_all_on_complexity_review(self):
        return list(self.storage)

