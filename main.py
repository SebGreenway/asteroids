import pygame
from constants import *
from player import *
from circleshape import *
from asteroid import *
from asteroidfield import *
from shot import *

updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print('Starting Asteroids!')
    print(f'Screen width: {SCREEN_WIDTH}')
    print(f'Screen height: {SCREEN_HEIGHT}')
    clock = pygame.time.Clock()
    dt = 0
    game_over = False
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    Shot.containers = (updatable, drawable, shots)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        if not game_over:
            updatable.update(dt)
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    print("Game over!")
                    game_over = True
                    # Handle collision (e.g., end game, reduce health, etc.)
            for shot in shots:
                for asteroid in asteroids:
                    if shot.collides_with(asteroid):
                        print("Shot hit an asteroid!")
                        # Handle collision (e.g., remove asteroid, increase score, etc.)
                        shot.kill()
                        asteroid.split()
            screen.fill(BLACK)  # Fill the screen with black
            for sprite in drawable:
                sprite.draw(screen)
            #player.draw(screen)  # Draw the player
            pygame.display.flip()  # Update the display
            dt = clock.tick(60) / 1000.0

        else:
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.fill(BLACK)
            screen.blit(text, text_rect)
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                
                game_over = False
            

if __name__ == "__main__":
    main()