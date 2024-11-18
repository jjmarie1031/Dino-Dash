import pygame, random
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
playing = True

highScore = 0
seconds = 0
font = pygame.font.Font('lunchds.ttf', 32)
smallFont = pygame.font.Font('lunchds.ttf', 16)

# importing audio
gameOverSound = pygame.mixer.Sound('gameover.wav')
jumpSound = pygame.mixer.Sound('jumping.mp3')
jumpSound.set_volume(.2)

# Importing images
# Normal, running image
charSkinImg = pygame.image.load("run.png").convert_alpha()
charSkin = pygame.transform.scale(charSkinImg, (100, 120))
# Crouching
charCrouchImg = pygame.image.load("crouch.png").convert_alpha()
charCrouch = pygame.transform.scale(charCrouchImg, (120, 80))
# Jumping
charJumpImg = pygame.image.load("jump.png").convert_alpha()
charJump = pygame.transform.scale(charJumpImg, (100, 120))
# Crates as obstacles
crate1Img = pygame.image.load('Crate1.png').convert_alpha()
crate2Img = pygame.image.load('Crate2.png').convert_alpha()
crate3Img = pygame.image.load('Crate3.png').convert_alpha()
crate1 = pygame.transform.scale(crate1Img, (50, 100))
crate2 = pygame.transform.scale(crate2Img, (50, 160))
crate3 = pygame.transform.scale(crate3Img, (180, 120))

# importing miscellaneous images
groundImg = pygame.image.load('ground.png').convert_alpha()
ground = pygame.transform.scale(groundImg, (500, 100))
cloud1Img = pygame.image.load('cloud1.png').convert_alpha()
cloud1 = pygame.transform.scale(cloud1Img, (136, 32))
cloud2Img = pygame.image.load('cloud2.png').convert_alpha()
cloud2 = pygame.transform.scale(cloud2Img, (94, 64))

# Value initialized for image being used
currentSkin = charSkin

# Creating the player character and attributes
char = pygame.Rect(30, 600, 90, 100)
charYSpd = 0
charXSpd = 0
dead = True

# Creating rectangles for cloud movement
cloud1Rect = pygame.Rect(200, 200, 136, 32)
cloud2Rect = pygame.Rect(750, 200, 94, 64)

obstacleSpd = -10

# Menu items
dinoDash = font.render('Dino Dash', False, (255, 0, 0))
dinoDashRect = dinoDash.get_rect(center=(500, 200))
playOrNot = font.render('Press Y to play or N to exit the game!', False, (0, 0, 0))
playOrNotRect = playOrNot.get_rect(center=(500, 300))
highScoreDisplay = font.render('Highscore: ' + str(highScore) + 's', False, (0, 0, 0))
highScoreDisplayRect = highScoreDisplay.get_rect(center=(500, 400))
instructions = smallFont.render('Help the Dino avoid the crates using the WASD keys.', False, (0, 0, 0))
instructionsRect = instructions.get_rect(center=(500, 500))
instructions2 = smallFont.render('Survive as long as you can and beat the high score!', False, (0, 0, 0))
instructions2Rect = instructions2.get_rect(center=(500, 520))


# Creating classes for obstacles
class Obstacle1:
    def __init__(self):
        self.h = 100
        self.w = 50
        self.x = 1000
        self.y = 700 - self.h
        self.color = (77, 54, 15)
        self.speed = obstacleSpd
        self.img = crate1


class Obstacle2:
    def __init__(self):
        self.h = 160
        self.w = 50
        self.x = 1000
        self.y = 630 - self.h
        self.color = (77, 54, 15)
        self.speed = obstacleSpd
        self.img = crate2


class Obstacle3:
    def __init__(self):
        self.h = 120
        self.w = 180
        self.x = 1000
        self.y = 700 - self.h
        self.color = (77, 54, 15)
        self.speed = obstacleSpd
        self.img = crate3


# Variables for obstacles:
obstacleList = []
nextObstacleTime = 2000
timeInterval = 1000
lvlUpTimer = 0
frames = 0

menu_image = pygame.image.load("menu_image.png").convert_alpha()
menu_image = pygame.transform.scale(menu_image, (1000, 700))

credits_image = pygame.image.load("code.png").convert_alpha()
credits_image = pygame.transform.scale(credits_image, (1000, 700))

loading_image = pygame.image.load("loading_image.png").convert_alpha()
loading_image = pygame.transform.scale(loading_image, (1000, 700))

pygame.mixer.music.load("gamemenusound.wav")

MAIN_MENU = "main_menu"
GAME = "game"
CREDITS = "credits"
LOADING = "loading"
state = MAIN_MENU

start_button = pygame.Rect(649, 392, 246, 63)
credits_button = pygame.Rect(631, 489, 280, 62)

back_button_area = pygame.Rect(901, 643, 70, 53)

loading_start_time = None
music_playing = False
while playing == True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if keys[pygame.K_ESCAPE]:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if state == MAIN_MENU:
                if start_button.collidepoint(mouse_pos):
                    state = LOADING
                    loading_start_time = pygame.time.get_ticks()
                    pygame.mixer.music.stop()
                if credits_button.collidepoint(mouse_pos):
                    state = CREDITS

            if state == CREDITS:

                if back_button_area.collidepoint(mouse_pos):
                    state = MAIN_MENU


    if state == MAIN_MENU:
        screen.blit(menu_image, (0, 0))
        if not music_playing:
            pygame.mixer.music.play(-1, 0.0)
            music_playing = True

    if state == GAME:

        if not dead:
            frames += 1
            if frames >= 60:
                frames = 0
                seconds += 1

        # Updating displays in game
        timerDisplay = font.render('Score:' + str(seconds) + 's', False, (0, 0, 0))
        highScoreDisplay = font.render('Highscore: ' + str(highScore) + 's', False, (0, 0, 0))

        # Timer for obstacle spawn
        currentTime = pygame.time.get_ticks()
        if currentTime > nextObstacleTime and not dead:
            nextObstacleTime += timeInterval
            lvlUpTimer += 1

            # Determining which obstacle will spawn based on probability
            randomInt = random.uniform(0, 1)
            if randomInt > .6 and randomInt < .9:
                obstacleList.append(Obstacle2())
            elif randomInt < .6:
                obstacleList.append(Obstacle1())
            else:
                obstacleList.append(Obstacle3())

        # Filling screen and blitting miscellaneous surfaces
        screen.fill((150, 200, 255))
        screen.blit(ground, (0, 670))
        screen.blit(ground, (500, 670))
        screen.blit(cloud1, (cloud1Rect.x, cloud1Rect.y))
        screen.blit(cloud2, (cloud2Rect.x, cloud2Rect.y))
        screen.blit(timerDisplay, (5, 5))

        # Motion of miscellaneous surfaces
        if not dead:
            cloud1Rect = cloud1Rect.move(-1, 0)
            cloud2Rect = cloud2Rect.move(-1, 0)
        if cloud1Rect.right < 0:
            cloud1Rect.x = 1050
        if cloud2Rect.x < 0 - cloud1Rect.width:
            cloud2Rect.x = 1050

        # Drawing obstacle to screen and obstacle movement
        for obstacle in obstacleList[:]:
            obstacle.x += obstacle.speed
            pygame.draw.rect(screen, obstacle.color, pygame.Rect(obstacle.x, obstacle.y, obstacle.w, obstacle.h))
            screen.blit(obstacle.img, (obstacle.x, obstacle.y))
            # Setting up collision
            if pygame.Rect(obstacle.x, obstacle.y, obstacle.w, obstacle.h).colliderect(char):
                charYSpd = 0
                charXSpd = 0
                obstacleList = []
                if not dead:
                    gameOverSound.play()
                dead = True
                if seconds > highScore:
                    highScore = seconds
                print(highScore)

            # Removing obstacles from list if out of play
            if obstacle.x + obstacle.w < -0:
                obstacleList.remove(obstacle)

        # Character horizontal movement
        if keys[pygame.K_d] and char.right < 1000:
            charXSpd = 10
        elif keys[pygame.K_a] and char.left > 0:
            charXSpd = -10
        else:
            charXSpd = 0

        # Character vertical movement

        if char.bottom < 700:
            charYSpd += 2
        if char.bottom >= 700:
            charYSpd = 0
        if char.bottom > 700:
            char.bottom = 700
        if keys[pygame.K_w] and char.bottom >= 700 and not dead:
            charYSpd -= 30
            jumpSound.play()
        elif keys[pygame.K_s] and char.bottom < 700:
            charYSpd += 5

        # Setting up jump/crouch skins
        if keys[pygame.K_s] and not dead:
            char.h = 60
            currentSkin = charCrouch
        elif char.bottom < 700 and not keys[pygame.K_s]:
            currentSkin = charJump
            char.h = 100
        else:
            char.h = 100
            if not dead:
                currentSkin = charSkin

        if not dead:
            char = char.move(charXSpd, charYSpd)

        # increasing speed the longer the player survives
        if lvlUpTimer == 10:
            obstacleSpd += -2
            lvlUpTimer = 0
            nextObstacleTime -= 50

        if dead:
            screen.blit(dinoDash, (dinoDashRect.x, dinoDashRect.y))
            screen.blit(playOrNot, (playOrNotRect.x, playOrNotRect.y))
            screen.blit(highScoreDisplay, (highScoreDisplayRect.x, highScoreDisplayRect.y))
            screen.blit(instructions, (instructionsRect.x, instructionsRect.y))
            screen.blit(instructions2, (instructions2Rect.x, instructions2Rect.y))

        if dead and keys[pygame.K_n]:
            playing = False
        if dead and keys[pygame.K_y]:
            lvlUptimer = 0
            obstacleSpd = -10
            nextObstacleTime = currentTime + 2000
            timeInterval = 1000
            lvlUpTimer = 0
            dead = False
            obstacleList = []
            char.x = 30
            char.y = 600
            seconds = 0

        screen.blit(currentSkin, (char.x, char.y))
        # You can un-comment the line below to see the character's rectangle that determines his location and collision
        # pygame.draw.rect(screen, (0,0,0), char)


    if state == CREDITS:
        screen.blit(credits_image, (0, 0))
        if not music_playing:
            pygame.mixer.music.play(-1, 0.0)
            music_playing = True

    if state == LOADING:
        screen.blit(loading_image, (0, 0))

        if pygame.time.get_ticks() - loading_start_time >= 2500:
            state = GAME

    pygame.display.flip()
    clock.tick(60)