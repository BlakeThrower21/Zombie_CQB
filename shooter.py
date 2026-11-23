import pygame


class Shooter(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(64, 64), speed=250):
        super().__init__()
        self.speed = speed

        # Put your character's file path right here:
        raw_img = pygame.image.load(r"kenney_top-down-shooter\PNG\Hitman 1\hitman1_gun.png").convert_alpha()
        if size is not None:
            raw_img = pygame.transform.smoothscale(raw_img, size)

        self.original_image = raw_img
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0, 0)

        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1

        if direction.length() > 0:
            direction = direction.normalize()

        return direction

    def rotate_to_mouse(self, gs_offset=(19, 0)):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x = (mouse_x - gs_offset[0]) - self.pos.x
        rel_y = (mouse_y - gs_offset[1]) - self.pos.y

        angle = pygame.math.Vector2(rel_x, rel_y).angle_to((1, 0))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt, gs_rect, gs_offset=(19, 0)):
        direction = self.handle_input()
        self.pos += direction * self.speed * dt

        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.rect.clamp_ip(gs_rect)
        self.pos = pygame.math.Vector2(self.rect.center)

        self.rotate_to_mouse(gs_offset)