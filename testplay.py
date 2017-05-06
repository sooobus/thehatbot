import config
import words
import hatplay

playable = words.WordsStorage(config.playable_storage_filename)

game = hatplay.Circle(2, playable, words_limit=5)
game.show()
print(game.individual_play())
