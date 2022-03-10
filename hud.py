import pygame
from pathlib import Path
from settings import s


class Hud(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, player_1: str, player_2: str):
        """
        Класс реализующий худ и его размещение на игровом экране
        :param x: точка размещения по оси Х
        :param y: точка размещения по оси Y
        :param w: ширина худа
        """
        super().__init__()

        self.w = w

        self.p_1 = player_1
        self.p_2 = player_2

        self.image = pygame.Surface((self.w, 300))
        self.image.fill('blue')
        self.image.set_colorkey('blue')

        self.health_bar = pygame.Surface((500, 30))
        self.health_bar_1 = pygame.Surface((w, 30))

        self.health_bar.fill('green')
        self.health_bar_1.fill('green')

        self.image.blit(self.health_bar, (0, 0, 500, 50))
        self.image.blit(self.health_bar_1, (500 - w, 0, 500, 50))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.img = pygame.image.load(Path('content', 'props', 'inf.gif'))
        self.image.blit(self.img, (0, 0, 100, 100))

        self.font = pygame.font.Font(Path('content', 'font', 'mortalkombat1.ttf'), 50)
        self.name_1 = self.font.render(self.p_1, False, 'white')
        self.name_2 = self.font.render(self.p_2, False, 'white')

        self.sound_1 = pygame.mixer.Sound(Path('content', 'sound', '03.mp3'))
        self.sound_2 = pygame.mixer.Sound(Path('content', 'sound', '04.mp3'))
        self.sound_3 = pygame.mixer.Sound(Path('content', 'sound', 'mk2-finish1a.mp3'))

        self.sound_1.set_volume(s.get_music())
        self.sound_2.set_volume(s.get_sound())
        self.sound_3.set_volume(s.get_music())

        self.sound_1.play(-1)
        self.end = False

    def update(self, health: int, health_2: int) -> None:
        """
        Обновляет данные здоровья персонажей на главном экране
        :param health: здоровье первого игрока
        :param health_2: здоровье второго игрока
        :return: None
        """
        self.image = pygame.Surface((self.w, 300))
        self.image.fill('blue')
        self.image.set_colorkey('blue')

        self.__health_bar(health)
        self.__health_bar(health_2, True)

        self.image.blit(self.img, (self.w // 2 - 80, -40))

        if health == 0 or health_2 == 0:
            self.sound_1.stop()
            self.__endRound(health)

    def lets_fight(self, sound) -> bool:
        """
        Озвучка старта матча
        :param sound: фразу произнесли?
        :return: да, фразу произнесли (bool)
        """
        if sound:
            self.sound_2.play()
        return False

    def __endRound(self, h1: int) -> None:
        """
        Отслеживает окончание матча
        :return: None
        """
        if not self.end:
            p = self.p_2 if h1 == 0 else self.p_1
            sound = pygame.mixer.Sound(Path('content', 'sound', f'{p}win.mp3'))
            sound.set_volume(s.get_sound())
            sound.play()
            self.end = True

    def __health_bar(self, health: int, pos: bool = False) -> None:
        w = int(500 * health / 100)
        if w >= 0:
            health_bar = pygame.Surface((w, 30), flags=pygame.SRCALPHA)
            health_bar.fill('green')
            if pos:
                self.image.blit(health_bar, (self.w - w - 40, 0, 500, 50))
                self.image.blit(self.name_2, (self.w - self.name_2.get_width() - 40, 20))
            else:
                self.image.blit(health_bar, (0, 0, 500, 50))
                self.image.blit(self.name_1, (0, 20))
