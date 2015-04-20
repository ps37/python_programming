# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        cards_contents = ""
        # return a string representation of a hand
        for card in self.cards:
            cards_contents += str(card.get_suit()) + str(card.get_rank()) + " "
        return "Hand contains " + cards_contents  

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        values_of_cards = 0
        count_of_aces = 0
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        for i in range(len(self.cards)):
            rank = self.cards[i].get_rank()
            # count, if we find an Ace.
            if rank == 'A':
                count_of_aces += 1
            values_of_cards = values_of_cards + VALUES[rank]

        if count_of_aces == 0:  #no aces in the hand
            return values_of_cards
        else:                   #there are aces in the hand
            if (values_of_cards + 10) <= 21:
                return values_of_cards + 10
            else:
                return values_of_cards
        
    def draw(self, canvas, vertical_distance):
        for card in self.cards:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.get_rank()), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.get_suit()))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [(60 + (self.cards.index(card))*CARD_SIZE[0] + 
                                                                  (self.cards.index(card))*20), vertical_distance], CARD_SIZE)
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.card_s = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit,rank)
                self.card_s.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_s)

    def deal_card(self):
        # deal a card object from the deck
        return random.choice(self.card_s)
    
    def __str__(self):
        # return a string representing the deck
        string_of_cards = ""
        for i in range(len(self.card_s)):
            string_of_cards += str(self.card_s[i].get_suit()) + str(self.card_s[i].get_rank()) + " "
        return "Deck contains " + string_of_cards        

# global variables of card sets.
deck = Deck()
player_hand = Hand()
dealer_hand = Hand()
    
#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    if in_play:
        outcome = "You Loose the current round!!"
        score -= 1
        in_play = False
        
    elif not in_play:
        outcome = "Hit or Stand?"
        # empty both player's and dealer's hands!!
        deck = Deck()
        player_hand = Hand()
        dealer_hand = Hand()

        # shuffle the created deck
        deck.shuffle()
        # add 1 card each to player and the dealer Twice
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        in_play = True

def hit():
    global outcome, in_play, score
    if in_play:
        if player_hand.get_value() <= 21: # hand is in play
            # give extra card to the player
            player_hand.add_card(deck.deal_card())

        if player_hand.get_value() > 21: # if busted!   
            # busted. so assign a message to outcome, update in_play and score
            outcome = "You are Busted! " + "New deal?"
            in_play = False
            score = score - 1
       
def stand():
    global outcome, score, in_play
    #outcome = "Hit or Stand?"
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while(dealer_hand.get_value() < 17):
            dealer_hand.add_card(deck.deal_card())
    
        # check if the dealer is busted
        if dealer_hand.get_value() > 21:
            outcome = "Dealer is Busted! " + "New deal?"
            score += 1
        else:
            # assign a message to outcome, update in_play and score
            if player_hand.get_value() <= dealer_hand.get_value():
                outcome = "You Loose!! " + "New deal?"
                score = score - 1
            else:
                outcome = "You Win!! " + "New deal?"
                score += 1
                
    in_play = False  
        
# draw handler    
def draw(canvas):
    global card_back, CARD_CENTER, in_play
    # Draw title
    canvas.draw_text("Black Jack!", [220, 50], 40, 'Yellow')        
    player_hand.draw(canvas, 450)    
    if in_play:
    # draw the card's back
        dealer_hand.draw(canvas, 250)
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, 
                      [60, 250], CARD_SIZE)
    elif not in_play:
    #draw dealer's hand
        dealer_hand.draw(canvas, 250)        
    # draw score
    canvas.draw_text("Your score "+str(score), [400, 100], 25, 'White')
    canvas.draw_text(outcome, [300, 350], 20, 'Black')
    canvas.draw_text("Player's Hand ", [30, 390], 20, 'Blue')
    canvas.draw_text("Dealer's Hand ", [30, 190], 20, 'Blue')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric