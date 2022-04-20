'''Idea:
States are defined by whether you have confirmed each letter.
Examples for the word "Spark":
00000
0000k
000r0
000rk
sp00k
spa00
spar0
spa0k
spark

these would be generalized as
00000
00001
00010
00011
11001
11100
11110
11101
11111
 in a dictionary kept by the agent
 to track individual lists of guesses and their observed reward

Agent tracks:
- Known letters (Confirmed)
- Each state with its own list of actions and reward
- Words it has guessed for a given game of wordle
- Current state

Environment tracks:
- Current state
- Probability of transitioning from state X to state Y in a state transition matrix
- Reward and discount factor
- Also gives reward when agent guesses correctly (and nothing when 6 rounds without correct pass)
'''
from random import choice, random
from english_words import english_words_lower_set

def generate_wordset():
    words = []
    for word in english_words_lower_set:
        if len(word)==5:
            ok = True
            for letter in ["\'", "!", "\"", ",", "_", " "]:
                if letter in word:
                    ok = False
            if ok:
                words.append(word)
    print("Created word list with",len(words),"words.")
    return words

class Agent:  # agent class, as described above
    def __init__(self, wordlist):
        self.known_words = wordlist  # list of possible guesses
        self.weights = {}  # will hold all the different weights
        self.current_knowledge = "00000"  # current knowledge. Gets reset each game
        self.current_state = "00000"  # current state. Gets reset each game
        self.valid_guesses = wordlist
        self.guesses_this_game = []  # holds tuples of ("guess", state-at-the-time)

    def reset(self):
        self.current_knowledge = "00000"
        self.current_state = "00000"

    def setup_weights(self):   # sets up agent with list of weights for all actions for all states
        list_of_states = {}
        for i in range(32):
            current_state = {}
            n = str(format(i, "05b"))
            for word in self.known_words:
                current_state[word] = 1
            list_of_states[n] = current_state
        self.weights = list_of_states

    def make_guess_from_weights(self):
        dict_of_available_weights = self.weights[self.current_state]
        sum_of_weights = 0
        for action in dict_of_available_weights.keys():
            sum_of_weights += self.weights[self.current_state][action]
        roll = int(random()*sum_of_weights)
        print(roll, sum_of_weights)

class Environment:  # environment class as described above
    def __init__(self, wordlist):
        self.possible_secrets = wordlist
        self.state_transition_matrix = {}
        self.current_state = "00000"
        self.secret = "00000"
        self.reward = 1.0
        self.discount = 0.95

    # sets the current secret, called when setting up a game
    def set_secret(self, secret):
        if secret=="":
            self.secret = choice(self.possible_secrets)
        else:
            self.secret = secret

    # evaluates the current guess + the current state. Returns next state. Called whenever agent makes a guess
    def evaluate_guess(self,guess, known_letters, current_state):
        next_state = known_letters
        for letter in range(5):
            if self.secret[letter] == guess[letter] and next_state[letter]=="*":
                next_state[letter] = guess[letter]
                current_state[letter] = 1


list_of_words = generate_wordset()
agent = Agent(list_of_words)
environment = Environment(list_of_words)
environment.set_secret("")
agent.setup_weights()
# print(agent.weights["10000"]["horse"])
epochs = 250  # number of games to run
for epoch in range(epochs):  # for each game
    if epoch % 50 == 0 and epoch != 0:  # print status each 50th epoch
        print("Epoch: ", epoch)
    agent.make_guess_from_weights()
