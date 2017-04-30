import words
import config

playable = words.WordsStorage(config.playable_storage_filename)
review = words.Reviewer(config.unreviewed_storage_filename)


#for i in range(3, 12):
#    playable.add_from_csv("words" + str(i) + ".csv")
playable.show_stats()
playable.clear_storage()
playable.show_stats()

playable.add_from_csv("words.csv")
for i in range(3, 13):
    print(i)
    playable.add_from_csv("words" + str(i) + ".csv")

print(playable.check_complexity('шимоза'))

print(playable.take_hat(30, 0.8, 0.9))
