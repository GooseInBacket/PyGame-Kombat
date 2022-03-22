import pygame
from pathlib import Path
from settings import s


class Menu:
    def __init__(self, clock: pygame.time.Clock):
        """
        Класс реализует работу главного меню игры
        :param clock: счётчик FPS
        """
        self.w, self.h = s.size
        self.clock = clock

        self.font_1 = pygame.font.Font(Path('content', 'font', 'mortalkombat1.ttf'), 80)

        menu = pygame.image.load(Path('content', 'props', '07.png')).convert()
        un_menu = pygame.image.load(Path('content', 'props', '08.png')).convert()
        choose = pygame.image.load(Path('content', 'props', '02.png')).convert()

        self.un_main_menu = pygame.transform.scale(un_menu, (self.w, self.h * 3))
        self.un_main_menu_rect = self.un_main_menu.get_rect()
        self.un_main_menu_rect.y = -(self.h * 2)

        self.main_menu = pygame.transform.scale(menu, (self.w, self.h))
        self.main_menu.set_colorkey('white')
        self.main_menu_rect = self.main_menu.get_rect()

        self.choose_menu = pygame.transform.scale(choose, (self.w, self.h))
        self.choose_menu_rect = self.choose_menu.get_rect()

        self.sound_1 = pygame.mixer.Sound(Path('content', 'sound', '01.mp3'))
        self.sound_2 = pygame.mixer.Sound(Path('content', 'sound', '02.mp3'))

        self.sound_1.set_volume(s.get_sound())
        self.sound_2.set_volume(s.get_music())
        self.sound_2.play(-1)

        self.buttons = ['tournament', 'settings']

        self.menu = True
        self.choose = True
        self.settings = False
        self.cursor = 0
        self.anim = 0

    def set_menu(self, screen: pygame.display) -> None:
        """
        Отрисовывает главное меню на экране -> (Турнир, Настройки)
        :param screen: экран игры
        :return: None
        """
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.cursor -= 1
                        if self.cursor < 0:
                            self.cursor = len(self.buttons) - 1

                    elif event.key == pygame.K_UP:
                        self.cursor += 1
                        if self.cursor > len(self.buttons) - 1:
                            self.cursor = 0

                    elif self.settings and event.key == pygame.K_LEFT:
                        if self.cursor:
                            s.set_sound(s.get_sound() - 0.1)
                            if s.get_sound() <= 0:
                                s.set_sound(0)
                        else:
                            s.set_music(s.get_music() - 0.1)
                            if s.get_music() <= 0:
                                s.set_music(0)
                        self.buttons = [f'music: {int(s.get_music() * 10)}',
                                        f'sound: {int(s.get_sound() * 10)}']

                    elif self.settings and event.key == pygame.K_RIGHT:
                        if self.cursor:
                            s.set_sound(s.get_sound() + 0.1)
                            if s.get_sound() >= 1:
                                s.set_sound(1)
                        else:
                            s.set_music(s.get_music() + 0.1)
                            if s.get_music() >= 1:
                                s.set_music(1)
                        self.buttons = [f'music: {int(s.get_music() * 10)}',
                                        f'sound: {int(s.get_sound() * 10)}']

                    elif event.key == pygame.K_RETURN:
                        if self.cursor == 0 and not self.settings:
                            self.menu = False
                        elif self.cursor == 1 and not self.settings:
                            self.buttons = [f'music: {int(s.get_music() * 10)}',
                                            f'sound: {int(s.get_sound() * 10)}']
                            self.settings = True
                        else:
                            self.buttons = ['tournament', 'settings']
                            self.settings = False
                        self.cursor = 0
                    self.sound_1.set_volume(s.get_sound())
                    self.sound_2.set_volume(s.get_music())
                    self.sound_1.play()

            self.set_background(screen, 10)
            self.set_title(screen, 'PyGame Kombat')
            for i, button in enumerate(self.buttons):
                if self.cursor == i:
                    self.draw_button(screen, button, self.h // 3 + 100 * i + 30, True, 3)
                else:
                    self.draw_button(screen, button, self.h // 3 + 100 * i + 30, True, 1)
            self.draw_button(screen, 'Press Enter', self.h - 170)

            self.anim += 1
            self.anim %= 30

            self.clock.tick(s.fps)
            pygame.display.flip()

    def choose_your_fighter(self, screen: pygame.display) -> None:
        """
        Отрисовывает меню выбора персонажей
        :param screen: экран игры
        :return: None
        """
        self.sound_1.set_volume(s.get_sound())
        self.sound_2.set_volume(s.get_music())
        pos_list = [[(100, 145), (300, 145), (705, 145), (910, 145)],
                    [(305, 400), (505, 400), (708, 400)]]
        fighters = {(100, 145): 'johny',
                    (300, 145): 'kano',
                    (705, 145): 'subzero',
                    (910, 145): 'sonya',
                    (300, 400): 'raiden',
                    (500, 400): 'lao',
                    (700, 400): 'scorpion'}
        current_fighter = 0
        row = 0
        color = 'green'

        while self.choose:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        row = 1
                        current_fighter = 2 if current_fighter > 1 else 0

                    elif event.key == pygame.K_UP:
                        row = 0
                        current_fighter = 1 if current_fighter == 0 else current_fighter

                    elif event.key == pygame.K_LEFT:
                        current_fighter -= 1
                        if not row and current_fighter < 0:
                            current_fighter = 3
                        elif row and current_fighter < 0:
                            current_fighter = 2

                    elif event.key == pygame.K_RIGHT:
                        current_fighter += 1
                        if not row and current_fighter >= 4:
                            current_fighter = 0
                        elif row and current_fighter >= 3:
                            current_fighter = 0

                    elif event.key == pygame.K_RETURN:
                        fighter = fighters[pos_list[row][current_fighter]]
                        if color == 'green':
                            s.set_player_1(fighter)
                            self.play_char(fighter)
                            color = 'red'
                            row, current_fighter = 0, 3
                        else:
                            s.set_player_2(fighter)
                            self.play_char(fighter)
                            while pygame.mixer.Channel(1).get_busy():
                                pass
                            self.choose = False
                            self.sound_2.stop()
                    self.sound_1.play()

            screen.blit(self.choose_menu, self.choose_menu_rect)
            c, r = pos_list[row][current_fighter]
            pygame.draw.rect(screen, color, (c, r, 190, 240), 10, 0)

            pygame.display.flip()
            self.clock.tick(s.fps)

    def draw_button(self, screen, text: str, y: float, click: bool = False, anim: int = 4) -> None:
        """
        Отрисовывает кнопку "пункт меню"
        :param screen: экран игры
        :param text: текст кнопки
        :param y: позиция кнопки по оси Y
        :param click: кликабальна?
        :param anim: анимирована?
        :return: None
        """
        c1, c2 = ('white', 'grey') if click else ('green', 'white')

        f = self.font_1.render(text, False, c1 if self.anim % anim == 0 else c2)
        fs = self.font_1.render(text, False, 'black')

        screen.blit(fs, (self.w // 2 - fs.get_width() // 2 + 2, y + 2))
        screen.blit(f, (self.w // 2 - fs.get_width() // 2, y))

    def set_title(self, screen, text: str) -> None:
        """
        Задаёт заголовок главного экрана игры
        :param screen: экран игры
        :param text: текст заголовка
        :return: None
        """
        f = self.font_1.render(text, False, 'yellow')
        fs = self.font_1.render(text, False, 'black')

        screen.blit(fs, (self.w // 2 - f.get_width() // 2 + 2, 100 + 2))
        screen.blit(f, (self.w // 2 - f.get_width() // 2, 100))

    def set_background(self, screen, anim: int = 5) -> None:
        """
        Задаёт задний фон главного меню игры
        :param screen: экран игры
        :param anim: анимированный?
        :return: None
        """
        if self.un_main_menu_rect.y > 0:
            self.un_main_menu_rect.y = -(self.h * 2)

        screen.blit(self.un_main_menu, self.un_main_menu_rect)
        screen.blit(self.main_menu, self.main_menu_rect)

        self.un_main_menu_rect.y += anim

    @classmethod
    def play_char(cls, fighter: str):
        who = pygame.mixer.Sound(Path('content', 'sound', f'{fighter}.mp3'))
        who.set_volume(s.get_sound())
        who.play()
