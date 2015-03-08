# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

secret_number = 0
remaining_guesses = 0
num_range = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global num_range
    global remaining_guesses
    global secret_number
    if(num_range == 100):
        print "New Game. Range is from 0 to 100"
        #global remaining_guesses
        remaining_guesses = 7
        print "Number of remaining guesses is", remaining_guesses
        print ""
        #global secret_number
        secret_number = random.randrange(0, num_range)
    elif(num_range == 1000):
        print "New Game. Range is from 0 to 1000"
        #global remaining_guesses
        remaining_guesses = 10
        print "Number of remaining guesses is", remaining_guesses
        print ""
        #global secret_number
        secret_number = random.randrange(0, num_range)

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global num_range
    num_range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here 
    ip = int(guess)
    print "Guess was",ip
    global secret_number
    global remaining_guesses
    remaining_guesses = remaining_guesses - 1 
    print "Number of remaining guesses is", remaining_guesses
    if(secret_number < ip):
        if(remaining_guesses > 0):
            print "lower! \n" 
    elif(secret_number > ip):
        if(remaining_guesses > 0):
            print "higher! \n"
    elif(secret_number == ip):
        #a game is completed
        print "Correct! \n"
        new_game()
    if(remaining_guesses <= 0):
        #a game is completed here also
        print "You ran out of guesses. The number was", secret_number
        print ""
        new_game()
    
# create frame
frame = simplegui.create_frame('Guess the number', 100, 200, 200)

# register event handlers for control elements and start frame
button1 = frame.add_button('Range [0,100)', range100, 100)
button2 = frame.add_button('Range [0, 1000)', range1000, 100)
inp = frame.add_input('input_guess:', input_guess, 100)

# call new_game 
new_game()

# always remember to check your completed program against the grading rubric
