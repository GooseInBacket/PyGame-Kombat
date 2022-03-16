import pygame
from os import path, listdir
from pathlib import Path
from time import time, sleep
from settings import s


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, flip: bool = False, control: bool = True):
        super().__init__()
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
        self.stay = True
        self.block = False
        self.punch = False
        self.kick = False
        self.kickh = False
        self.left = False
        self.right = False
        self.duck = False
        self.jump = False
        self.jump_over = False

        self.cooldown = 0
        self.jumpCount = s.jump
        self.speed = s.speed
        self.health = 1000

    def update(self):
        self.__button_pressing()
        self.__reactions()

    def __button_pressing(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and keys[pygame.K_d] and self.control:
            self.jump = self.jump_over = self.right = True

        elif keys[pygame.K_w] and keys[pygame.K_a] and self.control:
            self.jump = self.jump_over = self.left = True

        elif keys[pygame.K_SPACE] and self.control:
            self.block = True

        elif keys[pygame.K_s] and self.control:
            self.duck = True
            self.left = self.right = self.punch = False

        elif keys[pygame.K_d] and self.control:
            self.right = True
            self.left = False

        elif keys[pygame.K_a] and self.control:
            self.left = True
            self.right = False

        if not keys[pygame.K_a] and self.control:
            self.left = False
            self.stay = True
        if not keys[pygame.K_d] and self.control:
            self.right = False
            self.stay = True
        if not keys[pygame.K_SPACE] and self.control:
            self.block = False

    def __reactions(self):
        if self.jump and self.jump_over and self.right:
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
            self.jump = False

        elif self.jump:
            self.__jump()

        elif self.punch and self.control:
            self.__make_punch()

        elif self.duck:
            self.__animation('Ducking', 0.5, True)

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

        old_rect = self.rect.bottomleft if not self.flip else self.rect.topright
        count = -int(self.frameRate) if reverse else int(self.frameRate) if frame is None else frame

        self.frame = self.sprites[anim][count]
        self.image = pygame.Surface((self.frame.get_width(), self.frame.get_height()))
        self.rect = self.image.get_rect()

        if not self.flip:
            self.rect.bottomleft = old_rect
        else:
            self.rect.topright = old_rect

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
            self.__animation('JumpOver', 0.7, reverse=reverse)
            if reverse:
                self.rect.x -= 10
            else:
                self.rect.x += 10
        else:
            self.left = self.right = self.jump_over = self.jump = False
            self.punch = self.kick = self.kickh = False
            self.jumpCount = s.jump
            self.cooldown = time()
            self.control = True

    def get_pos(self):
        return self.rect.center

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def get_punch(self, n: int):
        if self.block:
            self.block_s.play()
            self.health -= 5
        else:
            self.health -= n
            self.hit_s.play()
            self.__animation('BeingHit', 0.7)
        sleep(0.1)

    def attack(self):
        return self.punch, self.kick, self.kickh

    def get_health(self):
        return self.health

    def stop(self):
        self.speed = 0
        if self.flip:
            self.rect.x += 1
        else:
            self.rect.x -= 1

    def go(self):
        self.speed = s.speed

    def cur_frame(self):
        return int(self.frameRate)


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

    def update(self, pos: tuple, w: int = 100, h: int = 80, body: bool = False, kick: bool = False):
        self.image = pygame.Surface((w, h))
        self.image.fill(self.color)
        self.image.set_alpha(180)
        self.rect = self.image.get_rect()

        if body:
            self.rect.center = pos
        else:
            self.rect.topleft = pos

        if kick:
            self.rect.topleft = pos
            self.rect.y += 50

    def get_pos(self):
        return self.rect.topleft


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()

        self.p = pygame.sprite.Group()
        self.h = pygame.sprite.Group()

        self.player = Player((300, self.screen.get_height() // 2))
        self.player2 = Player((500, self.screen.get_height() // 2), True, False)

        self.body = Hitbox(80, 250)
        self.body2 = Hitbox(80, 250)
        self.hit = Hitbox(200, 50, 'red')

        self.p.add(self.player)
        self.p.add(self.player2)

        self.h.add(self.body)
        self.h.add(self.body2)
        self.h.add(self.hit)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player.jump = True
                    elif event.key == pygame.K_e:
                        self.player.kick = True
                    elif event.key == pygame.K_f:
                        self.player.kickh = True
                    elif event.key == pygame.K_q:
                        self.player.punch = True
                    elif event.key == pygame.K_s:
                        self.player.duck = False

            self.screen.fill('blue')

            self.player.update()
            self.player2.update()
            self.player2.block = True

            self.body.update(self.player.get_pos(),
                             self.player.get_width() // 2,
                             self.player.get_height() // 1.2, body=True)

            self.body2.update(self.player2.get_pos(),
                              self.player2.get_width() // 2,
                              self.player2.get_height() // 1.2, True)

            punch, kick, kickh = self.player.attack()
            if punch and self.player.cur_frame() in (1, 2, 5, 7):
                self.__upd_hit()
                if bool(pygame.sprite.collide_mask(self.hit, self.body2)):
                    self.player2.get_punch(10)
                    print(self.player2.get_health())
                print('Punch', bool(pygame.sprite.collide_mask(self.hit, self.body2)), sep=' - ')

            elif kick and self.player.cur_frame() == 5:
                self.__upd_hit(True)
                if bool(pygame.sprite.collide_mask(self.hit, self.body2)):
                    self.player2.get_punch(20)
                    print(self.player2.get_health())
                print('Kick', bool(pygame.sprite.collide_mask(self.hit, self.body2)), sep=' - ')

            elif kickh and self.player.cur_frame() in (2, 3):
                self.__upd_hit()
                if bool(pygame.sprite.collide_mask(self.hit, self.body2)):
                    self.player2.get_punch(50)
                    print(self.player2.get_health())
                print('KickHead', bool(pygame.sprite.collide_mask(self.hit, self.body2)), sep=' - ')
            else:
                self.hit.kill()

            if pygame.sprite.collide_mask(self.body, self.body2):
                self.player.stop()
                self.player2.stop()
            else:
                self.player.go()
                self.player2.go()

            self.p.draw(self.screen)
            # self.h.draw(self.screen)

            self.clock.tick(30)
            pygame.display.flip()

    def __upd_hit(self, kick: bool = False):
        self.h.add(self.hit)
        self.hit.update(self.body.get_pos(), self.player.get_width() // 1.3, kick=kick)


game = Game()
game.run()
