from constants import *
from circleshape import *
from main import *

class Shot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = velocity 

    def draw(self, screen):
        pygame.draw.circle(screen, (WHITE), (int(self.position.x), int(self.position.y)), SHOT_RADIUS, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        
        