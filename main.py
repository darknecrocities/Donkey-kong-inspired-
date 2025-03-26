import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PLATFORM_COLOR = (139, 69, 19)
BARREL_COLOR = (150, 75, 0)
LADDER_COLOR = (100, 100, 255)
FONT = pygame.font.Font(None, 36)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Donkey Kong Clone")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(100, SCREEN_HEIGHT - 50))
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.climbing = False
    
    def update(self):
        if not self.climbing:
            self.vel_y += 1  # Gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Keep within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Collision with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True
                self.climbing = False

        # Ladder collision
        for ladder in ladders:
            if self.rect.colliderect(ladder.rect):
                self.climbing = True
                self.vel_y = 0

        # Keep player on the ground
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = -15  # Jump height
            self.on_ground = False

# Barrel class
class Barrel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BARREL_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = random.choice([-3, 3])
        self.vel_y = 0
    
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Check for collisions with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                break
        else:
            self.vel_y += 1  # Apply gravity

        # Reverse direction at screen edges
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vel_x *= -1

        # Reset barrel if it reaches the bottom
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.topleft = (random.randint(100, SCREEN_WIDTH - 100), 100)

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, 10))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

# Ladder class
class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y, height):
        super().__init__()
        self.image = pygame.Surface((20, height))
        self.image.fill(LADDER_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

# Create sprite groups
all_sprites = pygame.sprite.Group()
barrels = pygame.sprite.Group()
platforms = pygame.sprite.Group()
ladders = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create platforms
platform_data = [(50, 500, 300), (400, 400, 300), (50, 300, 300), (400, 200, 300)]
for x, y, width in platform_data:
    platform = Platform(x, y, width)
    platforms.add(platform)
    all_sprites.add(platform)

# Create ladders
ladder_data = [(320, 450, 50), (150, 350, 50), (470, 250, 50)]
for x, y, height in ladder_data:
    ladder = Ladder(x, y, height)
    ladders.add(ladder)
    all_sprites.add(ladder)

# Spawn barrels
for _ in range(3):
    barrel = Barrel(random.randint(100, SCREEN_WIDTH - 100), 100)
    barrels.add(barrel)
    all_sprites.add(barrel)

# Main Menu
running = True
while running:
    screen.fill(WHITE)
    title_text = FONT.render("Press ENTER to Start", True, RED)
    screen.blit(title_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            running = False

# Countdown
for i in range(3, 0, -1):
    screen.fill(WHITE)
    count_text = FONT.render(str(i), True, RED)
    screen.blit(count_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    time.sleep(1)

# Main loop
running = True
clock = pygame.time.Clock()
score = 0

def game_over():
    screen.fill(WHITE)
    game_over_text = FONT.render("Game Over! Press R to Restart", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump()
    keys = pygame.key.get_pressed()
    player.vel_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
    all_sprites.update()
    if pygame.sprite.spritecollideany(player, barrels):
        game_over()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()