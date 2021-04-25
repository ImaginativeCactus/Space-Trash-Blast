

# Intro to GameDev - Week 9 Multiple Levels
# Students will learn to:
# detect mouse clicks, add buttons, transition between multiple screen 

import pgzrun
import random

WIDTH = 1000
HEIGHT = 600

SCOREBOX_HEIGHT = 60

#keep track of score
score = 0
junk_collect = 0
level = 0
level_screen = 0
lvl2_LIMIT = 10
lvl3_LIMIT = 30

#sprite speeds
JUNK_SPEED = 5
SATELLITE_SPEED = 3
DEBRIS_SPEED = 3
LASER_SPEED = -5  # lasers are moving towards the left on screen

BACKGROUND_IMG = "space trash logo"
PLAYER_IMG = "player_ship"
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris2"
LASER_IMG = "laser_red"
START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"

def init():
    global player, junks, lasers, satellite, debris
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH - 15, HEIGHT/2)

    # initialize junk sprites
    junks = []  # list to keep track of junks
    for i in range(5):
        junk = Actor(JUNK_IMG)  # create a junk sprite
        x_pos = random.randint(-500, -50)
        y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
        junk.topright = (x_pos, y_pos)  # rect_position = (x, y)
        junks.append(junk)

    # initialize lasers
    lasers = []
    player.laserActive = 1

    # initialize satellite
    satellite = Actor(SATELLITE_IMG)  # create sprite
    x_sat = random.randint(-500, -50)
    y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat, y_sat)  # rect_position

    # initialize debris
    debris = Actor(DEBRIS_IMG)
    x_deb = random.randint(-500, -50)
    y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb, y_deb)

# initialize title screen buttons
start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 425)
instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)

def on_mouse_down(pos):
    global level, level_screen
    if start_button.collidepoint(pos):
        level = 1
        level_screen = 1
        print("start button pressed!")
    if instructions_button.collidepoint(pos):
        level = -1
        print("instructions button pressed!")
        
# game loop
init()

def update():
    global score, junk_collect, level, level_screen, BACKGROUND_IMG
    if junk_collect == lvl2_LIMIT:  # level 2
        level = 2
    if junk_collect == lvl3_LIMIT:  # level 3
        level = 3
    if level == -1: # instructions screen
        BACKGROUND_IMG = "level 1 background"

    if score >= 0 and level >= 1:
        if level_screen == 1:  # level 1 title screen
            BACKGROUND_IMG = "level 1 background"
            if keyboard.RETURN == 1:
                level_screen = 2
        if level_screen == 2:  # level 1 gameplay
            updatePlayer()  # calling our player update function
            updateJunk()  # calling junk update function
        if level == 2 and level_screen <= 3:  # level 2 title
            BACKGROUND_IMG = "level 2 background"
            level_screen = 3
            if keyboard.RETURN == 1:
                level_screen = 4
        if level_screen == 4:  # level 2 gameplay
            updatePlayer()
            updateJunk()
            updateSatellite()
        if level == 3 and level_screen <= 5:  # level 3 title
            level_screen = 5
            BACKGROUND_IMG = "level three background"
            if keyboard.RETURN == 1:
                level_screen = 6
        if level_screen == 6:  # level 3 game play
            updatePlayer()
            updateJunk()
            updateSatellite()
            updateDebris()
            updateLasers()

    if score < 0 or level == -2:  # game over or end game
        if keyboard.RETURN == 1:
            BACKGROUND_IMG = "space trash logo"
            score = 0
            junk_collect = 0
            level = 0
            init()
    
def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0,0))
    if level == -1:
        start_button.draw()
        show_instructions = "Use UP and DOWN arrow keys to move your player\n\npress SPACEBAR to shoot"
        screen.draw.text(show_instructions, midtop=(WIDTH/2, 70), fontsize=35, color="white")
    if level == 0:
        start_button.draw()
        instructions_button.draw()
    if level >= 1:
        player.draw()  # draw player sprite on screen
        for junk in junks:
            junk.draw()  # draw junk sprite on screen
    if level >= 2:
        satellite.draw()
    if level == 3:
        debris.draw()
        for laser in lasers:
            laser.draw()
            
    # game over screen
    if score < 0:
        game_over = "GAME OVER\npress ENTER to play again"
        screen.draw.text(game_over, center=(WIDTH / 2, HEIGHT / 2), fontsize=60, color="white")

    #draw some text on the screen
    show_score = "SCORE: " + str(score)  # remember to convert score to a string
    screen.draw.text(show_score, topleft=(436, 25), fontsize=35, color="black")
    show_collect_value = "JUNK: " + str(junk_collect)
    screen.draw.text(show_collect_value, topleft=(750, 25), fontsize=35, color="black")
    
    if level >= 1:
        show_level = "LEVEL " + str(level)
        screen.draw.text(show_level, topright=(375, 15), fontsize=35, color="white")

    if level_screen == 1 or level_screen == 3 or level_screen == 5:
        show_level_title = "LEVEL " + str(level) + "\nPress ENTER to continue..."
        screen.draw.text(show_level_title, center=(WIDTH/2, HEIGHT/2), fontsize=70, color="white")

# make separate functions for each of our sprites
def updatePlayer():
    # check for user input
    if keyboard.up == 1:
        player.y += -5  # moving up is in negative y direction
    elif keyboard.down == 1:
        player.y += 5  # moving down is in the postive y direction

    # prevent player from moving off screen
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

    #check for firing lasers
    if keyboard.space == 1 and level == 3:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)  # this is a function from the template code

def updateJunk():
    global score, junk_collect
    for junk in junks:
        junk.x += JUNK_SPEED

        collision = player.colliderect(junk)
        if junk.left > WIDTH or collision == 1:
            x_pos = random.randint(-500, -50)
            y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)
            
        # collisions between player and junk
        if collision:
            score += 1  # update the score
            junk_collect += 1

def updateSatellite():
    global score
    satellite.x += SATELLITE_SPEED  # or just put 3

    collision = player.colliderect(satellite)
    if satellite.left > WIDTH or collision == 1:
        x_sat = random.randint(-500, -50)
        y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision == 1:
        score += -10

def updateDebris():
    global score
    debris.x += DEBRIS_SPEED  # or just put 3

    collision = player.colliderect(debris)
    if debris.left > WIDTH or collision == 1:
        x_deb = random.randint(-500, -50)
        y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if collision == 1:
        score += -10

def updateLasers():
    global score
    for laser in lasers:
        laser.x += LASER_SPEED
        # remove laser if moves off screen
        if laser.right < 0:
            lasers.remove(laser)
        #check for collisions
        if satellite.colliderect(laser) == 1:
            lasers.remove(laser)
            x_sat = random.randint(-500, -50)
            y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score += - 5  # decrease the score
        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            x_deb = random.randint(-500, -50)
            y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 5  # increase the score
    
# activating lasers (template code)____________________________________
player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list
        
pgzrun.go()
