# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
WILDCARD = "*"
HAND_SIZE = 7 #originally set this to 6 set it back to 7 for testing is_valid_again

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word_len=len(word)
    product_of_points=0
    sum_of_points=0
    second_result=(7*word_len)-(3*(n-word_len))
    if word_len == 0:
        product_of_points=0
    else:
        lower_word=word.lower()
        #print(lower_word) #printing lower case version of the original word for testing purposes.
        for letter in lower_word:
            try:
                sum_of_points+=SCRABBLE_LETTER_VALUES[letter]
            except KeyError:
                #if there is a WILDCARD value you get zero points
                sum_of_points+=0
        if second_result <= 1:
            product_of_points=sum_of_points*1
        else:
            product_of_points=sum_of_points*second_result
    return product_of_points

    #pass  # TO DO... Remove this line when you implement this function

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    hand[WILDCARD] = hand.get(WILDCARD,0)+1
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand
# testing
# for x in range(5):
#     print(deal_hand(HAND_SIZE))

# Problem #2: Update a hand by removing letters
#
def update_hand(hand,word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    copy_hand = hand.copy()
    word=word.lower() #was having errors with the letters not being in the correct case for comparison, convert string word to be lowercase
    dict_word = get_frequency_dict(word)
    for letter in hand:
        if letter in dict_word:
            copy_hand[letter]=copy_hand[letter]-dict_word[letter]
            if copy_hand[letter] < 0:
                copy_hand[letter]=0
    #looping over the original hand that was passed in and removing from the copy_hand
    for letter in hand:
        if copy_hand[letter]==0:
            del copy_hand[letter]
    return copy_hand
    #pass  # TO DO... Remove this line when you implement this function

#print(update_hand({'e': 1, 'v': 2, 'n': 1, 'i': 1, 'l': 2},'Evil'))
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    index=0
    word=word.lower()
    dict_word=get_frequency_dict(word)
    index = word.find(WILDCARD)
    if word_list.count(word) > 0:
        Status = False
        #word that doesnt have wildcard character in it
        for letter in dict_word:
            try:
                if dict_word[letter]!=hand[letter]:
                    break
                else:
                    Status=True
            except KeyError:
                Status=False
                break
    elif index != -1:
        #word that does have wildcard character in it
        #print(word)
        Status = False
        for vowel in VOWELS:
            #word[index]=vowel cant do this strings are immutable
            word=word[:index]+vowel+word[index+1:] #have to insert the string
            #print(word)
            if word_list.count(word)>0:
                for letter in dict_word:
                    try:
                        if dict_word[letter] != hand[letter]:
                            break
                        else:
                            Status = True
                    except KeyError:
                        Status = False
                        break
    return Status
    #pass  # TO DO... Remove this line when you implement this function
#testing modified version
# print(is_valid_word("honey",{'n': 1, 'h': 1, '*': 1, 'y': 1, 'd': 1, 'w': 1, 'e': 2},load_words()))
# print(is_valid_word("h*ney",{'n': 1, 'h': 1, '*': 1, 'y': 1, 'd': 1, 'w': 1, 'e': 2},load_words()))
# print(is_valid_word("fe*d",{"f":1,"w":2,"e":1,"z":1,"d":1,"*":1},load_words()))
# print(is_valid_word("f*ed",{"c":2,"d":1,"e":1,"f":1,"s":1,"*":1},load_words()))
# print(is_valid_word("feed",{"f":1,"e":2,"d":1,"z":1,"s":1,"*":1},load_words()))
# print(is_valid_word("j*b",{"o":1, "e":1, "*":1, "j":1, "g":1, "b":1 },load_words()))
# print(is_valid_word("her*",{"h":1,"e":1,"t":1,"f":1,"*":1,"r":1,"x":1},load_words()))
# print(is_valid_word("here",{"h":1,"e":2,"f":1,"*":1,"r":1,"x":1},load_words()))

# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length_hand=0
    for key in hand:
        length_hand+=hand[key]
    return length_hand
    # pass  # TO DO... Remove this line when you implement this function
# print(calculate_handlen({'n': 1, 'h': 1, '*': 1, 'y': 1, 'd': 1, 'w': 1, 'e': 2}))
# print(calculate_handlen({"c":1,"w":1,"o":1,"z":1,"s":1,"*":1}))
def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    TOTAL_SCORE=0
    while True:
        print("Current Hand: ",end="")
        display_hand(hand)
        user_input = input("Enter word, or '!!' to indicate that you are finished: ")
        if user_input=="!!":
            print("Total score for this hand: ", TOTAL_SCORE)
            break
        else:
            Status=is_valid_word(user_input,hand,word_list)
            if Status==True:
                played_score=get_word_score(user_input,calculate_handlen(hand))
                TOTAL_SCORE+=played_score
                print(user_input,"earned",played_score,"points.","Total: ",TOTAL_SCORE,"points")
            elif Status == False:
                print("That is not a valid word. Please choose another word.")
            hand=update_hand(hand,user_input)
        if len(hand)==0:
            print("Ran out of letters. Total Score: ",TOTAL_SCORE)
            break
    return TOTAL_SCORE
#for testing
# print(play_hand({"h":1,"e":1,"t":1,"f":1,"*":1,"r":1,"x":1},load_words()))
# print(play_hand({"h":1,"e":2,"f":1,"*":1,"r":1,"x":1},load_words()))


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    copy_hand = hand.copy()
    letters_to_choose=VOWELS+CONSONANTS
    random_addition=random.choice(letters_to_choose)
    #print(copy_hand)
    try:
        if hand[letter] > 0:
            #letter in hand
            count=hand[letter]
            del copy_hand[letter]
            copy_hand[random_addition]=count
    except KeyError:
        pass
    return copy_hand
    #pass  # TO DO... Remove this line when you implement this function
# for testing purposes
# print(substitute_hand({"a":1,"j":1,"e":2,"f":1,"*":1,"r":1,"x":1},"e"))
# print(substitute_hand({"a":1,"k":1,"e":2,"f":1,"*":1,"r":1,"x":1},"z"))
# print(substitute_hand({"a":1,"j":1,"e":2,"f":1,"*":1,"r":1,"x":1},"a"))
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    TOTAL_SCORE=0
    HAND_SCORE=0
    REPLAY_SCORE=0
    number_hands=input("Enter total number of hands: ")
    for series in range(int(number_hands)):
        sub_or_no = False
        hand=deal_hand(HAND_SIZE)
        print("Current Hand: ",end="")
        display_hand(hand)
        if sub_or_no == False:
            #hasn't been asked if they want to substitute a letter
            sub_input=input("Would you like to substitute a letter? ")
            if sub_input.lower()=="yes":
                sub_or_no=True
                letter=input("What letter would you like to replace: ")
                hand=substitute_hand(hand,letter)
            else:
                #dont substitute a letter
                sub_or_no=True
        HAND_SCORE=play_hand(hand,word_list)
        print("----------")
        replay_or_no=input("Would you like to replay the hand? ")
        if replay_or_no.lower()=="yes":
            REPLAY_SCORE=play_hand(hand, word_list)
            if REPLAY_SCORE >= HAND_SCORE:
                HAND_SCORE=REPLAY_SCORE
        TOTAL_SCORE+=HAND_SCORE
    print("----------")
    print("Total Score over all hands: ",TOTAL_SCORE)
    #print("play_game not implemented.") # TO DO... Remove this line when you implement this function
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
