import random
import pygame
from shooter import Shooter
from zombie import Zombie
from bullet import Bullet

pygame.init()
ts = 64
#just barely fits height without pushing too far away from a square
size = (870, 704)
#make the screen
screen = pygame.display.set_mode(size)
#set actual game surface
gs = pygame.Surface((832, 704))
#make the window say game name
pygame.display.set_caption('Zombie CQB')
#set background color for the edges that are not covered by game surface
background = (69, 65, 65)

#set up gs
grass = pygame.image.load(r"kenney_top-down-shooter\PNG\Tiles\tile_06.png")
for x in range(0, 13):
    for y in range(0, 11):
        gs.blit(grass, (x * ts, y * ts))

top_left = pygame.image.load(r'kenney_top-down-shooter\PNG\Tiles\tile_181.png')
#gs.blit(top_left,(0,0))
top_right = pygame.image.load(r"kenney_top-down-shooter\PNG\Tiles\tile_182.png")
bot_left = pygame.image.load(r"kenney_top-down-shooter\PNG\Tiles\tile_208.png")
bot_right = pygame.image.load(r"kenney_top-down-shooter\PNG\Tiles\tile_209.png")

# Midline calculations for gs (832 x 704)
mid_x = gs.get_width() // 2   # 416
mid_y = gs.get_height() // 2  # 352

# Fonts and Menu UI setup
title_font = pygame.font.SysFont(None, 78)
subtitle_font = pygame.font.SysFont(None, 34)
button_font = pygame.font.SysFont(None, 42)
hud_font = pygame.font.SysFont(None, 32)

# Button rect positioned in screen coordinates (centered on the 870x704 window)
menu_button = pygame.Rect(0, 0, 240, 60)
menu_button.center = (size[0] // 2, mid_y + 70)

# Create sprite groups
player = Shooter(mid_x - 50, mid_y)
player_group = pygame.sprite.Group(player)

zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

score = 0
flash_timer = 0.0


def spawn_zombies():
    """Spawns 3 to 8 zombies at random edges of the game surface."""
    count = random.randint(3, 8)
    w, h = gs.get_width(), gs.get_height()
    margin = ts // 2  # Keep sprite centers inside gs bounds (32px from edges)

    for _ in range(count):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = random.randint(margin, w - margin), margin
        elif edge == "bottom":
            x, y = random.randint(margin, w - margin), h - margin
        elif edge == "left":
            x, y = margin, random.randint(margin, h - margin)
        else:  # right
            x, y = w - margin, random.randint(margin, h - margin)

        zombies.add(Zombie(x, y))


def start_new_game():
    """Resets player, score, clears old bullets/zombies, and spawns the first wave."""
    global score, flash_timer
    score = 0
    flash_timer = 0.0
    player.pos = pygame.math.Vector2(mid_x - 50, mid_y)
    player.rect.center = (mid_x - 50, mid_y)
    zombies.empty()
    bullets.empty()
    spawn_zombies()


def draw_start_screen():
    """Draws the start menu overlay on top of the grass map."""
    overlay = pygame.Surface(gs.get_size(), pygame.SRCALPHA)
    overlay.fill((20, 20, 25, 175))
    gs.blit(overlay, (0, 0))

    title_surf = title_font.render("ZOMBIE CQB", True, (240, 240, 240))
    title_rect = title_surf.get_rect(center=(mid_x, mid_y - 90))
    gs.blit(title_surf, title_rect)

    controls_surf = subtitle_font.render("Move: WASD   |   Aim & Shoot: Mouse", True, (200, 200, 200))
    controls_rect = controls_surf.get_rect(center=(mid_x, mid_y - 20))
    gs.blit(controls_surf, controls_rect)

    screen.fill(background)
    screen.blit(gs, (19, 0))

    mouse_pos = pygame.mouse.get_pos()
    btn_color = (90, 170, 90) if menu_button.collidepoint(mouse_pos) else (65, 135, 65)
    pygame.draw.rect(screen, btn_color, menu_button, border_radius=10)
    pygame.draw.rect(screen, (230, 230, 230), menu_button, width=2, border_radius=10)

    btn_text = button_font.render("PLAY", True, (255, 255, 255))
    screen.blit(btn_text, btn_text.get_rect(center=menu_button.center))


def draw_game_over_screen():
    """Draws the red impact flash followed by the Game Over overlay."""
    bullets.draw(gs)
    player_group.draw(gs)
    zombies.draw(gs)

    overlay = pygame.Surface(gs.get_size(), pygame.SRCALPHA)
    if flash_timer > 0:
        overlay.fill((220, 30, 30, 210))
    else:
        overlay.fill((35, 10, 10, 195))
    gs.blit(overlay, (0, 0))

    title_surf = title_font.render("GAME OVER", True, (245, 75, 75))
    title_rect = title_surf.get_rect(center=(mid_x, mid_y - 90))
    gs.blit(title_surf, title_rect)

    score_surf = subtitle_font.render(f"Zombies Eliminated: {score}", True, (235, 235, 235))
    score_rect = score_surf.get_rect(center=(mid_x, mid_y - 20))
    gs.blit(score_surf, score_rect)

    screen.fill(background)
    screen.blit(gs, (19, 0))

    mouse_pos = pygame.mouse.get_pos()
    btn_color = (190, 70, 70) if menu_button.collidepoint(mouse_pos) else (150, 50, 50)
    pygame.draw.rect(screen, btn_color, menu_button, border_radius=10)
    pygame.draw.rect(screen, (230, 230, 230), menu_button, width=2, border_radius=10)

    btn_text = button_font.render("PLAY AGAIN", True, (255, 255, 255))
    screen.blit(btn_text, btn_text.get_rect(center=menu_button.center))


clock = pygame.time.Clock()
gs_rect = gs.get_rect()
game_state = "start"

running = 1
while running:
    dt = clock.tick(60) / 1000.0

    # Event handling
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

        if game_state in ("start", "game_over"):
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if menu_button.collidepoint(e.pos):
                    start_new_game()
                    game_state = "playing"
            elif e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                start_new_game()
                game_state = "playing"

        elif game_state == "playing":
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                target_pos = (mouse_x - 19, mouse_y)
                bullets.add(Bullet(player.pos, target_pos))

    # Redraw grass tiles on gs
    for x in range(0, 13):
        for y in range(0, 11):
            gs.blit(grass, (x * ts, y * ts))

    if game_state == "start":
        draw_start_screen()

    elif game_state == "playing":
        # Update player, zombies, and bullets
        player_group.update(dt, gs_rect, (19, 0))
        zombies.update(dt, gs_rect, player.pos)
        bullets.update(dt, gs_rect)

        # Check bullet collisions with zombies (True, True deletes both on hit)
        hits = pygame.sprite.groupcollide(bullets, zombies, True, True)
        for hit_zombies in hits.values():
            score += len(hit_zombies)

        # Check if any zombie touches the shooter (tighter body-to-body distance)
        hit_player = False
        for zombie in zombies:
            if player.pos.distance_to(zombie.pos) < 24:
                hit_player = True
                break

        if hit_player:
            flash_timer = 0.25  # 0.25-second red flash on impact
            game_state = "game_over"

        # Spawn a new random wave of 3-8 zombies once all are eliminated
        elif len(zombies) == 0:
            spawn_zombies()

        # Draw all sprites onto gs
        bullets.draw(gs)
        player_group.draw(gs)
        zombies.draw(gs)

        # Draw live score in top-left of gs
        hud_surf = hud_font.render(f"Kills: {score}", True, (255, 255, 255))
        gs.blit(hud_surf, (15, 12))

        # Make background desired color
        screen.fill(background)
        # put gs on background
        screen.blit(gs, (19, 0))

    elif game_state == "game_over":
        if flash_timer > 0:
            flash_timer -= dt
        draw_game_over_screen()

    pygame.display.flip()

pygame.quit()