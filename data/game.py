import pygame
import sys

from pathlib import Path
from random import randint
from time import sleep

from .player import Player
from .hitbox import Hitbox
from .main_menu import Menu
from .hud import Hud

from data.settings import s


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('MK ALPHA v.1.1')
        pygame.display.set_icon(pygame.image.load(Path('data', 'content', 'props', 'logo.png')))

        self.font = pygame.font.Font(Path('data', 'content', 'font', 'mortalkombat1.ttf'), 50)
        self.pause_text = self.font.render('pause', True, 'white')

        self.screen = pygame.display.set_mode(s.size)
        self.clock = pygame.time.Clock()

        self.p = pygame.sprite.Group()
        self.h = pygame.sprite.Group()

        self.hud = None

        img = pygame.image.load(Path('data', 'content', 'maps', f'0{randint(1, 3)}.png')).convert()
        self.background = pygame.transform.scale(img, s.size)
        self.background_rect = self.background.get_rect()

    def run(self) -> None:
        """run game func"""
        while True:
            s.win_p_1 = s.win_p_2 = 0
            s.round = 1

            menu = Menu(self.clock)
            menu.set_menu(self.screen)
            menu.choose_your_fighter(self.screen)

            music = pygame.mixer.Sound(Path('data', 'content', 'sound', '03.mp3'))
            music.set_volume(s.get_music())
            music.play(-1)
            while s.win_p_1 != 2 and s.win_p_2 != 2:
                s.fight = True
                self.__fight()
                self.p.empty()
                self.h.empty()
                self.hud = None

            if s.win_p_1 == 2:
                win_s = pygame.mixer.Sound(Path('data', 'content', 'sound', f'{s.player_1}win.mp3'))
            else:
                win_s = pygame.mixer.Sound(Path('data', 'content', 'sound', f'{s.player_2}win.mp3'))
            win_s.set_volume(s.sound)

            music.stop()
            win_s.play()
            sleep(2)

    def __fight(self) -> None:
        """fight round func"""
        self.player = Player((250, self.screen.get_height() // 2), name=s.player_1)
        self.player2 = Player((s.size[0] - 410, self.screen.get_height() // 2), True, True, True,
                              name=s.player_2)
        self.player.control = self.player2.control = False

        self.body = Hitbox(80, 250)
        self.body2 = Hitbox(80, 250)
        self.body2.set_direction()

        self.hit = Hitbox(200, 50, 'red')
        self.hit_2 = Hitbox(200, 50, 'red')
        self.hit_2.direction = False

        self.hud = Hud(s.player_1, s.player_2)

        self.p.add(self.player)
        self.p.add(self.player2)

        self.h.add(self.body)
        self.h.add(self.body2)

        self.h.add(self.hit)
        self.h.add(self.hit_2)

        self.pause = False

        while s.fight:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYUP:
                    # player 1
                    if event.key == pygame.K_w and self.player.control:
                        self.player.jump = True
                    elif event.key == pygame.K_e:
                        self.player.kick = True
                    elif event.key == pygame.K_f:
                        self.player.kickh = True
                    elif event.key == pygame.K_q:
                        self.player.punch = True
                    elif event.key == pygame.K_s:
                        if self.player.duck and not self.player.kickh:
                            self.player.duck = False
                            self.player.kickh = False

                    # player 2
                    if event.key == pygame.K_UP and self.player2.control:
                        self.player2.jump = True
                    elif event.key == pygame.K_KP1:
                        self.player2.kick = True
                    elif event.key == pygame.K_KP2:
                        self.player2.kickh = True
                    elif event.key == pygame.K_KP3:
                        self.player2.punch = True
                    elif event.key == pygame.K_DOWN:
                        if self.player2.duck and not self.player2.kickh:
                            self.player2.duck = False
                            self.player2.kickh = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = not self.pause

            if self.pause:
                self.__pause()
                continue

            if self.player.get_health() <= 0:
                self.player.control = False
                self.player2.control = False
                self.player2.win = True
                self.player.dead = True

            if self.player2.get_health() <= 0:
                self.player.control = False
                self.player2.control = False
                self.player.win = True
                self.player2.dead = True

            self.screen.blit(self.background, self.background_rect)

            if self.hud.update(self.player.get_health(), self.player2.get_health()):
                self.player.control = self.player2.control = True
            self.hud.draw(self.screen)

            if self.player.get_health() <= 0:
                pass

            self.player.update()
            self.player2.update()

            self.body.update(self.player.get_pos(),
                             self.player.get_width() // 2,
                             self.player.get_height() // 1.2,
                             body=True)

            self.body2.update(self.player2.get_pos(),
                              self.player2.get_width() // 2,
                              self.player2.get_height() // 1.2,
                              body=True)

            self.__punch_detected(self.player, self.player2, self.hit, self.body, self.body2)
            self.__punch_detected(self.player2, self.player, self.hit_2, self.body2, self.body)

            self.__collide_detected(self.player)
            self.__collide_detected(self.player2)
            self.__flip_detected()

            self.p.draw(self.screen)
            # self.h.draw(self.screen)

            self.clock.tick(30)
            pygame.display.flip()

        s.round += 1
        if self.player.get_health() <= 0:
            s.win_p_2 += 1
        elif self.player2.get_health() <= 0:
            s.win_p_1 += 1
        sleep(1)
        return

    def __upd_hit(self, player, hit, body, **kwargs) -> None:
        """updates hitbox hit"""
        self.h.add(hit)
        hit.update(body.get_pos(),
                   player.get_width() // 1.3,
                   kick=kwargs.get('kick', False), flykick=kwargs.get('flykick', False))

    def __punch_detected(self, player: Player, player_2: Player,
                         hit: Hitbox, body: Hitbox, body_2: Hitbox) -> None:
        """

        :param player: models player 1
        :param player_2: models player 2
        :param hit: hitbox hit player 1
        :param body: hitbox body player 1
        :param body_2: hitbox body player 2
        :return: None
        """
        punch, kick, kickh, flykick, cut = player.attack()
        name = player.name

        if punch:
            self.__upd_hit(player, hit, body)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(5)

        elif kick and (player.cur_frame() in s.get_kick_set(name)):
            self.__upd_hit(player, hit, body, kick=True)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(20)

        elif cut:
            self.__upd_hit(player, hit, body)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(10, cut=True)
                self.hit.kill()

        elif kickh and (player.cur_frame() in s.get_kickh_set(name)):
            self.__upd_hit(player, hit, body)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(50)

        elif flykick:
            self.__upd_hit(player, hit, body, flykick=flykick)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(50, crit=True)
                player.flykick = player.jump_over = False

        else:
            hit.kill()

    def __collide_detected(self, player: Player) -> None:
        """Tracks the touch of two players"""
        if pygame.sprite.collide_mask(self.body, self.body2):
            player.stop()
        else:
            player.go()

        if player.rect.x < 0:
            player.rect.x = 0
        elif player.rect.x > s.size[0] - player.get_width():
            player.rect.x = s.size[0] - player.get_width()

    def __flip_detected(self) -> None:
        """Tracking the turn of the player model"""
        if self.body.get_center_x() > self.body2.get_center_x() and not self.player.get_flip():
            self.player.mirror()
            self.player2.mirror()
            self.body.set_direction()
            self.body2.set_direction()
            self.hit.set_direction()
            self.hit_2.set_direction()

        elif self.body.get_center_x() < self.body2.get_center_x() and self.player.get_flip():
            self.player.mirror()
            self.player2.mirror()
            self.body.set_direction()
            self.body2.set_direction()
            self.hit.set_direction()
            self.hit_2.set_direction()

    def __pause(self) -> None:
        """pause func"""
        pause_screen = pygame.Surface(s.size)
        pause_screen.fill('#141414')
        pause_screen.set_alpha(5)

        self.screen.blit(pause_screen, (0, 0))
        pos = (s.size[0] // 2 - self.pause_text.get_width() // 2, s.size[1] // 2)
        self.screen.blit(self.pause_text, pos)
        pygame.display.flip()


def run_game() -> None:
    """Run Game func"""
    game = Game()
    game.run()
