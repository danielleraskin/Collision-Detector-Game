#Peyton Moffatt - PM - 20936732
#Danielle Raskin - DR - 20936398

#imports modules (gives built in functions)
import pygame, sys, random
from pygame.locals import *


# Set up pygame.
pygame.init() #initializes pygame
mainClock = pygame.time.Clock() #keeps track of time 

# Set up the window. 
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
#pygame uses surfaces its what we put images on (this all sets it up)
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32) 
pygame.display.set_caption('Input')

# Set up the colors.  these are colours we can use in the display of the game (rgb values)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255,0,0)

#initialize font for letters on screen DR
font = pygame.font.Font('freesansbold.ttf', 32)

# Set up the player and food data structure.
foodCounter = 0
NEWFOOD = 45 #assigning to variable but later this means every 40 loops new food is added !! i changed to 60 so it adds less often 
FOODSIZE = 50
#rect is a rectangle, it makes the player
#parameters x dis, y dis, x width, y width
# (0,0) is top left
#makes rectangle for player (invisible only used for coordinates so it can move)
player = pygame.Rect(300, 100, 90, 90) 
#upload monkey pic for player DR
player_img = pygame.image.load('monkey.png')
#changes monkey pic to be same size as player rectangle
player_img = pygame.transform.scale(player_img, (90, 90))
#upload pic for food DR
food_img = pygame.image.load('banana.png')
#adjust size of food
food_img = pygame.transform.scale(food_img, (50, 50))

foods = []
for i in range(10):
    #randint gives random values for displacements, and foodsize
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

# Set up movement variables.
#false because initially not moving
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

#how fast it moves when it does move
MOVESPEED = 6

#Score and Countdown 
#score starts at 0 PM
score = 0
#make rectangle where score counter text will go PM
score_rectangle = pygame.Rect(0,0,100,100)
#start countdown at 30 seconds PM
countdown = 30
#make rectangle where countdown will go PM 
countdown_rectangle = pygame.Rect(180, 0, 100, 100)
#set up variables counter will use DR
frames = 40
frame_counter = 0

#uses true loop because always running until you close it 
# Run the game loop.
while True:
    # Check for events.
    for event in pygame.event.get(): 
        if event.type == QUIT: #quit is built in 
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN: #keydown is built in
            # Change the keyboard variables.
            if event.key == K_LEFT or event.key == K_a: #k_letter is the letter key
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP: #keyup is when you let go of the key (seperate event from key being pressed)
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            if event.key == K_x: #resets player in a random spot
                player.top = random.randint(0, WINDOWHEIGHT - player.height)
                player.left = random.randint(0, WINDOWWIDTH - player.width)

        if event.type == MOUSEBUTTONUP: #mouse button doesnt need seperate events for up and down
            #this adds new food to the screen
            foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))

    foodCounter += 1
    if foodCounter >= NEWFOOD: #this adds new food when the 40 loops are up (40 from assigning before)
        # Add new food.
        foodCounter = 0 #resets the counter (counts # loops so hits 40 every time)
        #adds food in random (append is a built in function of lists)
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

    # Draw the white background onto the surface.
    windowSurface.fill(WHITE)

    # Move the player.
    #uses speeds assigned before
    #makes sure player isnt touching edge of screen before moving 
    if moveDown and player.bottom < WINDOWHEIGHT: 
        player.top += MOVESPEED
    if moveUp and player.top > 0:
        player.top -= MOVESPEED
    if moveLeft and player.left > 0: 
        player.left -= MOVESPEED
    if moveRight and player.right < WINDOWWIDTH:
        player.right += MOVESPEED

    #draws monkey image onto screen PM
    #uses coordinates of player rectangle to move player
    windowSurface.blit(player_img, (player.left, player.top))

    # Check if the player has intersected with any food squares.
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            #adds one to score which is displayed on the screen for player DR
            score += 1

    # Draw the food. PM
    for i in range(len(foods)):
        windowSurface.blit(food_img, foods[i])
        
    #sets up variables so the countdown goes down every second, based on 40 frames a second in frames variable DR
    frame_counter += 1
    if frame_counter >= frames:
        frame_counter = 0
        countdown -= 1

    #this is what happens when timer runs out and game ends PM&DR
    if countdown == 0:
        windowSurface.fill(WHITE)
        #this displaes score / make texts first 
        score_text = font.render('Your Score Was: '+ str(score), True, BLACK)
        #make rectangle with coordinates on screen 
        score_rectangle = pygame.Rect(WINDOWWIDTH // 2 - 150, WINDOWHEIGHT // 2 - 50, 100, 100)
        #put the text in the rectangle 
        windowSurface.blit(score_text, score_rectangle)
        #this actually ends the game 
        while True:
            for event in pygame.event.get(): 
                if event.type == QUIT: #quit is built in 
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    #Score counter
    #make text and use score variable so it updates PM
    score_text = font.render('Score: '+ str(score), True, BLACK)
    #put text in rectangle PM
    windowSurface.blit(score_text, score_rectangle)

    #count down 
    #make countdown text using countdown variable so it updates DR
    countdown_text = font.render('Time Left: '+ str(countdown), True, BLACK)
    #put countdown text into rectangle DR
    windowSurface.blit(countdown_text, countdown_rectangle)

    pygame.display.update()
    mainClock.tick(frames) #runs 40 loops a second PM
