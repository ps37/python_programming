# Program of Space Wars
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

pi = 3.14
ship_acceleration = 0
friction_constant = -0.06
rocks = set([])
missiles = set([])
explosion_group = set([])
shoot = False
lost_lives = 0

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
    
    def set_pos(self, pos):
        self.pos = [pos[0],pos[1]]
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)

    def set_thrust(self, thrust):
        self.thrust = thrust
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
        
    def update(self):
        global ship_acceleration, friction_constant
        
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
        
    def missile_shoot(self):
        global missiles
        #get the angle of ship's tip
        ship_angle = angle_to_vector(self.angle)
        missile_x_pos = (self.pos[0]) + 45*ship_angle[0]
        missile_y_pos = (self.pos[1]) + 45*ship_angle[1]
        missile = Sprite([missile_x_pos, missile_y_pos], [8*ship_angle[0], 8*ship_angle[1]], 
                                                0, 0, missile_image, missile_info, missile_sound) 
        missiles.add(missile)
    
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
        self.collided = False
        if sound:
            #sound.rewind()
            sound.play()
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        global time
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                            self.pos, self.image_size, self.angle)
            
        elif self.animated:
            i = time % 24
            image_center_0 = (i * (2*self.image_center[0]))
            image_center_1 = self.image_center[1]
            canvas.draw_image(self.image, [image_center_0, image_center_1], self.image_size, 
                              self.pos, self.image_size, self.angle)
            time += 1
        
    def collision_detected(self, other_object):
        global lost_lives
        other_object_pos = other_object.get_pos()
        other_object_radius = other_object.get_radius()
        distance = dist(self.pos, other_object_pos)
        if distance < (self.radius + other_object_radius):
            #there is a collision
            return True
            #lost_lives += 1
        else:
            return False
    
    def update(self):
        # don't update the pos and vel for explosion
        if not self.animated:
            #update the angle based on the angular velocity of the sprite
            self.angle += self.angle_vel
            #update the position based on the velocity
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]

            # wrap around if the ship reaches the edge of the canvas
            if self.pos[0]  <= 0: # ships is at left horizontal edge
                self.pos[0] = 800
            elif self.pos[0]  >= WIDTH: # ships is at right horizontal edge
                self.pos[0] = 0

            if self.pos[1]  <= 0: # ships is at top edge
                self.pos[1] = 600
            elif self.pos[1]  >= HEIGHT: # ships is at right horizontal edge
                self.pos[1] = 0
            
        #incrementing the age of a sprite to keep track of its life span if it had one
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
        
# time interval between firing of missiles, when space bar is cotinuously pressed
i = 20

    global time, rocks, shoot, i, score, lives, lost_lives, my_ship, started, missiles
    global explosion_group
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if started:
        timer.start()
        # check for game over!
        if lives <= 0:
            started = False
        # play the sound track
        soundtrack.play()
        # draw and update ship and sprites
        my_ship.draw(canvas)
        my_ship.update()
        process_sprite_group(canvas, rocks)
        process_sprite_group(canvas, missiles)
        process_sprite_group(canvas, explosion_group)
        
        # for continuous firing of missiles when spacebar is pressed
        if i == 0:    
            if shoot:
                my_ship.missile_shoot()
            i = 20
        i -= 1
            
        if group_collision(rocks, missiles, my_ship):
            lives = lives - 1

        #draw the UI
        canvas.draw_text("Asteroids", [350, 60], 40, 'Red')
        canvas.draw_text('Lives', [50, 60], 30, 'Yellow')
        canvas.draw_text(str(lives), [80, 95], 30, 'Yellow')
        canvas.draw_text('Score', [650, 60], 30, 'Yellow')
        canvas.draw_text(str(score), [680, 95], 30, 'Yellow')
    
    #Draw the Splash image if game is not started
    if (not started):
        lives = 3
        score = 0
        rocks = set([])
        missiles = set([])
        timer.stop()
        my_ship.set_pos([WIDTH / 2, HEIGHT / 2])
        soundtrack.pause()
        soundtrack.rewind()
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
# helper function for drawing and updating a sprite group         
def process_sprite_group(canvas, sprites_group):
    global rocks, lost_lives, explosion_group, missiles
    for sprite in set(sprites_group):
        if sprite.update():
            sprites_group.remove(sprite)
        sprite.draw(canvas)
            
def group_collision(rocks_group, missiles_group, ship):
    global rocks, my_ship, score, explosion_group, missiles
    collided = False    
#loop for checking rock_group collision with missile_group
    for rock in set(rocks_group):
        for missile in set(missiles_group):
            if rock.collision_detected(missile):
                # creating an explosion image in palce of the colliding rock being removed
                rocks_group.remove(rock)
                explosion_pos = rock.get_pos()
                explosion_object = Sprite(explosion_pos, [0, 0], 0, 0, 
                                          explosion_image, explosion_info, explosion_sound)
                explosion_group.add(explosion_object)
                missiles_group.remove(missile)
                score += 1
                break
                
# loop for removing colliding rocks with the ship
    for rock in set(rocks_group):
        if rock.collision_detected(ship):
            collided = True
            explosion_pos = rock.get_pos()
            explosion_object = Sprite(explosion_pos, [0, 0], 0, 0, 
                                          explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion_object)
            rocks_group.remove(rock) 
            
    if collided:
        return True
    else:
        return False
    
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
        my_ship.set_thrust(True)
    if key == simplegui.KEY_MAP["space"]:
        shoot = True
        my_ship.missile_shoot()
                
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
        my_ship.set_thrust(False)
    if key == simplegui.KEY_MAP["space"]:
        shoot = False
        
# Mouse click handler
def mouse_click_handler(pos):
    global started
    size = splash_info.get_size()
    center = splash_info.get_center()
    splash_x1 = center[0] - WIDTH/2
    splash_x2 = center[0] + WIDTH/2
    if pos[0] > splash_x1 and pos[0] < splash_x2:
        started = True

rock_spawn_count = 0
# timer handler that spawns a rock    
def rock_spawner():
    global rocks, shoot, rock_spawn_count, my_ship
    if len(rocks) < 8:
        rock = Sprite([random.randrange(50,WIDTH-50), random.randrange(50,HEIGHT-50)], [random.choice([1,-1,0.5,-0.5]), 
                         random.choice([1,-1,0.5,-0.5])], 0, random.choice([pi/90,-pi/90,pi/60,-pi/60]), asteroid_image, asteroid_info)
        spawned_rock_center = rock.get_pos()
        ship_center = my_ship.get_pos()
        spawned_rock_radius = rock.get_radius()
        ship_radius = my_ship.get_radius()
        distance= dist(spawned_rock_center, ship_center)
        if distance > spawned_rock_radius + ship_radius:
            rocks.add(rock) 
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)
frame.set_mouseclick_handler(mouse_click_handler)

timer = simplegui.create_timer(1500.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
