# Step 1: Create wordle environment that takes in guess, returns value and method for filtering possible guesses
# Step 2: Create agent to randomly guess among valid words

import random
from english_words import english_words_set

def Generate_WordList(N):
    all_N_letter_words = []  # will hold all words
    for word in english_words_set:  # for all words in list
        if len(word)==N and word.lower() not in all_N_letter_words:  # if N letters and unique
            ok = True  # ok for now
            for letter in ["\'", "!", "\"", ",", "_", " "]:
                if letter in word:  # if bad letter in word, not ok anymore
                    ok = False
            if ok: # if word is ok, add to list
                lower = word.lower()
                all_N_letter_words.append(lower)
    return all_N_letter_words

class Environment:
    def __init__(self, discount_rate, reward_size):
        self.discount_rate = discount_rate
        self.reward_size = reward_size
        self.wordlist = Generate_WordList(5)

    def new_game(self):
        truth = random.choice(self.wordlist)
    # Rewards agent for correct guess
    def reward(self, guesses_this_round):
        print("Rewarding ",guesses_this_round, " with discount rate ",self.discount_rate," and reward size ",self.reward_size)

    # Evaluates agent's guess, gives feedback and/or reward
    def evaluate_guess(self,guess):
        print("Evaluating guess ",guess)
        # Reward part

        # Filtering part


class Agent:
    def __init__(self):
        self.wordlist = Generate_WordList(5)
        self.valid_wordlist = self.wordlist
    # Handles the incoming reward and feedback from environment
    def handle_reward(self,reward,feedback):
    # Update Weights
        print("Handling reward")
    # Filter possible guesses

# Setup environment and agent

environment = Environment(discount_rate=.99,reward_size=.15)
agent = Agent

# Training loop


# Evaluation loop

