import config
import telebot
import utils
import texts
from collections import deque
import hatplay
import words

bot = telebot.TeleBot(config.token)
wait_for_word = {}
first_type_eval = {}
second_type_eval = {}
first_type_eval_last = {}
second_type_eval_last = {}
wait_for_players_num = {}
status = {}
game_type = {}
game = {}
complexity = {}
bugreport = {}


def check_status(uid):
    if uid in status:
        st = status[uid]
        status[uid] = False
        return st
    else:
        return False


@bot.message_handler(commands=["start"])
def handle_bot_init(message):
    bot.send_message(message.chat.id, 
                     "Это бот для игры в Шляпу!\
                     Вот список его команд: \n \
                     /play -- Играть \n \
                     /add_word -- Предложить слово для Шляпы \n \
                     /bugreport -- Сообщить об ошибке \n \
                     /info -- Информация о боте \n", 
                     reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(commands=["info"])
def handle_bot_init(message):
    config.logger.info(str(message.chat.id) + " > asked for info")
    bot.send_message(message.chat.id, texts.botinfo, reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=["bugreport"])
def handle_bugreport(message):
    config.logger.info(str(message.chat.id) + " > sent bugreport")
    bot.send_message(message.chat.id, 
                     "Опишите ошибку. Мы разберёмся и ответим.",
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bugreport[message.chat.id] = True


@bot.message_handler(commands=["play"])
def handle_game_init(message):
    config.logger.info(str(message.chat.id) + " > initiated game")
    bot.send_message(message.chat.id,
                     "Выберите сложность игры",
                     reply_markup=utils.make_complexity_choice_keyboard())


@bot.message_handler(commands=["review"])
def choose_review_type(message):
    try:
        config.logger.info(str(message.chat.id) + " > asked for review")
        if utils.check_if_user_can_review(message.chat.id):
            config.logger.info(str(message.chat.id) + " > review approved")
            bot.send_message(message.chat.id,
                             "У вас есть права редактора. Выберите тип цензуры.",
                             reply_markup=utils.make_review_choice_keyboard())
        else:
            config.logger.info(str(message.chat.id) + " > review disapproved")
            bot.send_message(message.chat.id,
                            "К сожалению, у вас нет прав редактора. \
                            Их можно получить, написав на почту \
                            sooobus@gmail.com.",
                            reply_markup=telebot.types.ReplyKeyboardRemove())
    except:
        config.logger.error(str(message.chat.id) + " > crashed on review")
        utils.send_sad_message(bot.send_message, message.chat.id)


@bot.message_handler(commands=["add_word"])
def choose_review_type(message):
    config.logger.info(str(message.chat.id) + " > add_word")
    bot.send_message(message.chat.id,
                     "Напишите, пожалуйста, ровно одно слово.",
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    wait_for_word[message.chat.id] = True


@bot.message_handler(regexp="Проверять, подходят ли новые слова")
def handle_first_level_review_query(message):
    try:
        config.logger.info(str(message.chat.id) + " > check words level 1")
        bot.send_message(message.chat.id, "Вы выбрали проверку качества слов. \
                                        Сейчас вам будут присылаться слова. \
                                        Ваша задача -- оценить, насколько \
                                        каждое слово подходит для Шляпы.",
                                        reply_markup=telebot.types.ReplyKeyboardRemove())
        first_type_eval[message.chat.id] = utils.make_not_checked_words_pack(
            10,
            message.chat.id)
        if len(first_type_eval[message.chat.id]) > 0:
            first_type_eval_last[message.chat.id] = first_type_eval[
                                                        message.chat.id].pop()
            bot.send_message(message.chat.id,
                             first_type_eval_last[message.chat.id],
                             reply_markup=utils.make_first_type_review_keyboard())
        else:
            bot.send_message(message.chat.id,
                            "Слова для проверки закончились! Спасибо!",
                            reply_markup=telebot.types.ReplyKeyboardRemove())
    except:
        config.logger.error(str(message.chat.id) + " > add word crash")
        utils.send_sad_message(bot.send_message, message.chat.id)


@bot.message_handler(regexp="Оценивать слова")
def handle_second_level_review_query(message):
    try:
        config.logger.info(str(message.chat.id) + " > review_word level 2")
        bot.send_message(message.chat.id, "Вы выбрали оценку слов.\
                    Сейчас вам будут присылаться слова. \
                    Ваша задача -- оценить сложность слова.\
                    Если вы видите, что слово явно для шляпы плохое, \
                    воспользуйтесь командой /bugreport. \
                    Напоминаем критерии: " + texts.criteria_eval)
        second_type_eval[message.chat.id] = utils.make_not_eval_words_pack(
            10, message.chat.id)
        if len(second_type_eval[message.chat.id]) > 0:
            second_type_eval_last[message.chat.id] = second_type_eval[
                                                        message.chat.id].pop()
            bot.send_message(message.chat.id,
                             second_type_eval_last[message.chat.id],
                             reply_markup=utils.make_second_type_review_keyboard())
        else:
            bot.send_message(message.chat.id, "Слова закончились! Спасибо!",  reply_markup=telebot.types.ReplyKeyboardRemove())
    except:
        config.logger.error(str(message.chat.id) + " > review_words level 2 crash")
        utils.send_sad_message(bot.send_message, message.chat.id)


@bot.message_handler(regexp="""(Это хорошее слово для Шляпы|Это слово плохо подходит для Шляпы|Это слово совсем не подходит для Шляпы)""")
def handle_second_type_review_query(message):
    try:
        config.logger.info(str(message.chat.id) + " > review words level 2 query")
        marks = [
            'Это хорошее слово для Шляпы',
            'Это слово плохо подходит для Шляпы',
            'Это слово совсем не подходит для Шляпы'
                ]
        if message.chat.id in first_type_eval_last:
            utils.add_first_type_review(first_type_eval_last[message.chat.id],
                                        marks.index(message.text),
                                        message.chat.id)
        if message.chat.id in first_type_eval and len(first_type_eval[
                                                            message.chat.id]) > 0:
            first_type_eval_last[message.chat.id] = first_type_eval[
                                                        message.chat.id].pop()
            bot.send_message(message.chat.id,
                             first_type_eval_last[message.chat.id],
                             reply_markup=utils.make_first_type_review_keyboard())
        else:
            bot.send_message(message.chat.id,  "Слова закончились! Спасибо!",  reply_markup=telebot.types.ReplyKeyboardRemove())
    except:
        config.logger.error(str(message.chat.id) + " > review words level 2 query crash")
        utils.send_sad_message(bot.send_message, message.chat.id)


@bot.message_handler(regexp=('Угадано|Ошибка'))
def guessed(message):
    config.logger.info(str(message.chat.id) + " > guessed or error")
    if message.chat.id in status and message.text == 'Угадано':
        status[message.chat.id] = True
    elif message.chat.id in status and message.text == 'Ошибка':
        status[message.chat.id] = None
    else:
        utils.send_sad_message(bot.send_message, message.chat.id)


@bot.message_handler(regexp='(0|1|2|3|4){1}')
def handle_second_type_review_query(message):
    try:
        config.logger.info(str(message.chat.id) + " > 2nd type review query")
        if message.chat.id in wait_for_players_num and wait_for_players_num[
                                                            message.chat.id]:
            handle_number_of_players_query(message)
        else:
            mark = int(message.text)
            if message.chat.id in second_type_eval_last:
                utils.add_second_type_review(second_type_eval_last[
                                            message.chat.id],
                                            mark, message.chat.id)
            if message.chat.id in second_type_eval and len(second_type_eval[
                                                        message.chat.id]) > 0:
                second_type_eval_last[message.chat.id] = second_type_eval[
                                                        message.chat.id].pop()
                bot.send_message(
                    message.chat.id,
                    second_type_eval_last[message.chat.id],
                    reply_markup=utils.make_second_type_review_keyboard())
            else:
                bot.send_message(message.chat.id,  """Слова закончились!
                                                    Спасибо за помощь!""",
                                                    reply_markup=telebot.types.ReplyKeyboardRemove())
    except:
        config.logger.error(str(message.chat.id) + " > 2nd type review query crash")
        utils.send_sad_message(bot.send_message, message.chat.id)


@bot.message_handler(regexp='(0|1|2|3|4|5|6|7|8|9|10|11|12){1}')
def handle_number_of_players_query(message):
    try:
        config.logger.info(str(message.chat.id) + " > number of players query")
        if message.chat.id in wait_for_players_num and wait_for_players_num[
                                                                message.chat.id]:
            wait_for_players_num[message.chat.id] = False
            num, players = utils.parse_players_and_num(message.text)
            print(num, players)
            w_storage = words.WordsStorage(config.playable_storage_filename)
            game[message.chat.id] = hatplay.Circle(
                players_number=num,
                words_storage=w_storage,
                sender=bot.send_message,
                uid=message.chat.id,
                keyboard=utils.make_guesser_keyboard(),
                transit_keyboard=utils.make_transit_keyboard(),
                check_status=check_status,
                is_pair=game_type[message.chat.id],
                players_names=players,
                complexity=complexity[message.chat.id])
            game[message.chat.id].show()

            status[message.chat.id] = False
            game[message.chat.id].make_turn()
    except:
        config.logger.error(str(message.chat.id) + " > number of players query crash")
        utils.send_sad_message(bot.send_message, message.chat.id)


@bot.message_handler(regexp='(Просто|Средне|Сложно|Жесть)')
def handle_complexity_type(message):
    try:
        config.logger.info(str(message.chat.id) + " > complexity type")
        compl = ["Просто", "Средне", "Сложно", "Жесть"].index(message.text)
        complexity[message.chat.id] = (0.25 * compl, 0.25 * (compl + 1))
        bot.send_message(message.chat.id, "Выберите тип игры",
                         reply_markup=utils.make_play_choice_keyboard())
    except:
        config.logger.error(str(message.chat.id) + " > complexity type error")
        complexity[message.chat.id] = (0.25, 0.5)
        utils.send_sad_message(bot.send_message, message.chat.id)


@bot.message_handler(regexp='(Личная игра|Парная игра)')
def handle_game_type(message):
    try:
        config.logger.info(str(message.chat.id) + " > pair or not type")
        bot.send_message(message.chat.id, "Введите количество игроков (от 1 до 12) \
                                        и, если хотите, их имена через запятую. \
                                        \n Например, \n 3 Винтик, Шпунтик, Незнайка",  
                                        reply_markup=telebot.types.ReplyKeyboardRemove())
        if message.text == "Личная игра":
            game_type[message.chat.id] = False
        else:
            game_type[message.chat.id] = True
        wait_for_players_num[message.chat.id] = True
    except:
        config.logger.error(str(message.chat.id) + " > pair or not type crash")
        game_type[message.chat.id] = True
        wait_for_players_num[message.chat.id] = True


@bot.message_handler(regexp="""(Следующий ход|
                            Ошибка во время хода|Закончить игру)""")
def handle_game_type(message):
    try:
        config.logger.info(str(message.chat.id) + " > between turns")
        if message.chat.id not in status:
            return
        if message.text == "Следующий ход":
            if game[message.chat.id].next_turn():
                game[message.chat.id].make_turn()
            else:
                del status[message.chat.id]
                bot.send_message(message.chat.id,
                                 "Игра окончена!",
                                 reply_markup=telebot.types.ReplyKeyboardRemove())
                res, word_time = game[message.chat.id].results()
                bot.send_message(message.chat.id, res, reply_markup=telebot.types.ReplyKeyboardRemove())
        elif message.text == "Ошибка во время хода":
            bot.send_message(
                message.chat.id,
                "К сожалению, пока мы не умеем \
                редактировать раунд. Следите за обновлениями!",
                reply_markup=telebot.types.ReplyKeyboardRemove())
        elif message.text == "Закончить игру":
                del status[message.chat.id]
                bot.send_message(message.chat.id, "Игра окончена!",
                                 reply_markup=telebot.types.ReplyKeyboardRemove())
                res, word_time = game[message.chat.id].results()
                for name, points in sorted(res, key=lambda t: t[1], reverse=True):
                    bot.send_message(message.chat.id, name + ": " + str(points))
        else:
            raise
    except:
        config.logger.error(str(message.chat.id) + " > between turns crash")
        utils.send_sad_message(bot.send_message, message.chat.id)


@bot.message_handler(content_types=['text'])
def handle_word(message):
    try:
        config.logger.info(str(message.chat.id) + " > text, not sure")
        if(message.chat.id in wait_for_word and wait_for_word[message.chat.id]):
            if utils.add_new_word(message.text.strip()):
                bot.send_message(message.chat.id, "Спасибо за слово! \
                                            Оно появится в игре после проверки.",
                                            reply_markup=telebot.types.ReplyKeyboardRemove())
            else:
                bot.send_message(
                    message.chat.id,
                    "Такое слово уже есть в нашей базе :) Спасибо!",
                    reply_markup=telebot.types.ReplyKeyboardRemove())
            wait_for_word[message.chat.id] = False
        elif message.chat.id in bugreport and  bugreport[message.chat.id]:
            with open("bugreports", "a") as bugreportfile:
                bugreportfile.write(str(message.chat.id) + ">>> " + message.text + "\n")
            bugreport[message.chat.id] = False
            bot.send_message(
                message.chat.id,
                "Спасибо за замечание! Мы обязательно с этим разберёмся.",
                reply_markup=telebot.types.ReplyKeyboardRemove())
 
        else:
            raise
    except:
        config.logger.info(str(message.chat.id) + " > strange things...")
        utils.send_sad_message(bot.send_message, message.chat.id)
if __name__ == '__main__':
        bot.polling(none_stop=True)

