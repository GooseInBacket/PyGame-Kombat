import pygame
from random import choice
from os import path, listdir
from pathlib import Path
from time import time, sleep
from data.settings import s


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, flip: bool = False, control: bool = True, player_2: bool = False,
                 name: str = 'subzero'):
        """
        Game character model
        :param pos: The position of the player on the game canvas
        :param flip: Character reflected
        :param control: Have character control
        :param player_2: Is this the second player?
        :param name: Model name
        """
        super().__init__()

        self.name = name
        self.player = player_2

        if not self.player:
            self.keys = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a,
                         'right': pygame.K_d, 'punch': pygame.K_q, 'kick': pygame.K_e,
                         'kickhead': pygame.K_f, 'block': pygame.K_SPACE}
        else:
            self.keys = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT,
                         'right': pygame.K_RIGHT, 'punch': pygame.K_KP1, 'kick': pygame.K_KP2,
                         'kickhead': pygame.K_KP3, 'block': pygame.K_KP0}

        self.flip = flip
        self.sprites = self.__create_sprite_list(name)

        sound = pygame.mixer.Sound
        self.hit_s = [sound(Path('data', 'content', 'sound', f'{str(i).rjust(2, "0")}.mp3'))
                      for i in range(5, 13)]

        self.block_s = pygame.mixer.Sound(Path('data', 'content', 'sound', 'mk1-00049.mp3'))
        for i in self.hit_s:
            i.set_volume(s.get_sound())
        self.block_s.set_volume(s.sound)

        if self.flip:
            self.__flip_img()

        self.buttons = [pygame.K_d, pygame.K_a, pygame.K_q, pygame.K_e, pygame.K_f]

        self.frame = self.sprites['Fighting Stance'][0]
        self.image = pygame.Surface((self.frame.get_width(), self.frame.get_height()))
        self.current_key = set()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.frameRate = 0
        self.new_anim = True

        self.control = control
        self.__upd_state()

        self.fall = False
        self.dead = False
        self.win = False

        self.cooldown = 0
        self.jumpCount = s.jump
        self.speed = s.speed
        self.health = 1000

        self.punch_anim = 0
        self.punch_cooldown = 0
        self.t = 0
        self.flag = True

    def update(self) -> None:
        """Tracks button presses and click responses"""
        self.__button_pressing()
        self.__reactions()

    def __upd_state(self) -> None:
        """Обновляет основные переменные"""
        self.dead = False
        self.fall = False
        self.stay = True
        self.block = False
        self.punch = False
        self.kick = False
        self.flykick = False
        self.kickh = False
        self.left = False
        self.right = False
        self.duck = False
        self.jump = False
        self.on_floor = False
        self.jump_over = False
        self.undercut = False

    def __button_pressing(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[self.keys['up']] and keys[self.keys['right']] and self.control:
            self.jump = self.jump_over = self.right = True

        elif keys[self.keys['up']] and keys[self.keys['left']] and self.control:
            self.jump = self.jump_over = self.left = True

        elif keys[self.keys['block']] and self.control:
            self.block = True

        elif keys[self.keys['down']] and self.control:
            self.duck = True
            self.left = self.right = self.punch = False

        elif keys[self.keys['right']] and self.control:
            self.right = True
            self.left = False

        elif keys[self.keys['left']] and self.control:
            self.left = True
            self.right = False

        if not keys[self.keys['left']] and self.control:
            self.left = False
            self.stay = True

        if not keys[self.keys['right']] and self.control:
            self.right = False
            self.stay = True

        if not keys[self.keys['block']] and self.control:
            self.block = False

    def __reactions(self) -> None:
        if self.win:
            self.__upd_state()
            if self.__animation('Win', once=True):
                if self.flag:
                    self.t = time()
                    self.flag = False
                if time() - self.t > 2:
                    s.fight = False
            self.rect.y = 400

        elif self.dead:
            self.__make_fall()

        elif self.fall:
            self.__make_fall('Fall')

        elif self.duck:
            if self.kickh:
                if self.new_anim:
                    self.frameRate = 0
                    self.new_anim = False
                    self.duck = self.undercut = True
                if self.__animation('Undercut', 0.5, once=True):
                    self.kickh = self.undercut = self.duck = False
                    self.new_anim = True
            else:
                self.__animation('Ducking', frame=2)

        elif self.jump and self.jump_over and self.right:
            if time() - self.cooldown > 0.2:
                self.__jump_over()
            else:
                self.__animation('Fighting Stance', 0.4)

        elif self.jump and self.jump_over and self.left:
            if time() - self.cooldown > 0.2:
                self.__jump_over(reverse=True)
            else:
                self.__animation('Fighting Stance', 0.4)

        elif self.kick and self.control:
            if self.new_anim:
                self.frameRate = 0
                self.new_anim = False
                self.punch = self.kickh = False

            if self.__animation('Kick', 0.5):
                self.kick = False
                self.new_anim = True

        elif self.kickh and self.control:
            if self.new_anim:
                self.frameRate = 0
                self.new_anim = False
                self.punch = self.kick = False

            if self.__animation('KickHead', 0.5):
                self.kickh = False
                self.new_anim = True

        elif self.block:
            self.__animation('Block', once=True)
            self.jump = self.punch = self.kickh = self.kick = False

        elif self.jump:
            self.__jump()

        elif self.punch and self.control:
            self.__make_punch()

        elif self.left:
            self.rect.x -= self.speed
            self.__animation('Walking', 0.4, reverse=True)

        elif self.right:
            self.rect.x += self.speed
            self.__animation('Walking', 0.4)

        elif self.stay:
            self.__animation('Fighting Stance', 0.4)

    def __animation(self, anim: str, speed: int | float = 0.4, once: bool = False,
                    reverse: bool = False, frame: int = None) -> bool:
        """
        Sprite animation function
        :param anim: name animation in sprite list
        :param speed: speed animation
        :param once: play animation once
        :param reverse: flip animation
        :param frame: run specific frame
        :return: bool
        """
        length = len(self.sprites[anim])
        if once and int(self.frameRate) == length - 1:
            return True

        self.frameRate += speed
        self.frameRate %= length

        old_rect = self.rect.bottomleft if not self.flip else self.rect.bottomright
        if self.flip and anim not in ('Kick', 'KickHead', 'Punch', 'Dead', 'Up'):
            count = int(self.frameRate) if reverse else -int(
                self.frameRate) if frame is None else frame
        else:
            count = -int(self.frameRate) if reverse else int(
                self.frameRate) if frame is None else frame

        self.frame = self.sprites[anim][
            length - 1 if once and int(self.frameRate) == length - 1 else count]
        self.image = pygame.Surface((self.frame.get_width(), self.frame.get_height()))
        self.rect = self.image.get_rect()

        if not self.flip:
            self.rect.bottomleft = old_rect
        else:
            self.rect.bottomright = old_rect

        self.image.fill('green')
        self.image.set_colorkey('green')
        self.image.blit(self.frame, (0, 0, self.frame.get_width(), self.frame.get_height()))

        if int(self.frameRate) == length - 1:
            return True

    def __create_sprite_list(self, dir_name: str) -> dict:
        result = dict()
        dir_path = path.join('data', 'characters', dir_name)
        for f in listdir(dir_path):
            folder = path.join(dir_path, f)
            imgs = listdir(folder)
            result[f] = list(map(lambda x: pygame.image.load(path.join(folder, x)).convert(), imgs))
            result[f] = list(map(self.__resize_img, result[f]))
        return result

    @classmethod
    def __resize_img(cls, image) -> pygame.Surface:
        width = image.get_width() * s.size_c
        height = image.get_height() * s.size_c
        return pygame.transform.scale(image, (width, height))

    def __flip_img(self) -> None:
        for key in self.sprites.keys():
            self.sprites[key] = list(
                map(lambda x: pygame.transform.flip(x, True, False), self.sprites[key]))

    def __make_punch(self) -> None:
        length = len(self.sprites['Punch'])
        self.jump = False

        if time() - self.punch_cooldown <= 0.5:
            self.punch_anim += 0.4
            self.punch_anim %= length
            self.__animation('Punch', frame=int(self.punch_anim))
        else:
            self.punch_cooldown = time()
            self.punch = False

    def __jump(self) -> None:
        self.control = False
        if self.jumpCount >= -s.jump:
            self.jump = True
            self.rect.y -= int((self.jumpCount * abs(self.jumpCount)) * 0.3)
            self.jumpCount -= 1
            self.__animation('Jump', frame=0)
        else:
            self.left = self.right = self.jump = False
            self.punch = self.kick = self.kickh = False
            self.jumpCount = s.jump
            self.control = True

    def __jump_over(self, reverse: bool = False) -> None:
        self.control = False
        if self.jumpCount >= -s.jump:
            self.jump_over = True
            self.rect.y -= int((self.jumpCount * abs(self.jumpCount)) * 0.3)
            self.jumpCount -= 1
            if self.kick:
                self.flykick = True
                self.__animation('FlyKick', 0.7)
            else:
                self.__animation('JumpOver', 0.7, reverse=reverse)
            self.kickh = self.punch = False
            if reverse:
                self.rect.x -= 10
            else:
                self.rect.x += 10
        else:
            self.left = self.right = self.jump_over = self.jump = False
            self.punch = self.kick = self.kickh = self.flykick = False
            self.jumpCount = s.jump
            self.cooldown = time()
            self.control = True

    def __make_fall(self, name: str = 'Dead') -> None:
        """fall/death animation"""
        if self.new_anim:
            self.frameRate = 0
            self.new_anim = False

        if self.__animation(name, 0.5, once=True):
            self.punch = self.kick = self.kickh = False
            if self.jump or self.jump_over or self.duck or self.left or self.right:
                self.jump = False
                self.on_floor = True
                self.dead = False
                self.fall = False
                self.control = True
        else:
            if name == 'Dead':
                self.rect.x += 20 if self.flip else -20
                if self.jumpCount != s.jump:
                    self.jumpCount = s.jump
                    self.jump = self.right = self.left = self.kick = False
                    self.control = True

                if self.rect.y < s.size[1] // 2:
                    self.rect.y += 25
                    self.rect.y = s.size[1] // 2

    def get_pos(self) -> tuple:
        return self.rect.center

    def get_width(self) -> int:
        return self.image.get_width()

    def get_height(self) -> int:
        return self.image.get_height()

    def get_punch(self, n: int, **kwargs) -> None:
        if self.block:
            self.block_s.play()
            self.health -= 2
        else:
            if kwargs.get('crit', False) and not self.block:
                self.dead = True
            elif kwargs.get('cut', False) and not self.block:
                self.fall = True
            else:
                self.__make_fall('BeingHit')
            self.health -= n
            choice(self.hit_s).play()
        sleep(0.05)

    def attack(self) -> tuple:
        return self.punch, self.kick, self.kickh, self.flykick, self.undercut

    def get_health(self) -> int:
        return self.health

    def get_flip(self) -> bool:
        return self.flip

    def stop(self) -> None:
        """Stop character when touching another character"""
        self.speed = 0
        if self.flip:
            self.rect.x += 1
        else:
            self.rect.x -= 1

    def mirror(self) -> None:
        """Reflect character model"""
        self.__flip_img()
        self.flip = not self.flip

    def go(self) -> None:
        """Возобновить движение персонажа"""
        self.speed = s.speed

    def cur_frame(self) -> int:
        """current animation frame"""
        return int(self.frameRate)
