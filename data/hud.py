import pygame
from time import time
from pathlib import Path
from data.settings import s


class Hud(pygame.sprite.Sprite):
    def __init__(self, name_1: str = 'name', name_2: str = 'name'):
        super().__init__()

        self.anim = 0

        self.image = pygame.Surface((s.size[0], s.size[1] // 5))
        self.image.fill('Green')
        self.image.set_colorkey('Green')
        self.rect = self.image.get_rect()

        self.start_round = time()
        self.start_time = time()
        self.timer = 90
        self.round = 1

        self.font = pygame.font.Font(Path('content', 'font', 'mortalkombat1.ttf'), 65)
        self.font_names = pygame.font.Font(Path('content', 'font', 'mortalkombat1.ttf'), 40)
        self.time_count = self.font.render(f'{self.timer}'.rjust(2, '0'), True, 'white')
        self.time_count_s = self.font.render(f'{self.timer}'.rjust(2, '0'), True, '#141414')
        self.r_anonce = self.font.render(f'Round {self.round}', True, 'white')

        self.music = pygame.mixer.Sound(Path('content', 'sound', '03.mp3'))
        self.fight_anonce = pygame.mixer.Sound(Path('content', 'sound', '04.mp3'))
        self.fight_anonce.set_volume(s.get_sound())
        self.music.set_volume(s.get_music())
        self.music.play(-1)

        self.name_1 = self.font_names.render(name_1, True, '#ffff00')
        self.name_2 = self.font_names.render(name_2, True, '#ffff00')

        self.width_1 = s.size[0] // 2.5
        self.width_2 = s.size[0] // 2.5
        self.start = 10

    def update(self, health_1, health_2):
        self.width_1 = int(480 * (health_1 / 1000))
        self.width_2 = int(480 * (health_2 / 1000))
        if time() - self.start_round > 3:
            if time() - self.start_time >= 1:
                self.timer -= 1
                self.start_time = time()
            if self.timer <= 0:
                self.timer = 0
            self.time_count = self.font.render(f'{self.timer}'.rjust(2, '0'), True, 'white')
            self.time_count_s = self.font.render(f'{self.timer}'.rjust(2, '0'), True, '#141414')

        else:
            self.anim += 1
            self.anim %= 30

        if 0.1 < time() - self.start_round < 2:
            color = 'red' if self.anim % 3 == 0 else 'white'

            self.r_anonce = self.font.render(f'Round {self.round}', True, color)
            self.image.blit(self.r_anonce, (s.size[0] // 2 - self.r_anonce.get_width() // 2, 100))

        if 2 < time() - self.start_round < 2.1 and not pygame.mixer.Channel(2).get_busy():
            self.fight_anonce.play()
            return True

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

        self.image = pygame.Surface((s.size[0], s.size[1] // 5))
        self.image.fill('Black')
        self.image.set_colorkey('Black')
        self.rect = self.image.get_rect()

        pos_1 = (10, 15, s.size[0] // 2.5, 40)
        pos_2 = (s.size[0] - s.size[0] // 2.5 - 10, 15, s.size[0] // 2.5, 40)

        health_1 = (self.start + 480 - self.width_1, 15, self.width_1, 40)
        health_2 = (s.size[0] - s.size[0] // 2.5 - 10, 15, self.width_2, 40)

        pygame.draw.rect(self.image, '#b50000', pos_1, 0)
        pygame.draw.rect(self.image, '#00a500', health_1, 0)
        pygame.draw.rect(self.image, '#ffff00', pos_1, 5, 1)

        pygame.draw.rect(self.image, '#b50000', pos_2, 0)
        pygame.draw.rect(self.image, '#00a500', health_2, 0)
        pygame.draw.rect(self.image, '#ffff00', pos_2, 5, 1)

        pos = (s.size[0] // 2 - self.time_count.get_width() // 2 + 5, 15)
        self.image.blit(self.time_count_s, pos)
        self.image.blit(self.time_count, (s.size[0] // 2 - self.time_count.get_width() // 2, 10))
        self.image.blit(self.name_1, (20, 8))
        self.image.blit(self.name_2, (s.size[0] - 20 - self.name_2.get_width(), 8))
