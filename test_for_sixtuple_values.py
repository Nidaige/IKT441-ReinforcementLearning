'''
Idea is that the probability of choosing a certain word should only be based on which guess
In a perfect MDP, each secret word will have a list of every possible combination of guesses, but this requires
X*10^19 values, and is therefore completely infeasible.

If we don't enforce the rules of the game on what guesses are possible, we will end up with a model where guesses that
have no value in the context of the game are rewarded.
For example, if the secret word is horse, and the agent guesses pizza, again, and some other "bad" guesses, before
finally guessing horse, then those bad guesses will be rewarded even though the random guess of "horse" was unrelated.

The idea of this implementation is to have each transition as a separate weight, and then try with and without
enforcing the rules of the game. The idea is that no guess is truly "invalid" as long as it is a 5 letter word in the
list, and the perfect guesser gets the word right on the first try. Instead the underlying distribution of letters in
words etc. will act as the differentiatior.
'''
from english_words import english_words_set


def generate_wordlist(N):
    all_n_letter_words = []  # will hold all words of N length
    for word in english_words_set:  # for all words in list
        if len(word) == N:  # and word.lower() not in all_N_letter_words:  # if N letters and unique
            ok = True  # ok for now
            for letter in ["\'", "!", "\"", ",", "_", " "]:
                if letter in word:  # if bad letter in word, not ok anymore
                    ok = False
            if ok:  # if word is ok, add to list
                lower = word.lower()
                all_n_letter_words.append(lower)
    return all_n_letter_words

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


sum_of_inclusions = 0
wordlist = generate_wordlist(5)
inclusions = []
for secret in wordlist:  # for every secret word
    next_guesses = []
    per_secret_inclusions = 0
    for word in wordlist:  # check every guess and compute the number of valid next guesses
        exclusion_list = wordlist
        filt = make_guess(word,secret)
        to_delete = []
        for next_word in exclusion_list:
            ok = True
            for letter in range(5):
                f2 = filt[2]
                if (f2[letter] in next_word) and ok:
                    to_delete.append(exclusion_list.index(next_word))
                    ok = False
        if len(to_delete)<0:
            for delete_me in to_delete:
                print(delete_me)
                #del exclusion_list[delete_me]
        next_guesses.append([word,len(exclusion_list)])
    s = 0
    for a in next_guesses:
        s += a[1]
    inclusions.append([secret, s])
print(inclusions)



