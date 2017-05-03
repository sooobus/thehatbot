import words

playable = words.WordsStorage("playable_words")


reviewer = words.Reviewer("on_review", "new_words")

reviewer.transit_good()
"""
for w in reviewer.get_all_on_goodness_review():
    print(w)
    reviewer.show_goodness_marks(w)

for w in reviewer.get_all_on_complexity_review():
    print(w)
    reviewer.show_marks(w)
"""
