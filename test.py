import words

playable = words.WordsStorage("playable_words")


reviewer = words.Reviewer("on_review", "new_words")
print(playable.check_complexity("выборка"))
print(playable.check_complexity("выборка"))
reviewer.show_marks("выборка")
reviewer.show_goodness_marks("выборка")
reviewer.add_mark("выборка", 2)
reviewer.add_mark("выборка", 2)
reviewer.add_mark("выборка", 2)
reviewer.show_marks("выборка")
reviewer.transit_evaluated(playable)
print(playable.check_complexity("выборка"))

#reviewer.add_mark("фибрилляция", 3)
#reviewer.add_mark("фибрилляция", 2)
#reviewer.show_marks("фибрилляция")
#reviewer.transit_evaluated(playable)
#print(playable.check_complexity("фибрилляция"))
#reviewer.add_mark("фибрилляция", 3)
#reviewer.transit_evaluated(playable)
#print(playable.check_complexity("фибрилляция"))


#print(playable.take_hat(100, 0.6, 0.7))
