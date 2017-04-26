import shelve
import pandas as pd

class WordsStorage(object):
    def __init__(self, filename):
        self.storage = shelve.open(filename)
    def __exit__(self):
        self.storage.close()

    def add_word(word, complexity=None):
        self.storage[word] = (1 / (13 - complexity))

    def add_from_csv(filename):
        words = pd.read_csv("sample_csv.csv", header=None, names=['word', 'complexity'], delimiter=' ')
        print(words.head())    
        for word in words['word']:
            add_word(word, [words[words['word'] == word]['complexity'])

