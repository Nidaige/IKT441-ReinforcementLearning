import time
from random import choice, random
from english_words import english_words_lower_set
import matplotlib.pyplot as plt


def generate_wordset():  # generates set of words from english_words library
    words = []
    for word in english_words_lower_set:  # for each word:
        if len(word) == 5:  # ensure 5 letters
            ok = True
            for letter in ["\'", "!", "\"", ",", "_", " "]:  # ensure no punctuation etc.
                if letter in word:
                    ok = False
            if ok:
                words.append(word)
    print("Created word list with", len(words), "words.")  # status update for number of words in list
    return words


class Agent:  # agent class, keeps track of current knowledge and expected rewards
    def __init__(self, wordlist):
        self.known_words = wordlist  # list of possible guesses
        self.weights = {}  # will hold all the different weights
        self.current_knowledge = "00000"  # current knowledge. Gets reset each game - letters known
        self.current_state = "00000"  # current state. Gets reset each game
        self.guesses_this_game = []  # holds tuples of ("guess", state-at-the-time)
        self.discount_factor = 0.99  # discount factor for rewards
        self.reward_value = 1  # reward value before discounting

    def reset(self):  # resets per-game information
        self.current_knowledge = "00000"
        self.current_state = "00000"
        self.guesses_this_game = []

    def setup_weights(self, initial_weight):   # sets up agent with list of weights for all actions for all states
        list_of_states = {}
        for i in range(32):  # for each state from "00000" to "11111":
            current_state = {}
            n = str(format(i, "05b"))  # turn iterated int into string of binary, 5 digits
            for word in self.known_words:
                current_state[word] = initial_weight  # initializes the starting weight for each word for each state
            list_of_states[n] = current_state
        self.weights = list_of_states

    def make_guess_from_weights(self):
        dict_of_available_weights = self.weights[self.current_state]
        sum_of_weights = 0
        for action in dict_of_available_weights.keys():
            sum_of_weights += self.weights[self.current_state][action]
        roll = int(random()*sum_of_weights)
        current_sum = 0
        for key in dict_of_available_weights.keys():
            current_sum += dict_of_available_weights[key]
            if current_sum >= roll:
                self.guesses_this_game.append([key, self.current_state])
                return key

    def process_feedback(self, feedback_tuple):
        self.current_knowledge = feedback_tuple[0]  # take in new knowledge on present letters
        self.current_state = feedback_tuple[1]  # take in new state binary
        correct_letters = 0  # counts correct letters based on current state. Happens each guess
        for letter in self.current_state:
            if letter != "0":
                correct_letters += 1
        if correct_letters == 5:  # if all 5 letters are correct, we are in the winning state, let's reward
            self.reward()
            return True  # we won, so we return True
        return False  # we didn't win (yet) so we return False

    def reward(self):  # handles updating of weights
        discount_factor = 1  # last (correct) guess is not discounted
        self.guesses_this_game.reverse()  # reverse order of guesses so last guess comes first
        for guessed_word in self.guesses_this_game:  # for each guess made from back to front
            self.weights[guessed_word[1]][guessed_word[0]] += self.reward_value*discount_factor  # add reward
            discount_factor *= self.discount_factor  # then multiply next reward with discount factor


class Environment:  # environment class as described above
    def __init__(self, wordlist):
        self.possible_secrets = wordlist
        self.state_transition_matrix = {}
        self.secret = "00000"
        self.reward = 1.0
        self.discount = 0.95

    # sets the current secret, called when setting up a game
    def set_secret(self, secret):
        if secret == "":
            self.secret = choice(self.possible_secrets)
        else:
            self.secret = secret

    # evaluates the current guess + the current state. Returns next state. Called whenever agent makes a guess
    def evaluate_guess(self, guessed, known_letters, current_state):
        next_state = list(current_state)  # tracks state binary 11001
        next_letters = list(known_letters)  # tracks state letters sp00k
        for letter in range(5):
            if self.secret[letter] == guessed[letter] and current_state[letter] == "0":
                next_state[letter] = 1
                next_letters[letter] = guessed[letter]
        temp_letters = ""
        temp_state = ""
        for a in range(5):
            temp_letters += str(next_letters[a])
            temp_state += str(next_state[a])
        return temp_letters, temp_state


epochs = 30000  # number of games to run (currently estimated time 1 hour training)
wins = 0
total_games = 0
initial_weight_per_word = 1
list_of_words = generate_wordset()
agent = Agent(list_of_words)
environment = Environment(list_of_words)
environment.set_secret("")
agent.setup_weights(initial_weight_per_word)
analytics = [[], []]
start_time = time.time()
old_time = time.time()
new_time = old_time
for epoch in range(epochs+1):  # for each game
    if epoch % 150 == 0 and epoch != 0:  # print status each 50th epoch
        old_time = new_time
        new_time = time.time()
        print("Epoch: ", epoch, "current accuracy is:", (wins*100)/total_games, "%. Time spent since last checkpoint: ",
              new_time-old_time, "s", "total wins: ", wins)
        analytics[0].append(epoch)
        analytics[1].append(wins/total_games)
        wins = 0
        total_games = 0
    agent.reset()
    won = False
    total_games += 1
    for rounds in range(6):
        if not won:
            guess = agent.make_guess_from_weights()
            new_letters, new_state = environment.evaluate_guess(guess, agent.current_knowledge, agent.current_state)
            feedback = (new_letters, new_state)
            won = agent.process_feedback(feedback)
            if won:
                wins += 1
end_time = time.time()
plt.title("Accuracy for last 1500 games when guessing \""+environment.secret+"\"")
plt.plot(analytics[0], analytics[1])
plt.show()
