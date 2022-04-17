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