import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side Scrolling Game")

# Frame rate
clock = pygame.time.Clock()

# Game Variables
score = 0
camera_x = 0
level = 1

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Red player
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 150
        self.speed = 5
        self.jump_power = 17  # Increased jump power
        self.is_jumping = False
        self.velocity_y = 0
        self.health = 100
        self.lives = 3

    def update(self, keys_pressed):
        # Left and right movement
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Jumping mechanics
        if not self.is_jumping and keys_pressed[pygame.K_SPACE]:
            self.is_jumping = True
            self.velocity_y = -self.jump_power

        if self.is_jumping:
            self.velocity_y += 1  # Simulate gravity
            self.rect.y += self.velocity_y
            # Reset jump when the player hits the ground
            if self.rect.y >= SCREEN_HEIGHT - 150:
                self.rect.y = SCREEN_HEIGHT - 150
                self.is_jumping = False

# Create a player object
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((0, 255, 0))  # Green projectile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.kill()

# Create a list to hold projectiles
projectiles = pygame.sprite.Group()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Blue enemy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 50
        self.required_hits = 1  # Default hits required for level 1

    def update(self):
        self.rect.x -= 3 + (level - 1)  # Gradually increase enemy speed
        if self.rect.x < -50:
            self.kill()

# Boss Class
class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((100, 100))  # Bigger boss size
        self.image.fill((255, 0, 255))  # Purple boss
        self.health = 150  # Boss health
        self.required_hits = 4  # Hits required to defeat boss

# Create sprite groups
enemies = pygame.sprite.Group()

# Function to spawn a level
def spawn_level(level):
    global enemies
    enemies.empty()
    
    if level == 1:
        enemy_count = 5
    elif level == 2:
        enemy_count = 7
    elif level == 3:
        enemy_count = 10  # Total enemies including the boss
    
    for i in range(enemy_count):
        if level == 3 and i == 9:  # Spawn boss at the last enemy spot
            boss = Boss(SCREEN_WIDTH + i * 200, SCREEN_HEIGHT - 150)
            enemies.add(boss)
        else:
            enemy = Enemy(SCREEN_WIDTH + i * 200, SCREEN_HEIGHT - 150)
            enemies.add(enemy)

def draw_ui():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 50))

    lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 90))

    level_text = font.render(f"Level: {level}", True, (255, 255, 255))  # Display current level
    screen.blit(level_text, (10, 130))

def update_camera():
    global camera_x
    camera_x += (player.rect.x - camera_x - 100) * 0.1

def draw_scene():
    screen.fill((135, 206, 235))  # Sky-blue background

    for sprite in player_group:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
    
    for sprite in projectiles:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

    for sprite in enemies:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

def game_over():
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

def win_game():
    font = pygame.font.Font(None, 74)
    win_text = font.render("Congratulations!", True, (0, 255, 0))
    screen.blit(win_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

def restart_game():
    global score, level
    score = 0
    player.health = 100
    player.lives = 3
    player.rect.x = 100
    player.rect.y = SCREEN_HEIGHT - 150
    level = 1
    spawn_level(level)

# Call the function to spawn the first level
spawn_level(level)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed)

    # Handle projectile shooting
    if keys_pressed[pygame.K_z]:  # Press Z to shoot
        projectile = Projectile(player.rect.x + 50, player.rect.y + 20)
        projectiles.add(projectile)

    # Update projectiles and enemies
    projectiles.update()
    enemies.update()

    # Check collisions
    for projectile in projectiles:
        hit_enemies = pygame.sprite.spritecollide(projectile, enemies, False)
        for enemy in hit_enemies:
            if enemy.required_hits > 0:  # If the enemy requires hits
                enemy.required_hits -= 1  # Decrease required hits
                if enemy.required_hits == 0:  # If hits reach zero, remove enemy
                    enemy.kill()
                    score += 10  # Increment score
            projectile.kill()  # Remove the projectile after hitting

    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            player.health -= 10  # Player loses health on collision
            enemy.kill()  # Remove enemy on collision
            if player.health <= 0:
                player.lives -= 1  # Lose a life if health reaches zero
                player.health = 100  # Reset health for the next life

    # Check if all enemies are defeated
    if len(enemies) == 0:  # Check for the condition of all enemies defeated
        if level < 3:  # Proceed to next level
            level += 1
            spawn_level(level)
        else:  # If all enemies (including boss) are defeated
            win_game()
            pygame.display.update()
            pygame.time.delay(2000)  # Wait for 2 seconds to show the message
            running = False  # End the game

    update_camera()
    draw_scene()
    draw_ui()

    # Check game over condition
    if player.lives <= 0:
        game_over()
        pygame.display.update()
        pygame.time.delay(2000)  # Wait for 2 seconds before quitting
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
