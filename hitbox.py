import pygame
from os import path, listdir
from pathlib import Path
from random import choice
from settings import s
from time import time


class Hitbox(pygame.sprite.Sprite):
    """
    Класс абстрактного игрока
    """
    def __init__(self, name: str, x: int, y: int, control: bool = True, flip: bool = False):
        pygame.sprite.Sprite.__init__(self)
        self.spites = self.__create_sprite_list(name)
        if flip:
            self.__flip_img()

        self.current_frame = 0
        self.fight_frame = 0
        self.jumpCount = s.jump
        self.cooldown = 0
        self.health = 100

        sound = pygame.mixer.Sound
        self.hit_s = [sound(Path('content', 'sound', f'{str(i).rjust(2, "0")}.mp3'))
                      for i in range(5, 12)]

        for i in self.hit_s:
            i.set_volume(s.get_sound())

        if control:
            self.move_set = [pygame.K_s, pygame.K_w, pygame.K_a, pygame.K_d,
                             pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_q]
        else:
            self.move_set = [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT,
                             pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP0]

        self.direction = not flip
        self.isJump = False
        self.isDucking = False
        self.right = False
        self.left = False
        self.punch = False
        self.kick = False
        self.kick_head = False
        self.block = False

        self.img = self.spites['Fighting Stance'][self.current_frame]
        self.image = pygame.Surface((self.img.get_width(), self.img.get_height()))
        self.rect = self.image.get_rect()
        self.image.blit(self.img, (0, 0, self.img.get_width(), self.img.get_height()))

        self.rect.x, self.rect.y = (x, y)
        self.rect.x += 100
        self.flip = False

    def update(self, anim_speed: int | float, speed: int | float, collision=None,
               attack: bool = False, fight: bool = True, win: bool = False):
        self.current_frame += anim_speed
        key = pygame.key.get_pressed()

        if not self.block and not self.isJump and self.health and fight and not win:
            self.__press_button(key)
        self.__reactions(speed, collision, attack, win)

        key_count = key.count(True)
        if not any(key):
            self.left = self.right = False
            self.block = False
            self.isDucking = False

        elif key_count == 2:
            if key[self.move_set[2]] and key[self.move_set[3]]:
                self.left = self.right = False
            elif key[self.move_set[4]] and (key[self.move_set[2]] or key[self.move_set[3]]):
                self.left = self.right = False
            elif key[self.move_set[0]] and (key[self.move_set[2]] or key[self.move_set[3]]):
                self.left = self.right = False

    def __press_button(self, key):
        # вниз влево
        if key[self.move_set[0]] and key[self.move_set[2]]:
            self.left = True
            self.isDucking = True
        # вниз вправо
        elif key[self.move_set[0]] and key[self.move_set[3]]:
            self.right = True
            self.isDucking = True
        # вверх влево
        elif key[self.move_set[1]] and key[self.move_set[2]]:
            self.left = True
            self.isJump = True
        # вверх вправо
        elif key[self.move_set[1]] and key[self.move_set[3]]:
            self.right = True
            self.isJump = True
        # вправо
        elif key[self.move_set[3]]:
            self.right = True
        # влево
        elif key[self.move_set[2]]:
            self.left = True
        # вниз
        elif key[self.move_set[0]]:
            self.isDucking = True
        # вверх
        elif key[self.move_set[1]]:
            self.isJump = True
        # удар рукой
        elif key[self.move_set[4]]:
            self.punch = True
        # удар ногой
        elif key[self.move_set[5]]:
            self.kick = True
        # удар ногой в голову
        elif key[self.move_set[6]]:
            self.kick_head = True
        # блок
        elif key[self.move_set[7]]:
            self.block = True

    def __reactions(self, speed, collision, attack, win):
        if self.left and not (self.isDucking or self.isJump):
            self.rect.x -= speed
            self.__animation(self.spites['Walking'], reverse=self.direction)

        elif self.right and not (self.isDucking or self.isJump):
            self.rect.x += speed
            self.__animation(self.spites['Walking'], reverse=not self.direction)

        elif self.block:
            self.__animation(self.spites['Block'], once=True)

        elif self.isDucking and not (self.left or self.right or self.isJump):
            self.__animation(self.spites['Ducking'], once=True)

        elif self.isJump and not (self.left or self.right):
            self.__make_jump()

        elif self.isJump and self.right:
            if time() - self.cooldown >= 0.1:  # задержка после прыжка
                self.__make_jump(over=True)
            else:
                self.__animation(self.spites['Fighting Stance'])

        elif self.isJump and self.left:
            if time() - self.cooldown >= 0.1:  # задержка после прыжка
                self.__make_jump(over=True, left=True)
            else:
                self.__animation(self.spites['Fighting Stance'])

        elif self.punch and not (self.left or self.right):
            self.left = self.right = False
            self.punch = self.__make_kick('Punch', 0.3)

        elif self.kick and not (self.left or self.right):
            if time() - self.cooldown >= 0.4:
                self.kick = self.__make_kick('Kick', 0.5)
            else:
                self.__animation(self.spites['Fighting Stance'])

        elif self.kick_head and pygame.K_c and not (self.left or self.right):

            if time() - self.cooldown >= 0.4:
                self.kick_head = self.__make_kick('KickHead')
            else:
                self.__animation(self.spites['Fighting Stance'])
        elif collision and attack and not self.block and self.health:
            self.health -= 1
            if self.health <= 0:
                self.health = 0
            self.__animation(self.spites['BeingHit'])
            choice(self.hit_s).play()
        elif not self.health:
            self.__animation(self.spites['Dead'], once=True)

        elif win:
            self.__animation(self.spites['Win'], once=True)
        else:
            self.__animation(self.spites['Fighting Stance'])

    def __create_sprite_list(self, dir_name: str):
        """
        Создание словаря с мувсетом персонажа
        :param dir_name: имя персонажа
        :return: None
        """
        result = dict()
        dir_path = path.join('characters', dir_name)
        for f in listdir(dir_path):
            folder = path.join(dir_path, f)
            imgs = listdir(folder)
            result[f] = list(map(lambda x: pygame.image.load(path.join(folder, x)).convert(), imgs))
            result[f] = list(map(self.__resize_img, result[f]))
        return result

    @classmethod
    def __resize_img(cls, image) -> pygame.Surface:
        """
        Функция подгона изображений под размер игры
        :param image: спрайт персонажа
        :return: обработанный спрайт
        """
        return pygame.transform.scale(image, (image.get_width() * s.size_c,
                                              image.get_height() * s.size_c))

    def __flip_img(self) -> None:
        """
        Отражает спрайт на 180 градусов
        :return: None
        """
        for key in self.spites.keys():
            self.spites[key] = list(
                map(lambda x: pygame.transform.flip(x, flip_x=True, flip_y=False), self.spites[key]))

    def __animation(self, arr: list, reverse: bool = False, once: bool = False,
                    punch: bool = False) -> None:
        """
        Метод анимации персонажа
        :param arr: список кадров анимации
        :param reverse: показывает анимацию в обратном порядке
        :param once: повторить только один раз
        :param punch: тип анимации "удар"
        :return: None
        """
        old_rect = self.rect.topright
        if not punch:
            self.current_frame = self.__frames(self.current_frame, arr, once, reverse)
        else:
            self.fight_frame = self.__frames(self.fight_frame, arr, once, reverse)
        self.image = pygame.Surface((self.img.get_width(), self.img.get_height()))
        if not self.direction:
            self.rect = self.image.get_rect()
            self.rect.topright = old_rect
        self.image.fill('green')
        self.image.set_colorkey('green')
        self.image.blit(self.img, (0, 0, self.img.get_width(), self.img.get_height()))

    def __frames(self, var, arr, once: bool, reverse: bool) -> int:
        """Перезапускает счётчик фреймов"""
        if var >= len(arr):
            var = 0 if not once else len(arr) - 1
        self.img = arr[int(var)] if not reverse else arr[-int(var)]
        return var

    def __make_jump(self, over: bool = False, left: bool = False) -> None:
        """
        Реализация прыжков
        :param over: прыжок через объект?
        :param left: направление взгляда (по-умолчанию вправо)
        :return: None
        """
        if self.jumpCount >= -s.jump:
            self.isJump = True
            self.rect.y -= int((self.jumpCount * abs(self.jumpCount)) * 0.3)
            self.jumpCount -= 1

            if not over:
                self.__animation([self.spites['Jump'][0]], once=True, reverse=left)
            else:
                self.__animation(self.spites['JumpOver'], left if self.direction else not left)
                self.rect.x += s.width_jump if not left else -s.width_jump
        else:
            self.left = self.right = self.isJump = False
            self.jumpCount = s.jump
            self.cooldown = time()

    def __make_kick(self, kick_type: str, anim_speed: float = 0.5) -> bool:
        """
        Метод отвечающий за обработку анимаций удара
        :param kick_type: тип удара
        :param anim_speed: скорость анимации удара
        :return: статус выполнения анимации (bool)
        """
        if self.fight_frame < len(self.spites[kick_type]) - 1:
            self.fight_frame += anim_speed
            self.__animation(self.spites[kick_type], once=True, punch=True)
            return True
        else:
            self.fight_frame = 0
            self.cooldown = time()
            return False

    def get_posx(self) -> int:
        """Вернуть позицию X"""
        return self.rect.x

    def get_poxy(self) -> int:
        """Вернуть позицию Y"""
        return self.rect.y

    def get_pos(self) -> tuple:
        """Вернуть полную позицию"""
        return self.rect.x, self.rect.y

    def get_w(self) -> int:
        """Вернуть ширину персонажа"""
        return self.image.get_width()

    def get_health(self) -> int:
        """Вернуть здоровье персонажа"""
        return self.health

    def die(self) -> bool:
        """Персонаж не умер?"""
        return not bool(self.health)

    def attack(self) -> bool:
        """Была атака?"""
        return self.kick or self.punch or self.kick_head

    def get_h(self) -> int:
        """Вернуть высоту персонажа"""
        return self.image.get_height()

    def get_direction(self) -> bool:
        """Вернуть направление взгляда"""
        return self.direction

    def set_posx(self, x: int) -> None:
        """
        Задать новую позицию X
        :param x: координаты X
        :return: None
        """
        self.rect.x = x

    def set_posy(self, y: int) -> None:
        """
        Задать новую позицию Y
        :param y: координаты Y
        :return: None
        """
        self.rect.y = y

    def set_flip(self) -> None:
        """
        изменить направление взгляда
        :return: None
        """
        self.__flip_img()
        self.direction = not self.direction
