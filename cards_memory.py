# implementation of card game - Memory

import simplegui
import random

card_values1 = range(0,8)
card_values2 = range(0,8)
card_values = card_values1 + card_values2
random.shuffle(card_values)
print card_values

#positions of the first card
card_position = [10,65]

#exposed_list to keep track of list of exposed cards.
t = True
f = False
exposed = [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f]

#variable to keep track of turns of the player
turns = 0

#list variable to store previous 2 cards indices
exposed_indices = []

state = 0  #variable to keep track of mouse clicks

# helper function to initialize globals
def new_game():
    global exposed, turns, exposed_indices, state, card_values
    exposed = [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f]
    #variable to keep track of turns of the player
    turns = 0
    #list variable to store previous 2 cards indices
    exposed_indices = []
    state = 0  #variable to keep track of mouse clicks
    random.shuffle(card_values)
    
# helper to check if the mouse click is on a already opened card
def ignore_click(mouse_pos):
    for index in range(len(card_values)):
        #iterate through all the cards
        if exposed[index] == t:
            #check if a card is already exposed
            x = index*50
            x1 = (index*50) + 50
            if mouse_pos[0]>x and mouse_pos[0]<x1: 
                #check if the mouse click is on a exposed card
                return True #do nothing!
            
    #if the functions reaches this point, then click is not on opened card
    return False  #proceed with the execution

# helper routine to check if the previous to cards are different
def compare_and_pop():
    global exposed, exposed_indices
    
    if card_values[exposed_indices[0]] != card_values[exposed_indices[1]]:
        # close the previous 2 clicked cards, as they are different
        exposed[exposed_indices[0]] = f
        exposed[exposed_indices[1]] = f
        
    # if the two cards are equal don't bother to close the previous two cards
    
    # pop the first 2 exposed indices to as they are checked already
    exposed_indices.pop(0)
    exposed_indices.pop(0)

# define event handlers
def mouseclick(pos):
    global exposed, exposed_indices, state, turns
    print state
    if not ignore_click(pos):
    #if here then the click is on a closed card
    # for every click, expose the card and store the index
        for index in range(len(card_values)):
                x = index*50
                x1 = (index*50) + 50
                if pos[0]>x and pos[0]<x1: #a card is exposed
                    exposed[index] = t
                    exposed_indices.append(index) #add the index of the exposed card
                    print exposed_indices

        if state == 1:
            # player has used one turn for every 2nd mouse click on a closed card
            turns += 1

        state += 1 #increase the mouse click count

        if state == 3:
            #check for 3rd click
            state = 1
            #compare the 2 cards at this click to close them.
            compare_and_pop()
                
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global card_position
    #draw the card values
    for value in range(len(card_values)):
        canvas.draw_text(str(card_values[value]), (card_position[0], card_position[1]), 40, 'White')
        card_position[0] = card_position[0] + 50
    
    #draw green rectangles for not exposed values.
    for value in range(len(card_values)):
        if(exposed[value] == t):
            canvas.draw_text(str(card_values[value]), (card_position[0], card_position[1]), 40, 'White')
        elif(exposed[value] == f):
            x = value*50
            x1 = (value*50) + 50
            #draw a green rectangle
            canvas.draw_polygon([[x, 0], [x1, 0], [x1, 99], [x, 99]], 1, 'Red', 'Green')
            
    card_position[0] = 10
    label.set_text("Turns = " + str(turns))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
label = frame.add_label("Turns = 0")
label.set_text("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
frame.add_button("Reset", new_game)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric