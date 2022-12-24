# Coding Challenge 3, hangman.py
# Name: Rohan Shrestha
# Student No: NP03CS4S210094

# Hangman Game

import random
import string
from string import ascii_lowercase

WORDLIST_FILENAME = "words.txt"

# Responses to in-game events
responses = [
    "I am thinking of a word that is {0} letters long",
    "Congratulations, you won!",
    "Your total score for this game is: {0}",
    "Sorry, you ran out of guesses. The word was: {0}",
    "You have {0} guesses left.",
    "Available letters: {0}",
    "Good guess: {0}",
    "Oops! That letter is not in my word: {0}",
    "Oops! You've already guessed that letter: {0}",
    "Please guess a letter: ",
]


# to choose random word from the list of words
def choose_random_word(all_words):
    return random.choice(all_words)


# to load the words from file to a list
def load_words():
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME,'r')
    wordlist =[] 
    for line in inFile:
           line = line.split()
           wordlist.extend(line)
    print(" ", len(wordlist), "words loaded.")
    return wordlist


#to load the words automatically when running the program (gloabal list variable wordlist)
wordlist = load_words()


#to check if the entire word is guessed or not
def is_word_guessed(word, letters_guessed):
    for letter in word:
              if letter not in letters_guessed:
                     return False
    return True


#to show how many letters have been guessed by far
def get_guessed_word(word, letters_guessed):
    guessed_word = []
    check = 0
    for letter in word:
           if letter in letters_guessed:
                guessed_word.append(letter)
                check += 1
           else:
                guessed_word.append("_ ")
    return "".join(guessed_word)


#to get the remaining letters from the alphabets
def get_remaining_letters(letters_guessed):
    letters_guessed_in_str = ''.join(letters_guessed)
    #set is used to convert the strings into set 
    rem_in_set = set(ascii_lowercase) - set(letters_guessed_in_str.lower())
    rem_sorted_in_set = sorted(rem_in_set)
    rem_sorted_in_str = ''.join(rem_sorted_in_set)

    return rem_sorted_in_str


#to get the score of the user
def get_score(name):
    fname = name.split()[0]
    lname = name.split()[-1]

    try:
        score_file = open('scores.txt','r')
    except FileNotFoundError:
        return 0

    scores =[] 
    for data in score_file:
        data = data.split()
        scores.append(data)


    for list_items in scores:
        if fname in list_items and lname in list_items:
            high_score = list_items[0]
            return high_score

    return 0
    

#to save the score of the user
def save_score(name, score):
    fname = name.split()[0]
    lname = name.split()[-1]
    scores =[] 

    #try block to read the scores file 
    try:
        score_file = open('scores.txt','r')
        for data in score_file:
            data = data.split()
            scores.append(data)

        #exists flag 
        exists = False

        for list_items in scores:
            if fname in list_items and lname in list_items:
                list_items[0] = score
                exists = True #the flag is changed in case the user data was previously stored
            
        score_file.close()
        write_in_score_file = open("scores.txt", "w")
        for list_items in scores:
            write_in_score_file.write(str(list_items[0]) + " " + list_items[1] + " " + list_items[2] + "\n")
        
        #if it is a new user, the data is stored
        if exists == False:
            write_in_score_file.write(str(score) + " " + fname + " " + lname + "\n")

        write_in_score_file.close()

    #if the scores file does not exist, a new file is created and data is written
    except:
        write_in_score_file = open("scores.txt", "w")
        write_in_score_file.write(str(score) + " " + fname + " " + lname+ "\n")
        write_in_score_file.close()

    
    
#to show the scores and names of the users from file
def view_leaderboard():
    try:
        #reading the scores file and storing the data in scores[] list
        score_file = open('scores.txt','r')
        scores =[] 
        for data in score_file:
            data = data.split()
            scores.append(data)

        print("Score\tName")
        print("------------------------------")
        for list_items in scores:
            print(list_items[0] + "\t" + list_items[1] + " " + list_items[2])

        menu()
    except FileNotFoundError:
        #in case there is no scores file
        print("There is no data to be shown in the leaderboard.")
        menu()


    
#start the game by choosing a random word from the list of words
def play_game():
    word = choose_random_word(wordlist)
    hangman(word)


#the robust menu for the users
def menu():
    user_choice = input("Do you want to Play (p) view the leaderboard (l) or quit (q): ")
    if (user_choice.lower() == "p"):
        play_game()
    elif (user_choice.lower() == "l"):
        view_leaderboard()
    elif (user_choice.lower() == "q"):
        print("Thanks for playing, goodbye!")
        exit()
    else:
        print("Invalid input! ")
        menu()


#the first welcome message when starting the program
def welcome_message():
    print("Welcome to Hangman Ultimate Edition")
    menu()


#to ask the user to save their new high score or not
def ask_to_save(name, score):
    ans = input("A new personal best! Would you like to save your score(y/n): ")
    if ans.lower() == "y":
        save_score(name, score)
        print("Ok, your score has been saved.")
        menu()
    elif ans.lower() == "n": 
        menu()
    else:
        print("Invalid input")
        ask_to_save(name, score)


#the main hangman game
def hangman(word):
    fname = input("What is your first name: ")
    lname = input("What is your last name: ")
    name = fname + " " + lname
    print("I am thinking of a word that is {} letters long".format(len(word)))
    print("-------------")
    user_guesses = []
    no_of_guesses = 10

    #the guessing part of the game continues until the user guesses the word or runs out of chances
    while True:
        if is_word_guessed(word, user_guesses):
            print(responses[1])
            score = len(set(word)) * no_of_guesses
            print(responses[2].format(score)) 
            prev_score = int(get_score(name))
            #in case the user gets a high score, asking them to whether store it or not
            if score > prev_score:
                ask_to_save(name, score)
            else:
                menu()
        #to break out of the loop in case the number of chances are over
        if(no_of_guesses == 0):
               print(responses[3].format(word))
               menu()
        print(responses[4].format(no_of_guesses))
        print(responses[5].format(get_remaining_letters(user_guesses)))
        user_input = (input(responses[9]))

        #logic to check if the guessed letter is correct or not
        if user_input.isalpha():
            user_input_letter = user_input.lower()
            #if the user has already guessed the letter
            if user_input_letter in user_guesses:  
                if user_input_letter in word:
                    print(responses[8].format(get_guessed_word(word, user_guesses)))
                else:
                    print("Oops! You've already guessed that incorrect letter: {}".format(get_guessed_word(word, user_guesses))) 
            #if the user guess is a new letter and is correct
            elif user_input_letter in word:
                user_guesses.append(user_input_letter)
                print(responses[6].format(get_guessed_word(word, user_guesses)))
            #if the user guess is new and is incorrect 
            else: 
                user_guesses.append(user_input_letter)
                print(responses[7].format(get_guessed_word(word, user_guesses)))
                #in case the incorrect guess is a vowel, guess decrement = 2, else 1
                if user_input_letter in ('a', 'e', 'i', 'o', 'u'):
                    no_of_guesses -= 2
                else:
                    no_of_guesses -= 1
        else:
            print("Your input is invalid")
            no_of_guesses -= 1
        print("--------------------")  
    menu()


# Driver function for the program
if __name__ == "__main__":
    welcome_message()