import shelve
import pandas as pd
import numpy as np
import math
import random

class WordsStorage(object): #this class is used to interact with the storage of evaluated words 
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
            self.storage[word] = {'human': ((1/13) * complexity), 'time': [], 'complexity': ((1/13) *  complexity)}

    def clear_storage(self):
        self.storage.clear()

    def add_from_csv(self, filename):
        words = pd.read_csv(filename, header=None, names=['word', 'complexity'], delimiter=';')
        print(words.head(100))    
        for word in words['word']:
            #print(np.mean(np.array(words[words['word'] == word]['complexity'].values)))
            self.add_word(word, np.mean(np.array(words[words['word'] == word]['complexity'].values)))

    def check_complexity(self, word):
        return self.storage[word]['complexity']

    def add_time(self, word, time):
        time = min(time, 60.0) #if the word was explained more than 3 turns, it is possibly not so easy
        if word in self.storage:
            self.storage[word]['time'].append(time)
            time = self.storage[word]['time']
            meantime = sum(time) / len(time) 
            normal_time = math.tanh(meantime / 30)
            l = min(10, len(time))
            self.storage[word]['complexity'] = self.storage[word]['human'] * (1 - 0.1 * l) + normal_time * (0.1 * l)

    def take_hat(self, size, complexity_lower, complexity_upper):
        #for smth in self.storage:
        #    print((self.storage[smth]['complexity']))
        hat = [word for word in self.storage if complexity_lower <= self.storage[word]['complexity'] < complexity_upper]
        if len(hat) > size:
            return random.sample(hat, size)
        else:
            return random.shuffle(hat)

class Reviewer(object): #this class is used to interact with not yet evaluated words
    def __init__(self, filename):
        self.storage = shelve.open(filename)

    def __exit__(self):
        self.storage.close()

    def add_word(word, playable_storage): # storage stores pairs (word, list), where list contains all the marks for the word
        if word not in self.storage and not playable_storage.has_word():
            self.storage[word] = {}

    def add_mark(word, mark):
        if word in self.storage and 0 <= mark <= 12 and len(self.storage) < 3:
            self.storage[word].append(mark)

    def transit_evaluated(playable_storage): #moves words with 3 marks to playable
        for word in self.storage:
            if len(self.storage[word]) == 3:
                complexity = sum(self.storage[word])
                playable_storage.add_word(word, complexity)
