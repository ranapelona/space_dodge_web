import asyncio
import pygame
import time
import random
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Space Dodge")

BG = pygame.image.load("bg.jpg")
PLAYER_WIDTH = 300
PLAYER_HEIGHT = 360
PLAYER_VEL = 6
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 2
PLAYER_IMG_RAW = pygame.image.load("kid.png").convert_alpha()
PLAYER_IMG = pygame.transform.scale(
    PLAYER_IMG_RAW, (PLAYER_WIDTH, PLAYER_HEIGHT))
FONT = pygame.font.SysFont("Arial", 30)


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    draw_x = player.centerx - (PLAYER_WIDTH / 2)
    draw_y = player.botttom - PLAYER_HEIGHT
    WIN.blit(PLAYER_IMG, (draw_x, draw_y))
    for star in stars:
        pygame.draw.rect(WIN, "pink", star)
    pygame.display.update()


async def main():
    run = True
    WIN.blit(BG, (0, 0))
    pygame.display.update()
    await asyncio.sleep(0.1)
    swoosh_sound = pygame.mixer.Sound("ufo.ogg")
    swoosh_sound.set_volume(0.05)
    last_swoosh_time = 0

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    hitbox_width = 80
    hitbox_height = 80

    player = pygame.Rect(200, HEIGHT - hitbox_height - 55,
                         hitbox_width, hitbox_height)
    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False
    while run:
        await asyncio.sleep(0)
        dt = clock.tick(60)
        star_count += dt
        elapsed_time = time.time() - start_time
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x,  -STAR_HEIGHT,
                                   STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 20)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    swoosh_sound.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                swoosh_sound.play()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            mouse_x, _ = pygame.mouse.get_pos()
            if mouse_x < WIDTH / 2:
                if player.x - PLAYER_VEL > 43:
                    player.x -= PLAYER_VEL
            else:
                if player.x + PLAYER_VEL + hitbox_width <= WIDTH - 40:
                    player.x += PLAYER_VEL

        keys = pygame.key.get_pressed()
        if keys[pygame. K_LEFT] and player.x - PLAYER_VEL >= 43:
            player.x -= PLAYER_VEL
        if keys[pygame. K_RIGHT] and player.x + PLAYER_VEL + hitbox_width <= WIDTH - 40:
            player.x += PLAYER_VEL
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            draw(player, elapsed_time, stars)
            lost_text = FONT.render("You Lost !", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width() /
                     2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            await asyncio.sleep(4)
            break
        draw(player, elapsed_time, stars)
    pygame.quit()

asyncio.run(main())
