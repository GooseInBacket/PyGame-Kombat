import pygame
from os import path, listdir
from pathlib import Path
from time import time, sleep
from settings import s


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, flip: bool = False, control: bool = True, player_2: bool = False):
        super().__init__()

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
        self.sprites = self.__create_sprite_list('subzero')

        self.hit_s = pygame.mixer.Sound(Path('11.mp3'))
        self.block_s = pygame.mixer.Sound(Path('mk1-00049.mp3'))
        self.hit_s.set_volume(s.sound)
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

        self.cooldown = 0
        self.jumpCount = s.jump
        self.speed = s.speed
        self.health = 1000

    def update(self):
        self.__button_pressing()
        self.__reactions()

    def __upd_state(self):
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

    def __button_pressing(self):
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

    def __reactions(self):
        if self.duck:
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

        elif self.fall:
            self.__make_fall()

        elif self.on_floor:
            self.__stand_up()

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
                    reverse: bool = False, frame: int = None):
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

        self.frame = self.sprites[anim][count]
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

    def __create_sprite_list(self, dir_name: str):
        result = dict()
        dir_path = path.join(dir_name)
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

    def __make_punch(self):
        self.jump = False
        if self.new_anim:
            self.frameRate = 0
            self.new_anim = self.kick = self.kickh = False
            self.cooldown = time()
        self.__animation('Punch', 0.4)
        if int(self.frameRate) in (2, 5):
            if time() - self.cooldown < 0.5:
                self.punch = self.new_anim = False
            self.cooldown = time()

    def __jump(self):
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

    def __jump_over(self, reverse: bool = False):
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

    def __make_fall(self, name: str = 'Dead'):
        print(self.new_anim)
        if self.new_anim:
            self.frameRate = 0
            self.new_anim = False
            self.cooldown = time()

        if self.__animation(name, 0.5, once=True):
            if name in ('Dead', 'Fall') and time() - self.cooldown > 0.5:
                self.fall = False
                self.on_floor = True
                self.new_anim = True
                self.cooldown = time()
            elif name not in ('Dead', 'Fall'):
                self.fall = False
                self.kickh = False
                self.new_anim = True
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

    def __stand_up(self):
        if self.new_anim:
            self.frameRate = 0
            self.new_anim = False
        if self.__animation('Up', 0.5, once=True):
            self.on_floor = False
            self.new_anim = True

    def get_pos(self):
        return self.rect.center

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def get_punch(self, n: int, **kwargs):
        if self.block:
            self.block_s.play()
            self.health -= 5
        else:
            if kwargs.get('crit', False) and not self.block:
                self.health -= n
                self.fall = True
            elif kwargs.get('cut', False) and not self.block:
                self.__make_fall('Fall')
            else:
                self.__make_fall('BeingHit')
            self.hit_s.play()
        sleep(0.05)

    def attack(self):
        return self.punch, self.kick, self.kickh, self.flykick, self.undercut

    def get_health(self):
        return self.health

    def get_flip(self):
        return self.flip

    def stop(self):
        self.speed = 0
        if self.flip:
            self.rect.x += 1
        else:
            self.rect.x -= 1

    def mirror(self):
        self.__flip_img()
        self.flip = not self.flip

    def go(self):
        self.speed = s.speed

    def cur_frame(self):
        return int(self.frameRate)
