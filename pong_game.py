# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [0,0]
ball_vel = [0,0]

#center of the pad positions
paddle1_pos = [PAD_WIDTH/2, HEIGHT/2]
paddle2_pos = [WIDTH-PAD_WIDTH/2, HEIGHT/2]
#velocities of the pads
paddle1_vel = [0,0]
paddle2_vel = [0,0]
direction = bool

# scores
score_right = 0
score_left = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel       #these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]  #spawning the ball in the middle of the canvas
    
    #based on the direction key pressed ball's initial velocity is determined
    if direction == RIGHT:
        ball_vel = [+random.randrange(2, 4), -random.randrange(2, 4)]
    elif direction == LEFT:
        ball_vel = [-random.randrange(2, 4), -random.randrange(2, 4)]
    else:
        ball_vel = [0,0]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score_left, score_right  # these are ints
    score_left = 0
    score_right = 0
    spawn_ball(45)

    #button handler for restart button
def restart():
    new_game()

def draw(canvas):
    global score_left, score_right, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
# draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "Red")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
# update paddle's vertical position, keep paddle on the screen
    #changing the paddle 1 position
    paddle1_pos[1] += paddle1_vel[1]
    
    if paddle1_pos[1] - PAD_HEIGHT/2 <= 0:
        #constaraining pad 1 to top edge
        paddle1_pos[1] = PAD_HEIGHT/2
        
    if paddle1_pos[1] + PAD_HEIGHT/2 >= HEIGHT - 1:
        #constaraining pad 1 to bottom edge
        paddle1_pos[1] = (HEIGHT) - PAD_HEIGHT/2
   
    #changing the paddle 2 position 
    paddle2_pos[1] += paddle2_vel[1]
    
    if paddle2_pos[1] - PAD_HEIGHT/2 <= 0:
        #constaraining pad 1 to top edge
        paddle2_pos[1] = PAD_HEIGHT/2
        
    if paddle2_pos[1] + PAD_HEIGHT/2 >= HEIGHT - 1:
        #constaraining pad 1 to bottom edge
        paddle2_pos[1] = (HEIGHT) - PAD_HEIGHT/2
    
# collide and reflect off of edges of the canvas and the pads
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        # It touches left edge of the canvas, check for collision with paddle 1 
        if ((paddle1_pos[1] - PAD_HEIGHT/2) <= (ball_pos[1]) <= (paddle1_pos[1] + PAD_HEIGHT/2)):
            ball_vel[0] += 0.3 * ball_vel[0]
            ball_vel[0] = - ball_vel[0]
        else:
        # If no collision, spawn it right 
            spawn_ball(RIGHT)
            score_right = score_right + 1 #player at right got a point

    if ball_pos[0] >= ((WIDTH - 1) - (BALL_RADIUS + PAD_WIDTH)):
        # It touches right edge of the canvas, check for collision with paddle 2 
        if ((paddle2_pos[1] - PAD_HEIGHT/2) <= (ball_pos[1]) <= (paddle2_pos[1] + PAD_HEIGHT/2)):
            ball_vel[0] += 0.3 * ball_vel[0] 
            ball_vel[0] = - ball_vel[0]
        else:
        # If no collision, spawn it left 
            spawn_ball(LEFT)
            score_left = score_left + 1   #player at left got a point
            
    # check for collisions with vertical edges of the canvas 
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    if ball_pos[1] >= ((HEIGHT - 1) - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
        
# update ball's center position 
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
# draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
# draw paddles
    #paddle 1
    canvas.draw_line([paddle1_pos[0], paddle1_pos[1] - PAD_HEIGHT/2],[paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT/2], PAD_WIDTH, "Yellow")    
    #paddle 2
    canvas.draw_line([paddle2_pos[0], paddle2_pos[1] - PAD_HEIGHT/2],[paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT/2], PAD_WIDTH, "Yellow")     
# draw scores
    canvas.draw_text(str(score_left), [150, 50], 40, 'White')
    canvas.draw_text(str(score_right), [450, 50], 40, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["left"]:
        spawn_ball(LEFT)
    if key == simplegui.KEY_MAP["right"]:
        spawn_ball(RIGHT)
    if key == simplegui.KEY_MAP["up"]:
        #change the velocity of right pad2 to move in up direction
        paddle2_vel[1] = -4
    if key == simplegui.KEY_MAP["down"]:
        #change the velocity of right pad2 to move in down direction
        paddle2_vel[1] = +4
    if key == simplegui.KEY_MAP["w"]:
        #change the velocity of left pad1 to move in up direction
        paddle1_vel[1] = -4
    if key == simplegui.KEY_MAP["s"]:
        #change the velocity of left pad1 to move in down direction
        paddle1_vel[1] = +4
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel[1] = 0
    paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', restart, 100)

# start frame
new_game()
frame.start()
