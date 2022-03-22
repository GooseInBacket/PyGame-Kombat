import pygame
from random import randint
from hitbox import Hitbox
from hud import Hud
from pathlib import Path
from settings import s
from main_menu import Menu


class Game:
    def __init__(self, w, h):
        self.size = self.w, self.h = w, h

        pygame.init()

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('MK ALPHA')
        pygame.display.set_icon(pygame.image.load(Path('content', 'props', 'logo.png')))

        self.clock = pygame.time.Clock()

        self.players = pygame.sprite.Group()
        self.hitboxes = pygame.sprite.Group()

        self.hitbox = Hitbox('subzero', 0, 390)
        self.hitbox_2 = Hitbox('subzero', 850, 390, False, True)

        self.hitboxes.add(self.hitbox)
        self.hitboxes.add(self.hitbox_2)

        img = pygame.image.load(Path('content', 'maps', f'0{randint(1, 3)}.png')).convert()
        self.background = pygame.transform.scale(img, (w, h))
        self.background_rect = self.background.get_rect()

    def run(self):
        """
        Запуск основного игрового цикла
        :return: None
        """
        while True:
            menu = Menu(self.clock)
            menu.set_menu(self.screen)
            menu.choose_your_fighter(self.screen)

            self.fight()
            menu.menu = menu.choose = True

    def border_checker(self):
        """
        Проверяет соприкосновение моделей игроков с границами экрана и друг с другом
        :return: None
        """
        if self.hitbox.get_posx() <= 0:
            self.hitbox.set_posx(0)
        elif self.hitbox.get_posx() >= self.w - self.hitbox.get_w():
            self.hitbox.set_posx(self.w - self.hitbox.get_w())
        elif self.hitbox.get_posx() + self.hitbox.get_w() >= self.hitbox_2.get_posx() + 50:
            self.hitbox.set_posx(self.hitbox_2.get_posx() + 50 - self.hitbox.get_w())

        if self.hitbox_2.get_posx() <= 0:
            self.hitbox_2.set_posx(0)
        elif self.hitbox_2.get_posx() >= self.w - self.hitbox_2.get_w():
            self.hitbox_2.set_posx(self.w - self.hitbox_2.get_w())
        elif self.hitbox_2.get_posx() <= self.hitbox.get_posx() + self.hitbox.get_w():
            self.hitbox_2.set_posx(self.hitbox_2.get_posx())

    def set_direction(self):
        """
        Устанавливает направление взгляда персонажа
        :return: None
        """
        if self.hitbox.get_posx() > self.hitbox_2.get_posx() and self.hitbox.get_direction():
            self.hitbox.set_flip()
        elif self.hitbox.get_posx() < self.hitbox_2.get_posx() and not self.hitbox.get_direction():
            self.hitbox.set_flip()

        if self.hitbox_2.get_posx() > self.hitbox.get_posx() and self.hitbox_2.get_direction():
            self.hitbox_2.set_flip()
        elif self.hitbox_2.get_posx() < self.hitbox.get_posx() and not self.hitbox_2.get_direction():
            self.hitbox_2.set_flip()

    def fight(self):
        """
        Отвечает за реализацию матча
        :return: None
        """
        fight = True
        game = True

        huds = pygame.sprite.Group()
        self.hitboxes = pygame.sprite.Group()

        hud = Hud(20, 20, self.w, s.get_player1(), s.get_player2())
        self.hitbox = Hitbox(s.get_player1(), 0, 390)
        self.hitbox_2 = Hitbox(s.get_player2(), 850, 390, False, True)

        huds.add(hud)
        self.hitboxes.add(self.hitbox)
        self.hitboxes.add(self.hitbox_2)

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and hud.end:
                        game = False
            self.screen.blit(self.background, self.background_rect)

            hit = pygame.sprite.collide_mask(self.hitbox, self.hitbox_2)

            self.hitbox.update(s.anim, s.speed, hit, self.hitbox_2.attack(), win=self.hitbox_2.die())
            self.hitbox_2.update(s.anim, s.speed, hit, self.hitbox.attack(), win=self.hitbox.die())

            self.hitboxes.draw(self.screen)

            fight = hud.lets_fight(fight)

            hud.update(self.hitbox.get_health(), self.hitbox_2.get_health())
            huds.draw(self.screen)

            self.set_direction()
            self.border_checker()

            self.clock.tick(s.fps)
            pygame.display.flip()
