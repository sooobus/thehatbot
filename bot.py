import config
import telebot
import utils
import texts
from collections import deque

bot = telebot.TeleBot(config.token)
wait_for_word = {}
first_type_eval = {}
second_type_eval = {}
first_type_eval_last = {}
second_type_eval_last = {}

@bot.message_handler(commands=["review"])
def choose_review_type(message): 
    if utils.check_if_user_can_review(message.chat.id):
        bot.send_message(message.chat.id, "У вас есть права редактора. Выберите тип цензуры.", reply_markup=utils.make_review_choice_keyboard())
    else:
        bot.send_message(message.chat.id, "К сожалению, у вас нет прав редактора. Их можно получить, написав на почту sooobus@gmail.com.")


@bot.message_handler(commands=["add_word"])
def choose_review_type(message): 
    bot.send_message(message.chat.id, "Напишите, пожалуйста, ровно одно слово.")
    wait_for_word[message.chat.id] = True

@bot.message_handler(regexp="Проверять, подходят ли новые слова")
def handle_first_level_review_query(message):
    bot.send_message(message.chat.id, "Вы выбрали проверку качества слов. Сейчас вам будут присылаться слова. Ваша задача -- оценить, насколько каждое слово подходит для Шляпы.")

    first_type_eval[message.chat.id] = utils.make_not_checked_words_pack(10, message.chat.id)
    if len(first_type_eval[message.chat.id]) > 0:
        first_type_eval_last[message.chat.id] = first_type_eval[message.chat.id].pop() 
        bot.send_message(message.chat.id,  first_type_eval_last[message.chat.id], reply_markup=utils.make_first_type_review_keyboard())
    else:
        bot.send_message(message.chat.id, "Слова для проверки закончились! Спасибо!")
@bot.message_handler(regexp="Оценивать слова")
def handle_second_level_review_query(message):
    bot.send_message(message.chat.id, "Вы выбрали оценку слов. Сейчас вам будут присылаться слова. Ваша задача -- оценить сложность слова. Если вы видите, что слово явно для шляпы плохое, напишите Валерии Немычниковой. Напоминаем критерии: " + texts.criteria_eval)

@bot.message_handler(regexp='(Это хорошее слово для Шляпы|Это слово плохо подходит для Шляпы|Это слово совсем не подходит для Шляпы)')
def handle_second_type_review_query(message):
    marks = ['Это хорошее слово для Шляпы', 'Это слово плохо подходит для Шляпы', 'Это слово совсем не подходит для Шляпы']
    if message.chat.id in first_type_eval_last:
        utils.add_first_type_review(first_type_eval_last[message.chat.id], marks.index(message.text), message.chat.id)
    if message.chat.id in first_type_eval and len(first_type_eval[message.chat.id]) > 0:
        first_type_eval_last[message.chat.id] = first_type_eval[message.chat.id].pop() 
        bot.send_message(message.chat.id,  first_type_eval_last[message.chat.id], reply_markup=utils.make_first_type_review_keyboard()) 
    else:
        bot.send_message(message.chat.id,  "Слова закончились! Спасибо за помощь!") 


@bot.message_handler(content_types=['text'])
def handle_word(message):
    if(message.chat.id in wait_for_word and wait_for_word[message.chat.id]):
        if utils.add_new_word(message.text.strip()):
            bot.send_message(message.chat.id, "Спасибо за слово! Оно появится в игре после проверки.")
        else:
            bot.send_message(message.chat.id, "Такое слово уже есть в нашей базе :) Спасибо!")
        wait_for_word[message.chat.id] = False
    else:
        bot.send_message(message.chat.id, "К сожалению, ваша команда непонятна.")
        print("Just text")
if __name__ == '__main__':
        bot.polling(none_stop=True)
