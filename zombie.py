import pygame


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(64, 64), speed=120):
        super().__init__()
        self.speed = speed

        # Kenney Top-Down Shooter zombie file path (note Kenney's "zoimbie" spelling):
        raw_img = pygame.image.load(r"kenney_top-down-shooter\PNG\Zombie 1\zoimbie1_hold.png").convert_alpha()
        if size is not None:
            raw_img = pygame.transform.smoothscale(raw_img, size)

        self.original_image = raw_img
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)

    def chase_player(self, player_pos):
        """Returns a normalized direction vector pointing toward the player."""
        direction = pygame.math.Vector2(player_pos) - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        return direction

    def rotate_to_player(self, player_pos):
        """Rotates the zombie to face the player."""
        rel_x = player_pos[0] - self.pos.x
        rel_y = player_pos[1] - self.pos.y

        angle = pygame.math.Vector2(rel_x, rel_y).angle_to((1, 0))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt, gs_rect, player_pos):
        direction = self.chase_player(player_pos)
        self.pos += direction * self.speed * dt

        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.rect.clamp_ip(gs_rect)
        self.pos = pygame.math.Vector2(self.rect.center)

        self.rotate_to_player(player_pos)