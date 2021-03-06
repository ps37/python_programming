# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

pi = 3.14
ship_acceleration = 0
friction_constant = -0.08
#rocks
missiles = []
shoot = False
score = 0
lives = 5

#dictionary of keyboard left and righ keys
horizontal_keys = {"left" : -1.8*pi/60, "right": 1.8*pi/60}

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        # wrap around if the ship reaches the edge of the canvas
        if self.pos[0]  <= 0: # ships is at left horizontal edge
            self.pos[0] = 800
        elif self.pos[0]  >= WIDTH: # ships is at right horizontal edge
            self.pos[0] = 0
        #print self.pos[0]
        
        if self.pos[1]  <= 0: # ships is at top edge
            self.pos[1] = 600
        elif self.pos[1]  >= HEIGHT: # ships is at bottomedge
            self.pos[1] = 0
        #print self.pos[1]
        
        if self.thrust == True:
            #play the sound of ship accelerating
            ship_thrust_sound.play()
            # change the image of the ship with thrusters
            my_ship.image_center[0] = 135
            my_ship.image_center[1] = 45
        elif self.thrust == False:
            ship_thrust_sound.pause()
            my_ship.image_center[0] = 45
            my_ship.image_center[1] = 45    
        canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
        
    def update(self):
        global ship_acceleration, friction_constant
        # update the angular velocity of the ship
        self.angle += self.angle_vel
        # get the x,y components of the ship's orientation.
        forward_vector = angle_to_vector(self.angle)
        #resolve the scceleration in forward vector direction and add acceleration and friction to the velocity
        self.vel[0] += ship_acceleration*forward_vector[0] + friction_constant*self.vel[0]
        self.vel[1] += ship_acceleration*forward_vector[1] + friction_constant*self.vel[1]
        #update the position based on the velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        # wrap around if the ship reaches the edge of the canvas
        if self.pos[0]  <= 0: # ships is at left horizontal edge
            self.pos[0] = 800
        elif self.pos[0]  >= WIDTH: # ships is at right horizontal edge
            self.pos[0] = 0
        #print self.pos[0]
        
        if self.pos[1]  <= 0: # ships is at top edge
            self.pos[1] = 600
        elif self.pos[1]  >= HEIGHT: # ships is at right horizontal edge
            self.pos[1] = 0
        #print self.pos[1]
        
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
    def update(self):
        #update the angle based on the angular velocity of the sprite
        self.angle += self.angle_vel
        
        #update the position based on the velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
# time interval between firing of missiles, when space bar is cotinuously pressed
i = 20

def draw(canvas):
    global time, rocks, shoot, i, score, lives
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    # draw the rocks
    #for rock in rocks:
    rocks.draw(canvas)
    # for continuous firing of missiles when spacebar is pressed
    if i == 0:    
        if shoot:
            missile_shoot()
        i = 20
    i -= 1
    #draw the missiles
    for missile in missiles:
        missile.draw(canvas)
    # update ship and sprites
    my_ship.update()
    #update the rocks
    #for rock in rocks:
    rocks.update()
    #update the missiles    
    for missile in missiles:
        missile.update()
#draw the score and lives on the canvas
    canvas.draw_text("Asteroids", [350, 60], 40, 'Red')
    canvas.draw_text('Lives = ' + str(lives), [50, 60], 30, 'Yellow')
    canvas.draw_text('Score = ' + str(score), [650, 60], 30, 'Yellow')

#Helper function for shooting a missile
def missile_shoot():
    global missiles
    #get the angle of ship's tip
    ship_angle = angle_to_vector(my_ship.angle)
    missile_x_pos = (my_ship.pos[0]) + 45*ship_angle[0]
    missile_y_pos = (my_ship.pos[1]) + 45*ship_angle[1]
    missile = Sprite([missile_x_pos, missile_y_pos], [2.8*ship_angle[0], 2.8*ship_angle[1]], 
                                            0, 0, missile_image, missile_info, missile_sound) 
    missiles.append(missile)
    
# key down handler
def key_down_handler(key):
    global ship_acceleration, shoot, horizontal_keys
    for i in horizontal_keys:
        if key == simplegui.KEY_MAP[i]:
            my_ship.angle_vel = horizontal_keys[i] 
    if key == simplegui.KEY_MAP["up"]:
        global ship_acceleration
        # change the position of the ship by accelerting
        ship_acceleration = 1
        my_ship.thrust = True
    if key == simplegui.KEY_MAP["space"]:
        shoot = True
        missile_shoot()
                
# key down handler
def key_up_handler(key):
    global ship_acceleration, shoot
    # stop rotating the ship by not changing it pos.
    for i in horizontal_keys:
        if key == simplegui.KEY_MAP[i]:
            my_ship.angle_vel = 0
    #my_ship.image_center = ship_info.get_center()
    if key == simplegui.KEY_MAP["up"]:
        #No more acceleration
        ship_acceleration = 0
        my_ship.thrust = False 
    if key == simplegui.KEY_MAP["space"]:
        shoot = False

# timer handler that spawns a rock    
def rock_spawner():
    global rocks, shoot
    rocks = Sprite([random.randrange(1,WIDTH), random.randrange(1,HEIGHT)], [random.choice([1,-1,0.5,-0.5]), random.choice([1,-1,0.5,-0.5])], 
                  0, random.choice([pi/90,-pi/90]), asteroid_image, asteroid_info)
    #rocks.append(rock)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rocks = Sprite([random.randrange(1,WIDTH), random.randrange(1,HEIGHT)], [random.choice([1,-1,0.5,-0.5]), random.choice([1,-1,0.5,-0.5])], 
                  0, random.choice([pi/90,-pi/90]), asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)

timer = simplegui.create_timer(5000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
