import shelve
import pandas as pd
import math

class WordsStorage(object): #this class is used to interact with the storage of evaluated words 
    def __init__(self, filename):
        self.storage = shelve.open(filename)
    def __exit__(self):
        self.storage.close()

    def add_word(self, word, complexity):
        if word in self.storage:
            self.storage[word] = {'human': (1 / (13 - complexity), 'time': [], 'complexity': (1 / (13 - complexity))

    def add_from_csv(self, filename):
        words = pd.read_csv("sample_csv.csv", header=None, names=['word', 'complexity'], delimiter=' ')
        print(words.head())    
        for word in words['word']:
            add_word(word, [words[words['word'] == word]['complexity'])

    def add_time(self, word, time):
        time = min(time, 60.0) #if the word was explained more than 3 turns, it is possibly not so easy
        if word in self.storage:
            self.storage[word]['time'].append(time)
            time = self.storage[word]['time']
            meantime = sum(time) / len(time) 
            normal_time = math.tanh(meantime / 30)
            l = min(10, len(time))
            self.storage[word]['complexity'] = self.storage[word]['human'] * (1 - 0.1 * l) + normal_time * (0.1 * l)

    def take_hat(size, complexity_lower, complexity_upper):
        hat = [word for word, params in self.storage if complexity_upper <= params['complexity'] < complexity_lower]
        if len(hat) > size:
            return random.sample(hat, size)
        else:
            return random.shuffle(hat)

class Reviewer(object): #this class is used to interact with not yet evaluated words
    def __init__(self, filename):
        self.storage = shelve.open(filename)

    def __exit__(self):
        self.storage.close()

    def add_word(word): # storage stores pairs (word, list), where list contains all the marks for the word
        if word not in self.storage:
            self.storage[word] = []

    def add_mark(word, mark):
        if word in self.storage and 0 <= mark <= 12 and len(self.storage) < 3:
            self.storage[word].append(mark)

    def transit_evaluated(filename): #moves words with 3 marks to playable
        s = WordsStorage(filename)
        for word in self.storage:
            if len(self.storage[word]) == 3:
                complexity = sum(self.storage[word])
                s.add_word(word, complexity)
