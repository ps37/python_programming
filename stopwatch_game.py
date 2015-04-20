# template for "Stopwatch: The Game"

import math
import simplegui

# define global variables
interval = 100
tenths_of_second = 0
a = 0
b = 0
c = 0
d = 0
number_of_attempts = 0
successful_attempts = 0
timer_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(tenths_of_second):
    #global tenths_of_second = 0
    global a
    global b
    global c
    global d
    
    a = tenths_of_second / 600     #gives the quotient, which is minutes
    if(a > 9):                     #gives 'a' part of format
        a = 0
    
    remainder1 = tenths_of_second % 600     #this gives remander: seconds
    b = remainder1 / 100                    #gives the 'b' part of format
    if(b > 5):
        b = 0
    
    remainder2 = remainder1 % 100   #this gives remaining part of seconds
    c = remainder2 / 10            #gives the 'c' part of format
    if(c > 9):
        c = 0
    
    d = remainder2 % 10            #gives the 'd' part of format
    if(d > 9):
        d = 0
             
    return str(a) + ':' + str(b) + str(c) + '.' + str(d)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    global timer_running
    timer_running = True
    
def stop():
    timer.stop()
    global timer_running
    global number_of_attempts
    global successful_attempts
    #condition for whole number time and only then increse successful attemepts
    if ((d == 0) and (timer_running)): 
        successful_attempts += 1
        
    #condition to check if timer is running, if not running don't increase number of attempts   
    if(timer_running):
        number_of_attempts += 1
        
    timer_running = False
    
def reset():
    global tenths_of_second
    global a
    global b
    global c
    global d
    global number_of_attempts
    global successful_attempts
    tenths_of_second = 0
    a = 0
    b = 0
    c = 0
    d = 0
    number_of_attempts = 0
    successful_attempts = 0
    timer.stop()

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tenths_of_second
    tenths_of_second += 1
    format(tenths_of_second)

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(tenths_of_second), (149, 149), 30, 'Red')
    #to draw the score on upper right corner
    score = str(successful_attempts) + '/' + str(number_of_attempts)
    canvas.draw_text(score, (250, 20), 20, 'Green')
    
# create frame
frame = simplegui.create_frame('Stop Watch', 300, 300)

# register event handlers
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(interval, timer_handler)
button1 = frame.add_button('Start', start)
button2 = frame.add_button('Stop', stop)
button3 = frame.add_button('Reset', reset)

# start frame
frame.start()

# Please remember to review the grading rubric
