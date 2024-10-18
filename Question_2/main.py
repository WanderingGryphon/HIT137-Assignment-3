import pygame
import os
from player import Player
from enemy import Enemy
from projectile import Projectile
from collectible import *
import random

pygame.init()

# Initialize Pygame and the mixer module for sound
pygame.mixer.init()

# Initialize flags for voiceovers
level_voiceover_played = [False, False, False]  # Index 0 for level 1, 1 for level 2, 2 for level 3

# Load sound effects
jump_sound = pygame.mixer.Sound(os.path.join('sounds', 'jump.mp3'))
shoot_sound = pygame.mixer.Sound(os.path.join('sounds', 'shot.mp3'))
enemy_hit_sound = pygame.mixer.Sound(os.path.join('sounds', 'background_music.mp3'))
level_1 = pygame.mixer.Sound(os.path.join('sounds', 'level1.mp3'))
level_2 = pygame.mixer.Sound(os.path.join('sounds', 'level2.mp3'))
level_3 = pygame.mixer.Sound(os.path.join('sounds', 'level3.mp3'))
boss_level = pygame.mixer.Sound(os.path.join('sounds', 'boss.mp3'))

# Load and play background music (loop infinitely)
pygame.mixer.music.load(os.path.join('sounds', 'background_music.mp3'))
pygame.mixer.music.play(-1)  # Loop forever
pygame.mixer.music.set_volume(0.05)  # 20% volume

# Set up window dimensions
win_width, win_height = 1440, 720
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("PyGame - Assignment 3")

# Define variables for health bar dimensions
health_bar_width = 200
health_bar_height = 20

# Initialize display message timers and duration
display_message_timer_lv1 = 0
display_message_timer_lv2 = 0
display_message_timer_lv3 = 0
display_message_duration = 3

# Define current frame for animations
current_frame = 0

# Load images for player animations
run_animation_images = [pygame.image.load(os.path.join('images', f'Run ({i}).png')) for i in range(1, 10)]
run_animation_images = [pygame.transform.scale(image, (140, 180)) for image in run_animation_images]  # Adjust size
back_animation_images = [pygame.transform.flip(image, True, False) for image in run_animation_images]
jump_animation_images = [pygame.image.load(os.path.join('images', f'Jump ({i}).png')) for i in range(1, 10)]
jump_animation_images = [pygame.transform.scale(image, (140, 180)) for image in jump_animation_images]  # Adjust size
jump_back_animation_images = [pygame.transform.flip(image, True, False) for image in jump_animation_images]
idle_animation_images = [pygame.image.load(os.path.join('images', f'Idle ({i}).png')) for i in range(1, 10)]
idle_animation_images = [pygame.transform.scale(image, (140, 180)) for image in idle_animation_images]  # Adjust size
idle_left_animation_images = [pygame.transform.flip(image, True, False) for image in idle_animation_images]
shoot_animation_images = [pygame.image.load(os.path.join('images', f'Shoot ({i}).png')) for i in range(1, 4)]
shoot_animation_images = [pygame.transform.scale(image, (140, 180)) for image in shoot_animation_images]  # Adjust size
shoot_left_animation_images = [pygame.transform.flip(image, True, False) for image in shoot_animation_images]

# Create player object with animation images
player = Player(100, 500, 120, 180,
                run_animation_images, back_animation_images, jump_animation_images,
                jump_back_animation_images, idle_animation_images, idle_left_animation_images,
                shoot_animation_images, shoot_left_animation_images,jump_sound=jump_sound,shoot_sound=shoot_sound)

# Initialize list for projectiles
projectiles = []

# Load image for player lives
life_image = pygame.image.load(os.path.join('images', "lives.png"))
life_image = pygame.transform.scale(life_image, (30, 30))

# Initialize clock and frames per second
clock = pygame.time.Clock()
fps = 30

# Initialize list for enemies and variables for enemy spawning
enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = random.randint(30, 60)

# Define function to spawn enemies
def spawn_enemy(type):
    x = random.randint(50, win_width - 50)
    if type == 'ground':
        y = win_height - 180
    else: y = -20
    width = 100
    height = 130
    health = 50
    speed = random.uniform(1, 2)

    if type == 'ground':
        enemy = Enemy('ground', x, y, width, height, 30, speed)
    elif type == 'air':
        enemy = Enemy('air', x, y, width, height, 20, speed)
    else:
        enemy = Enemy('boss', x, y, 120, 100, 70, 2)
    enemies.append(enemy)

# Game loop
run = True
while run:
    # Display level up messages
    if (player.level == 1 and display_message_timer_lv1 <= display_message_duration * fps) \
            or (player.level == 2 and display_message_timer_lv2 <= display_message_duration * fps)\
            or (player.level == 3 and display_message_timer_lv3 <= display_message_duration * fps):
        # Display level up text
        font_large = pygame.font.Font(None, 72)
        if player.level == 1:
            level_up_text = font_large.render("LEVEL 1", True, (255, 255, 255))
            if not level_voiceover_played[0]:  # Check if voiceover has been played for level 1
                level_1.play()
                level_voiceover_played[0] = True  # Set the flag to true
        elif player.level == 2:
            level_up_text = font_large.render("LEVEL 2", True, (255, 255, 255))
            if not level_voiceover_played[1]:  # Check if voiceover has been played for level 2
                level_2.play()  # Ensure you have the level_2 sound defined
                level_voiceover_played[1] = True  # Set the flag to true
        else:
            level_up_text = font_large.render("LEVEL 3", True, (255, 255, 255))
            if not level_voiceover_played[2]:  # Check if voiceover has been played for level 3
                level_3.play()  # Ensure you have the level_3 sound defined
                level_voiceover_played[2] = True  # Set the flag to true
        text_rect = level_up_text.get_rect(center=(win_width // 2, win_height // 2))
        win.blit(level_up_text, text_rect)
        if player.level == 1:
            display_message_timer_lv1 += 1
        elif player.level == 2:
            display_message_timer_lv2 += 1
        else:
            display_message_timer_lv3 += 1
        pygame.display.update()

    # Control frame rate
    clock.tick(fps)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # Load background image
    background = pygame.image.load(os.path.join('images', "background.jpg"))
    background = pygame.transform.scale(background, (1440, 720))
    win.blit(background, (0, 0))

    # Handle player shooting
    if keys[pygame.K_SPACE] and player.can_shoot:
        shoot_sound.play() 
        direction = player.last_direction
        projectiles.append(Projectile(player.x + player.width // 2, player.y + player.height // 2, direction))
        player.can_shoot = False

    # Remove projectiles that are out of bounds
    projectiles = [projectile for projectile in projectiles if 0 < projectile.x < win_width]

    # Update and draw enemies
    for enemy in enemies:
        if not enemy.is_dead:
            enemy.update_direction(player.x)
            enemy.appear()
            enemy.move(player.y)
            if enemy.appear_done:
                if enemy.type == 'ground':
                    pygame.draw.rect(win, (0, 0, 255), (enemy.x + 5, enemy.y - 10, 30, 5))
                    pygame.draw.rect(win, (255, 255, 255), (enemy.x + 5, enemy.y - 10, max(0, enemy.health), 5))
                    pygame.draw.rect(win, (0, 255, 0), (enemy.x + 5, enemy.y - 10, max(0, enemy.health), 5))
                elif enemy.type == 'air':
                    pygame.draw.rect(win, (0, 0, 255), (enemy.x + 10, enemy.y, 20, 5))
                    pygame.draw.rect(win, (255, 255, 255), (enemy.x + 10, enemy.y, max(0, enemy.health), 5))
                    pygame.draw.rect(win, (0, 255, 0), (enemy.x + 10, enemy.y, max(0, enemy.health), 5))
                else:
                    pygame.draw.rect(win, (0, 0, 255), (enemy.x + 30, enemy.y - 5, 70, 5))
                    pygame.draw.rect(win, (255, 255, 255), (enemy.x + 30, enemy.y - 5, max(0, enemy.health), 5))
                    pygame.draw.rect(win, (0, 255, 0), (enemy.x + 30, enemy.y - 5, max(0, enemy.health), 5))

            win.blit(enemy.image, (enemy.x, enemy.y))

    # Handle collision between player and enemies
    for enemy in enemies:
        if (
                enemy.appear_done
                and not enemy.is_dead
                and player.x < enemy.x + enemy.width
                and player.x + player.width > enemy.x
                and player.y < enemy.y + enemy.height
                and player.y + player.height > enemy.y
        ):
            player.handle_collision(fps)

    # Update and draw projectiles
    for projectile in projectiles:
        if projectile.direction == 1:
            projectile.x += projectile.vel
        else:
            projectile.x -= projectile.vel
        projectile.update_image()
        win.blit(projectile.image, (projectile.x, projectile.y))

        # Check for collision between projectiles and enemies
        for enemy in enemies:
            if (
            enemy.appear_done
            and not enemy.is_dead
            and enemy.x < projectile.x < enemy.x + enemy.width
            and enemy.y < projectile.y < enemy.y + enemy.height
            ):
                enemy.update_health(player, 10)
                # enemy_hit_sound.play()#update sound
                if projectile in projectiles:
                    projectiles.remove(projectile)

    # Update player
    player.update(win, win_width, keys)

    # Draw health bar for player
    pygame.draw.rect(win, (255, 255, 255), (10, 10, health_bar_width, health_bar_height))
    pygame.draw.rect(win, (255, 0, 0), (10, 10, player.health, health_bar_height))

    # Draw player lives
    for i in range(player.lives):
        win.blit(life_image, (220 + i * 30, 3))

    # Increment enemy spawn timer and handle level transitions
    enemy_spawn_timer += 1
    if player.level == 1:
        if enemy_spawn_timer >= enemy_spawn_delay:
            if len(enemies) < 15:
                spawn_enemy('ground')
            enemy_spawn_timer = 0
            enemy_spawn_delay = random.randint(30, 60)

            if len(enemies) > 0 and all(enemy.appear_done and enemy.is_dead for enemy in enemies):
                player.level = 2
                enemies.clear()

    if player.level == 2:
        if enemy_spawn_timer >= enemy_spawn_delay:
            if len(enemies) < 20:
                spawn_enemy('air')
            enemy_spawn_timer = 0
            enemy_spawn_delay = random.randint(30, 60)

            if len(enemies) > 0 and all(enemy.appear_done and enemy.is_dead for enemy in enemies):
                player.level = 3
                enemies.clear()

    if player.level == 3 and not player.win:
        if enemy_spawn_timer >= enemy_spawn_delay:
            if len(enemies) < 40:
                spawn_enemy('ground')
                spawn_enemy('air')
                spawn_enemy('air')
            enemy_spawn_timer = 0
            enemy_spawn_delay = random.randint(30, 60)

            if not player.win and len(enemies) > 0 and all(enemy.appear_done and enemy.type != 'boss' and enemy.is_dead for enemy in enemies):
                boss_level.play()
                spawn_enemy('boss')

            if not player.win and any(enemy.type == 'boss' and enemy.is_dead for enemy in enemies):
                player.win = True
                enemies.clear()

    # Spawn and handle collectibles
    spawn_collectible(player)
    update_and_draw_collectibles(win, player)
    handle_collectible_collision(player)

    # Display score and level information
    font = pygame.font.SysFont(None,25)
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {player.level}", True, (255, 255, 255))

    win.blit(score_text, (10, 40))
    win.blit(level_text, (10, 65))

    # Display game over/win screen
    if player.lives <= 0 or player.win:
        pygame.mixer.music.stop() #Stop the sound
        win.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 50)
        if not player.win:
            final_text = font.render("YOU LOSE", True, (255, 0, 0))
        else:
            final_text = font.render("YOU WIN", True, (255, 0, 0))
        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
        prompt_text = font.render("Play again? (Y/N)", True, (255, 255, 255))
        win.blit(final_text,
                 (win_width // 2 - final_text.get_width() // 2, win_height // 2 - final_text.get_height() // 2))
        win.blit(score_text, (win_width // 2 - score_text.get_width() // 2, win_height // 2 + 50))
        win.blit(prompt_text, (win_width // 2 - prompt_text.get_width() // 2, win_height // 2 + 100))

        # Handle player input for playing again
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            # Reset game state and restart the game
            player.reset(enemies)  # Implement reset() method in Player class to reset player state
            # Reset enemies, score, etc.
            pygame.mixer.music.play(-1)
            continue
        elif keys[pygame.K_n]:
            run = False  # Quit the game if the player doesn't want to play again

    pygame.display.update()

pygame.quit()
