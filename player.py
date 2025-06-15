from circleshape import *
from constants import *
from main import *
from shot import Shot
import math

class Player(CircleShape):
    def __init__(self, x, y, joystick=None):
        super().__init__(x, y, PLAYER_RADIUS)
        self.debug_timer = 0
        self.rotation = 0
        self.shoot_timer = 0
        self.joystick = joystick

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
        
    def draw(self, screen):
        pygame.draw.polygon(screen, (WHITE), self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        
    def update(self, dt):
        self.shoot_timer -= dt
        #self.debug_timer += dt
        #if self.debug_timer >= 2:
            #self.debug_timer = 0
            #for i in range(self.joystick.get_numaxes()):
                #print(f"Axis {i}: {self.joystick.get_axis(i):.2f}")

        if self.joystick and self.joystick.get_init():
            # Left stick axes: axis 0 (left/right), axis 1 (up/down)
            move_x = self.joystick.get_axis(0)
            move_y = self.joystick.get_axis(1)
            
            aim_x = self.joystick.get_axis(2)
            aim_y = self.joystick.get_axis(3)
        
            # Deadzone to avoid drift
            deadzone = 0.5
        
            # Movement vector from left stick (invert y because up is usually -1)
            move_vector = pygame.Vector2(move_x, move_y)
            if move_vector.length() > deadzone:
                # Normalize and move player
                move_vector = move_vector.normalize()
                self.position += move_vector * PLAYER_SPEED * dt
        
            # Aim direction from right stick
            aim_vector = pygame.Vector2(aim_x, aim_y)
            if aim_vector.length() > deadzone:
                angle_radians = math.atan2(aim_y, aim_x)  
                angle_degrees = math.degrees(angle_radians)
                self.rotation = (angle_degrees + 270) % 360  # <-- key correction!
        
            # Shoot if right trigger pressed or button pressed
            # Example: check if button 0 (usually A) is pressed
            rt_value = self.joystick.get_axis(5)  # Right trigger axis
            trigger_deadzone = 0.2
            if rt_value > trigger_deadzone and self.shoot_timer <= 0:
                self.shoot()

        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.rotate(-dt)
            if keys[pygame.K_d]:
                self.rotate(dt)
            if keys[pygame.K_w] or keys[pygame.K_s]:
                self.move(dt)
            if keys[pygame.K_SPACE]:
                if self.shoot_timer <= 0:
                    self.shoot()
    
    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.position += forward * PLAYER_SPEED * dt
        elif keys[pygame.K_s]:
            backward = pygame.Vector2(0, -1).rotate(self.rotation)
            self.position += backward * PLAYER_SPEED * dt

    def shoot(self):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)  # assumes angle is clockwise
        velocity = direction * PLAYER_SHOOT_SPEED
        self.shoot_timer = PLAYER_SHOOT_TIMER
        Shot(self.position.x, self.position.y, velocity)
        
    