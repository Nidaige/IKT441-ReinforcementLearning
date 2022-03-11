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
                if lower!="exit":
                    all_N_letter_words.append(lower)
    return all_N_letter_words

def Pick_Word_From_Wordlist(wordlist):
    return random.choice(wordlist)

def Filter_Guess(guess, M):  # filters out bad guesses
    if len(guess)>M:
        print("guess too long, try again...")
        return False
    if len(guess)<M:
        print("guess too short, try again...")
        return False
    for letter in guess:
        if letter not in "abcdefghijklmnopqrstuvwxyz":
            print("Invalid letter detected: ",letter, "try again...")
            return False
    return True

def Evaluate_Guess(the_guess,correct_letters,answer):  # evaluates guess, handles logic
    correct = ""
    incorrect = ""
    for lc in range(len(the_guess)):  # first, identify correctly placed letters
        if the_guess[lc] in answer:  # is the letter in the word?
            if the_guess[lc] == answer[lc]:  # is the letter correctly placed?
                if correct_letters[lc]=="-":  # is the letter already known?
                    correct+= the_guess[lc]  # no, so we add from the guess
                    incorrect+="-"
                else:
                    correct+=correct_letters[lc]
                    incorrect+="-"
                        # yes, so we add from the correctly placed ones
            else:  # letter is incorrectly placed
                if incorrect.count(the_guess[lc]) < answer.count(the_guess[lc]):
                    incorrect += the_guess[lc]
                else:
                    incorrect += "-"
                correct+="-"
        else:
            incorrect += "-"
            correct += "-"
    return correct,incorrect


def Wordle(rounds, word_length):
    true_word = Pick_Word_From_Wordlist(Generate_WordList(word_length))
    correct = "----"
    victory = False
    for round in range(rounds):
        print("Round: ",round+1,"/",rounds)
        guess = input("Make a guess: ")
        if (guess=="exit"):
            print("Goodbye!")
            exit(0)
        while(not Filter_Guess(guess,word_length)):
            guess = input("Make a guess: ")
            if (guess == "exit"):
                print("Goodbye!")
                exit(0)
        correct,incorrect = Evaluate_Guess(guess,correct,true_word)
        if guess==true_word:
            print("Correct!")
            victory = True
            break
        else:
            print("Correctly placed letters:   ",correct)
            print("Incorrectly placed letters: ",incorrect)
    if victory:
        print("Congratulations! You won!")
    else:
        print("The word was ",true_word)
        print("You lost... Too bad, better luck next time...")
    replay = input("Play again? Y/N: ")
    if replay=="Y" or replay=="y":
        Wordle(rounds,word_length)
    else:
        print("Goodbye!")
        exit(0)

def main():
    print("Welcome to wordle! The objective is to guess the secret word.")
    print("You can unveil clues about the word by guessing other words, so choose your guesses with care!")
    print("And if you ever get tired of playing, just enter the word \"exit\" to leave.")
    print("----------")
    rounds = input("How many attempts do you want per word? ")
    if (rounds == "exit"):
        print("Goodbye!")
        exit(0)
    word_length = input("And how long words do you want to play with? ")
    if (word_length == "exit"):
        print("Goodbye!")
        exit(0)
    try:
        rounds = int(rounds)
        word_length = int(word_length)
        Wordle(rounds, word_length)
    except:
        exit()

main()






