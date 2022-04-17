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
    if M == 0:
        M = len(all_n_letter_words)
    for a in range(M):
        to_add = choice(all_n_letter_words)  # randomly choose a word
        all_n_letter_words.remove(to_add)  # remove from list of all N-letter words
        all_m_words_to_add.append(to_add)  # add to final list
    return all_m_words_to_add


def thin_valid_guesses_from_filter(indices, words, word_filter):
    indices_filtered = indices
    for index_of_word_in_valid_guesses in indices_filtered:
        word = words[index_of_word_in_valid_guesses]
        removed = False
        for letter in range(5):
            a = word_filter[0][letter]
            b = word_filter[1][letter]
            c = word_filter[2][letter]
            if a != words[index_of_word_in_valid_guesses] and not removed and a!="-":
                removed = True
                del indices_filtered[indices.index(index_of_word_in_valid_guesses)]
            elif b not in words[index_of_word_in_valid_guesses] and not removed and b!="-":
                removed = True
                del indices_filtered[indices.index(index_of_word_in_valid_guesses)]
            elif c in word and not removed:
                del indices_filtered[indices.index(index_of_word_in_valid_guesses)]
                removed = True
    return indices_filtered


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

def choice_by_weights(weights, indices):
    if (len(weights) <= 1) or len(indices) <= 1:
        return 0
    total_sum = 0
    for i in indices:
        total_sum += weights[i]
    roll = random()*total_sum
    current_sum = 0
    for value in indices:
        if current_sum >= roll:
            return value
        current_sum+=weights[value]


start_time = time.time()  # time when program started

wordlist, weightlist = create_transition_matrix_weights(generate_wordlist(5, 1500))  # create list of words and weights
pre_process_time = time.time()


accuracy = 1
total = 1
discount_value = 0.99
epochs = 470
reward_value = 50
newtime = time.time()
oldtime=time.time()
for epoch in range(epochs):  # for each game:
    if epoch % 25 == 0:  # print every 25th epoch
        oldtime = newtime
        newtime = time.time()
        print("Epoch: ", epoch, ", Time: ",newtime-oldtime, "accuracy: ", accuracy/total)
        print("Total correct guesses: ",accuracy-1)
    for secret in wordlist:
        guesses = []  # list to hold indices for each word
        for a in range(len(wordlist)):  # create list of indices to track words + weights
            guesses.append(a)
        #ground_truth = secret
        ground_truth = "print"
        guessed_words_this_round = []
        for rounds in range(6):  # for each round out of 6 per game:
            guess = choice_by_weights(weightlist,guesses)  # make a guess
            if guess == None:
                guess = 0
            guessed_words_this_round.append(guess)  # add guess to list of guesses for this game
            if wordlist[int(guess)] == ground_truth:  # if correct guess
                accuracy += 1  # increment accuracy for analytics
                discount_factor = discount_value  # copy in discount factor
                guessed_words_this_round.reverse()  # reverse list of made guesses so last (and correct) is first
                for guessed_word in guessed_words_this_round:  # for each guess made this round (reversed)
                    weightlist[guessed_word] += reward_value * discount_factor  # update weight with discount factor
                    discount_factor *= discount_value  # update discount factor
            filterstring = make_guess(wordlist[guess],ground_truth)  # get filter based on guess made
            guesses = thin_valid_guesses_from_filter(guesses,wordlist,filterstring)  # get new list of valid guesses
        total += 1  # increment total number of games


execution_time = time.time()
tempweights = weightlist
tempwords = wordlist
print("Top 10 guesses: ")
for a in range(10):
    i = tempweights.index(max(tempweights))
    print(tempwords[i], tempweights[i])
    del tempwords[i]
    del tempweights[i]


print("Pre-processing time: ",pre_process_time-start_time, ", Execution time at ", epochs," epochs: ", execution_time-pre_process_time)
print("Accuracy: ", (accuracy/total)*100, "%")
file = open("weights.txt",'w')
for a in range(len(weightlist)):
    file.writelines(str(wordlist[a]) + ": " + str(weightlist[a]))



