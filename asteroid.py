from constants import *
from circleshape import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (WHITE), (int(self.position.x), int(self.position.y)), self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return []
        else:
            angle = random.uniform(20, 50)
            speed = self.velocity.length()
            direction_1 = pygame.Vector2(0, 1).rotate(angle) * 1.2 * speed
            direction_2 = pygame.Vector2(0, 1).rotate(-angle) * 1.2 * speed
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            return [
                Asteroid(self.position.x, self.position.y, new_radius).set_velocity(direction_1),
                Asteroid(self.position.x, self.position.y, new_radius).set_velocity(direction_2)
            ]
    def set_velocity(self, velocity):
        self.velocity = velocity 
        return self