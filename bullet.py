import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, speed=700):
        super().__init__()
        self.speed = speed

        # Draw a small yellow bullet surface
        self.original_image = pygame.Surface((12, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (255, 220, 80), (0, 0, 12, 4), border_radius=2)

        # Calculate direction vector from shooter to mouse cursor
        direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(start_pos)
        if direction.length() > 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.math.Vector2(1, 0)

        # Rotate the bullet image to match the firing angle
        angle = self.direction.angle_to((1, 0))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, dt, gs_rect):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Remove the bullet automatically if it leaves the game surface
        if not gs_rect.colliderect(self.rect):
            self.kill()