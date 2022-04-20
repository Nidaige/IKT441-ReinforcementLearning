from time import time
from random import random, choice

from english_words import english_words_set
import nltk
from english_words import english_words_lower_set
def generate_wordlist(N):  # retrieves all N-letter words from the english_words library
    all_n_letter_words = []  # will hold all words of N length
    for word in english_words_lower_set:  # for all words in list
        if len(word) == N:  # and word.lower() not in all_N_letter_words:  # if N letters and unique
            ok = True  # ok for now
            for letter in ["\'", "!", "\"", ",", "_", " "]:
                if letter in word:  # if bad letter in word, not ok anymore
                    ok = False
            if ok and word not in all_n_letter_words:  # if word is ok, add to list
                '''lower = word.lower()
                all_n_letter_words.append(lower)'''
                all_n_letter_words.append(word)
    print(len(all_n_letter_words))
    return all_n_letter_words

def initialize_weights(list_of_words):  # returns initial weights corresponding to given list of words
    w = []
    for word in range(len(list_of_words)):
        w.append(1)
    return w


def choice_by_weights(list_of_weights, list_of_words):
    if (len(list_of_weights) <= 1) or len(list_of_words) <= 1:
        return 0
    total_sum = sum(list_of_weights)
    '''for i in range(len(list_of_words)):
        total_sum += list_of_weights[i]'''
    roll = random()*total_sum
    current_sum = 0
    for word in list_of_words:
        if current_sum >= roll:
            return word
        current_sum += weights[list_of_words.index(word)]


initial_time = time()
wordlist = generate_wordlist(5)
weights = initialize_weights(wordlist)
secret = choice(wordlist)
print(secret)
epochs = 12000
reward = 50
#discount_factor = 0.95
accuracy = 0
total = 0
pre_processing_time = time()
hundred_epoch_time_old = time()
hundred_epoch_time_new = time()
scores = []
epochlist = []
for epoch in range(epochs):  # for each epoch/games to play
    if epoch % 100 == 0 and epoch != 0:
        hundred_epoch_time_old = hundred_epoch_time_new
        hundred_epoch_time_new = time()
        print("Epoch: ",epoch, ", time spent on last 100: ",hundred_epoch_time_new-hundred_epoch_time_old,"s. Accuracy for last 100: ",accuracy/total)
        scores.append(accuracy/total)
        epochlist.append(epoch)
    total += 1
    guesses = []  # list of guesses made this game
    discount_factor_for_this_game = 1.0  # fresh discount factor
    for guessing_round in range(6):  # for each round in the game
        guess = choice_by_weights(weights, wordlist)
        if guess == secret:
            accuracy += 1
            weights[wordlist.index(guess)] += reward

post_game_time = time()
imax = weights.index(max(weights))
wmax = wordlist[imax]
print("Most successful word: ", wmax, " with total reward of: ",weights[imax],". Time spent training: ",post_game_time-pre_processing_time,"s")
import matplotlib.pyplot as plt
plt.plot(epochlist,scores)
plt.show()