from telebot import types
import words
import config
from collections import deque
import shelve

word_revs = shelve.open("words_reviewers")
word_evs = shelve.open("words_evaluators")
to_play = words.WordsStorage(config.playable_storage_filename) 
on_review = words.Reviewer(config.unreviewed_storage_filename, config.new_words_storage_filename) 

def check_if_user_can_review(uid):
    with open("reviewers_list") as list_:
        everyone = map(str.strip, list_.readlines())
        if str(uid) in everyone:
            return True

def make_review_choice_keyboard():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Проверять, подходят ли новые слова')
    markup.row('Оценивать слова')
    return markup

def make_first_type_review_keyboard():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Это хорошее слово для Шляпы')
    markup.row('Это слово плохо подходит для Шляпы')
    markup.row('Это слово совсем не подходит для Шляпы')
    return markup

def make_second_type_review_keyboard():
    markup = types.ReplyKeyboardMarkup()
    markup.row('0', '1')
    markup.row('2', '3', '4')
    return markup

def make_not_checked_words_pack(size, uid):
    words = on_review.get_not_checked(size) 
    for word in words:
        if word not in word_revs:
            word_revs[word] = []
    return deque([word for word in words if uid not in word_revs[word]])

def make_not_eval_words_pack(size, uid):
    words = on_review.get_not_evaluated(size) 
    for word in words:
        if word not in word_evs:
            word_evs[word] = []
    return deque([word for word in words if uid not in word_evs[word]])

def add_new_word(word):
    if on_review.add_word(word, to_play):
        print("Added " + word) 
        return True
    else:
        print("Tried to add " + word + ", already exists, complexity: " + str(to_play.check_complexity(word)))
        return False

def add_first_type_review(word, value, uid):
    if word in word_revs:
        word_revs[word] = word_revs[word] + [uid]
    else:
        word_revs[word] = [uid]

    if on_review.add_goodness_mark(word, value):
        print("Added goodness mark")
    else:
        print("Something went wrong with the goodness mark")
