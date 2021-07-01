import os
import random
import pygame
pygame.init()

MIXER = pygame.mixer
MIXER.init()

W, H = 900, 600
AV_W, AV_H = 85, 70
S_W, S_H = 50, 50
START_W, START_H = W, 100
WINDOW = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Invaders")

PATH = "Space Invaders Assets"
BG_FILE_NAME = "background.jpg"
AV_W_FILE_NAME = "white avatar.jpg"
AV_B_FILE_NAME = "blue avatar.jpg"
AV_G_FILE_NAME = "green avatar.png"
AV_R_FILE_NAME = "red avatar.jpg"
SHIP_FILE_NAME = "ship.png"
START_FILE_NAME = "start.png"
AV_CHOICE_FILE_NAME = "avatars.jpg"
PAUSE_FILE_NAME = "pause screen.jpg"
GAMEOVER_FILE_NAME = "gameover.jpeg"

BG_FILE = os.path.join(PATH, BG_FILE_NAME)
BACKGROUND = pygame.transform.scale(pygame.image.load(BG_FILE), (W,H))

AV_W_FILE = os.path.join(PATH, AV_W_FILE_NAME)
AVATAR_W = pygame.transform.scale(pygame.image.load(AV_W_FILE), (AV_W, AV_H))
AV_B_FILE = os.path.join(PATH, AV_B_FILE_NAME)
AVATAR_B = pygame.transform.scale(pygame.image.load(AV_B_FILE), (AV_W, AV_H))
AV_G_FILE = os.path.join(PATH, AV_G_FILE_NAME)
AVATAR_G = pygame.transform.scale(pygame.image.load(AV_G_FILE), (AV_W, AV_H))
AV_R_FILE = os.path.join(PATH, AV_R_FILE_NAME)
AVATAR_R = pygame.transform.scale(pygame.image.load(AV_R_FILE), (AV_W, AV_H))

SHIP_FILE = os.path.join(PATH, SHIP_FILE_NAME)
SHIP = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(SHIP_FILE), 180), (S_W, S_H))

START_FILE = os.path.join(PATH, START_FILE_NAME)
START = pygame.transform.scale(pygame.image.load(START_FILE), (START_W, START_H))

AV_CHOICE_FILE = os.path.join(PATH, AV_CHOICE_FILE_NAME)
AV_CHOICE = pygame.transform.scale(pygame.image.load(AV_CHOICE_FILE), (W, 200))

PAUSE_FILE = os.path.join(PATH, PAUSE_FILE_NAME)
PAUSE = pygame.transform.scale(pygame.image.load(PAUSE_FILE), (W, H))

GAMEOVER_FILE = os.path.join(PATH, GAMEOVER_FILE_NAME)
GAMEOVER = pygame.transform.scale(pygame.image.load(GAMEOVER_FILE), (W, H))

SOUND_FILE_NAME = "bullet.mp3"
BULLET_SOUND_FILE = os.path.join(PATH, SOUND_FILE_NAME)
BULLET_SOUND = MIXER.music.load(BULLET_SOUND_FILE)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 128, 255)

FONT = pygame.font.Font("freesansbold.ttf", 60)
SCORE_HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
RESTART_CONTINUE_FONT = pygame.font.Font("freesansbold.ttf", 50)

FPS = 60
AV_SPEED = 7
SHIP_SPEED = 3
BULLET_SPEED = 5

BULLET_W, BULLET_H = 7, 14

AVATAR_DAMAGE = pygame.USEREVENT + 1
SHIP_HIT = pygame.USEREVENT + 2

def draw(x, avatar_health, score, avatar):
    WINDOW.fill(BLACK)
    WINDOW.blit(avatar, (x - AV_W // 2, H - 90))
    health_text = SCORE_HEALTH_FONT.render(f"Health: {avatar_health}", True, BLUE)
    health_text_rect = health_text.get_rect()
    health_text_rect.centerx, health_text_rect.centery = 90, 60
    WINDOW.blit(health_text, health_text_rect)
    score_text = SCORE_HEALTH_FONT.render(f"Score {score}", True, BLUE)
    score_text_rect = score_text.get_rect()
    score_text_rect.centerx, score_text_rect.centery = W - 90, 60
    WINDOW.blit(score_text, score_text_rect)

def draw_intro():
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(START, (0, 200))

def draw_pick_avatar(AVATAR_W, AVATAR_B, AVATAR_G, AVATAR_R):
    WINDOW.fill(BLACK)
    WINDOW.blit(AV_CHOICE, (0, 100))
    WINDOW.blit(pygame.transform.scale(AVATAR_W, (200, 150)), (50, 350))
    WINDOW.blit(pygame.transform.scale(AVATAR_B, (200, 150)), (250, 350))
    WINDOW.blit(pygame.transform.scale(AVATAR_G, (200, 150)), (450, 350))
    WINDOW.blit(pygame.transform.scale(AVATAR_R, (200, 250)), (650, 300))

def draw_pause():
    WINDOW.blit(PAUSE, (0, 0))
    CONTINUE_TEXT = RESTART_CONTINUE_FONT.render("PRESS C TO CONTINUE", True, WHITE)
    CONTINUE_TEXT_RECT = CONTINUE_TEXT.get_rect()
    CONTINUE_TEXT_RECT.center = W // 2, H - 150
    WINDOW.blit(CONTINUE_TEXT, CONTINUE_TEXT_RECT)

def draw_lost():
    WINDOW.blit(GAMEOVER, (0, 0))
    RESTART_TEXT = RESTART_CONTINUE_FONT.render("PRESS R TO RESTART", True, BLACK)
    RESTART_TEXT_RECT = RESTART_TEXT.get_rect()
    RESTART_TEXT_RECT.centerx, RESTART_TEXT_RECT.centery = W // 2, H - 80
    WINDOW.blit(RESTART_TEXT, RESTART_TEXT_RECT)


def move_ships(ships, av_rect, bullets):
    for ship in ships:
        WINDOW.blit(ship[0], (ship[1][0], ship[1][1]))
        if ship[1][1] > H:
            pygame.event.post(pygame.event.Event(AVATAR_DAMAGE))
            ships.remove(ship)
        if pygame.Rect(ship[1][0], ship[1][1], S_W, S_H).colliderect(av_rect):
            pygame.event.post(pygame.event.Event(AVATAR_DAMAGE))
            ships.remove(ship)
        for bullet in bullets:
            if pygame.Rect(ship[1][0], ship[1][1], S_W, S_H).colliderect(bullet):
                pygame.event.post(pygame.event.Event(SHIP_HIT))
                try:
                    ships.remove(ship)
                    bullets.remove(bullet)
                except:
                    pass

def move_bullets(bullets):
    for bullet in bullets:
        if bullet.y < 0:
            bullets.remove(bullet)
        pygame.draw.rect(WINDOW, BLUE, bullet)

def mainloop():
    on_first = True
    on_avatar = False
    lost = False
    started = False
    paused = False
    run = True
    
    clock = pygame.time.Clock()

    x = W // 2
    ship_y = S_H

    ships = []
    delay = 0
    bullets = []
    MAX_BULLETS = 6

    avatar_health = 10
    score = 0

    while run:
        clock.tick(FPS)
        av_rect = pygame.Rect(x - AV_W // 2, H - 80, AV_W+20, AV_H)
        if not on_first and not on_avatar and started and not paused:    
            draw(x, avatar_health, score, avatar)
        if not on_first and not on_avatar and started:
            move_ships(ships, av_rect, bullets)
            move_bullets(bullets)
            delay += 1

        if avatar_health == 0:
            lost = True

        if delay == 60:
            if not on_first and not paused and started and not on_avatar:
                ship_x = random.randint(50, W - 100)
                ship = [SHIP, [ship_x, ship_y]]
                ships.append(ship)
            delay = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if on_first and not on_avatar and not started:
                    on_first = False
                    on_avatar = True

                elif not on_first and on_avatar and not started and not paused:
                    m_x, m_y = pygame.mouse.get_pos()
                    if 500 > m_y > 350 and 50 < m_x < 850:
                        if 50 < m_x < 250:
                            avatar = AVATAR_W
                        if 250 < m_x < 450:
                            avatar = AVATAR_B
                        if 450 < m_x < 650:
                            avatar = AVATAR_G
                        if 650 < m_x < 850:
                            avatar = AVATAR_R
                        on_avatar = False
                        started = True

            if event.type == AVATAR_DAMAGE:
                if not lost:
                    avatar_health -= 1
            if event.type == SHIP_HIT and not lost and not paused:
                score += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS and not lost and not on_first and started and not paused:
                    bullet = pygame.Rect(av_rect.centerx - 2*BULLET_W , av_rect.centery - BULLET_H - AV_H // 2 , BULLET_W, BULLET_H)
                    bullets.append(bullet)
                    MIXER.music.play()
                if event.key == pygame.K_p and not on_first and not on_avatar and not lost:
                    paused = True
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_r and lost:
                    lost = False
                    bullets = []
                    ships = []
                    score = 0
                    x = W // 2
                    avatar_health = 10

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RIGHT] and not on_first and started and not lost and not paused:
            if x < W - AV_W:
                x += AV_SPEED
        if pressed_keys[pygame.K_LEFT] and not on_first and started and not lost and not paused:
            if x - AV_W > 0:
                x -= AV_SPEED
        
        if not on_first and not on_avatar and started and not paused:
            for Ship in ships:
                Ship[1][1] += SHIP_SPEED

        av_rect = pygame.Rect(x - AV_W // 2, H - 80, AV_W+20, AV_H)

        if on_first:
            draw_intro()

        if not on_first and on_avatar and not started:
            draw_pick_avatar(AVATAR_W, AVATAR_B, AVATAR_G, AVATAR_R)

        if paused and started:
            draw_pause()

        if lost:
            draw_lost()

        if not paused and started:
            for bullet in bullets:
                bullet.y -= BULLET_SPEED

        pygame.display.update()
            
    pygame.quit()

mainloop()