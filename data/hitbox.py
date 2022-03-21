import pygame


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, w: int, h: int, color: str = 'orange'):
        super().__init__()

        self.color = color
        self.h = h
        self.w = w

        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.image.set_alpha(180)
        self.rect = self.image.get_rect()

        self.direction = True

    def update(self, pos: tuple, w: int = 100, h: int = 80, **kwargs):
        self.image = pygame.Surface((w, h))
        self.image.fill(self.color)
        self.image.set_alpha(180)
        self.rect = self.image.get_rect()

        if kwargs.get('body', False):
            self.rect.center = pos
        elif self.direction:
            self.rect.topleft = pos
        elif not self.direction:
            self.rect.topright = pos

        if kwargs.get('flykick', False):
            self.rect.y += h

        if kwargs.get('kick', False):
            self.rect.y += h // 2

    def get_pos(self):
        return self.rect.topleft if self.direction else self.rect.topright

    def get_center_x(self):
        return self.rect.center[0]

    def set_direction(self):
        self.direction = not self.direction

