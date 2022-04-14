''' Tests how fast we can filter based on a guess'''
from random import choice, random
from english_words import english_words_set
import time


def generate_wordlist(N, M):
    all_n_letter_words = []  # will hold all words of N length
    all_m_words_to_add = []  # will hold all M words of N length to use
    for word in english_words_set:  # for all words in list
        if len(word) == N:  # and word.lower() not in all_N_letter_words:  # if N letters and unique
            ok = True  # ok for now
            for letter in ["\'", "!", "\"", ",", "_", " "]:
                if letter in word:  # if bad letter in word, not ok anymore
                    ok = False
            if ok:  # if word is ok, add to list
                lower = word.lower()
                all_n_letter_words.append(lower)
    for a in range(M):
        to_add = choice(all_n_letter_words)  # randomly choose a word
        all_n_letter_words.remove(to_add)  # remove from list of all N-letter words
        all_m_words_to_add.append(to_add)  # add to final list
    return all_m_words_to_add


def thin_valid_guesses_from_filter(words,word_filter):
    new_wordlist = []
    for word in words:
        for r in range(5):
            if (word_filter[0][r] == word[r]) and word not in new_wordlist:  # if correct letter
                new_wordlist.append(word)
            elif (word_filter[1][r] in word) and word not in new_wordlist:  # if incorrectly placed letter
                new_wordlist.append(word)
        # check for not containing wrong letter
        ok = True
        for letter in word_filter[2]:
            if letter in word:
                ok = False
        if ok and word not in new_wordlist:
            new_wordlist.append(word)
    return new_wordlist


def make_guess(guessed,truth):
    # [0]: correctly placed letters     [1]: incorrectly placed letters [2] wrong letters (not in word)
    filters = [["-", "-", "-", "-", "-"], ["-", "-", "-", "-", "-"], ["-", "-", "-", "-", "-"]]
    for letter in range(5):
        if guessed[letter] == truth[letter]:  # if correctly placed
            filters[0][letter] = guessed[letter]
        elif (guessed[letter] in truth) and not guessed[truth.index(guessed[letter])] == truth[truth.index(guessed[letter])]:
            filters[1][letter] = guessed[letter]
        else:
            filters[2][letter] = guessed[letter]
    return filters


def create_transition_matrix_weights(list_of_words):
    all_words = []
    all_weights = []
    for w in list_of_words:
        all_words.append(w)
        all_weights.append(1.0)
    return all_words, all_weights


start_time = time.time()
wordlist = generate_wordlist(5,1500)
list_of_words, list_of_weights = create_transition_matrix_weights(wordlist)
pre_process_time = time.time()
guesses = wordlist
accuracy = 0
total = 0
discount_value = 0.99
for epoch in range(250):
    ground_truth = choice(wordlist)
    guessed_words_this_round = []
    if epoch % 25 == 0:
        print("Epoch: ", epoch)
    for rounds in range(6):
        guess = choice(guesses)
        guessed_words_this_round.append(guess)
        if guess == ground_truth:  # if correct guess
            accuracy += 1
            discount_factor = discount_value
            guessed_words_this_round.reverse()
            for guessed_word in guessed_words_this_round:
                list_of_weights[list_of_words.index(guessed_word)] += 5*discount_factor
                discount_factor *= discount_value
        filterstring = make_guess(guess,ground_truth)
        guesses = thin_valid_guesses_from_filter(wordlist,filterstring)
    total += 1

tempweights = []
tempwords = []
for a in range(len(list_of_words)):
    i = list_of_weights.index(max(list_of_weights))
    print(i, list_of_weights[i],list_of_words[i])
    tempweights.append(list_of_weights[i])
    tempwords.append(list_of_words[i])
    del list_of_weights[i]
    del list_of_words[i]

for a in range(len(list_of_words)):
    print(tempwords[a], tempweights[a])

execution_time = time.time()
print("Pre-processing time: ",pre_process_time-start_time, ", Execution time at 250 epochs: ", execution_time-pre_process_time)
print("Accuracy: ", (accuracy/total)*100, "%")


