import pygame
from player import Player
from hitbox import Hitbox


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()

        self.p = pygame.sprite.Group()
        self.h = pygame.sprite.Group()

        self.player = Player((300, self.screen.get_height() // 2))
        self.player2 = Player((500, self.screen.get_height() // 2), True, True, True)

        self.body = Hitbox(80, 250)
        self.body2 = Hitbox(80, 250)
        self.body2.set_direction()

        self.hit = Hitbox(200, 50, 'red')
        self.hit_2 = Hitbox(200, 50, 'red')
        self.hit_2.direction = False

        self.p.add(self.player)
        self.p.add(self.player2)

        self.h.add(self.body)
        self.h.add(self.body2)

        self.h.add(self.hit)
        self.h.add(self.hit_2)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYUP:
                    # player 1
                    if event.key == pygame.K_w:
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
                    if event.key == pygame.K_UP:
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

            self.screen.fill('blue')

            self.player.update()
            self.player2.update()
            # self.player2.block = True

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

            self.__connect_detected()
            self.__flip_detected()

            self.p.draw(self.screen)
            self.h.draw(self.screen)

            self.clock.tick(30)
            pygame.display.flip()

    def __upd_hit(self, player, hit, body, **kwargs):
        self.h.add(hit)
        hit.update(body.get_pos(),
                   player.get_width() // 1.3,
                   kick=kwargs.get('kick', False), flykick=kwargs.get('flykick', False))

    def __punch_detected(self, player, player_2, hit, body, body_2):
        """

        :param player: модель игрока 1
        :param player_2: модель игрока 2
        :param hit:
        :param body: хитбокс тела игрока 1
        :param body_2: хитбокс игрока 2
        :return:
        """
        punch, kick, kickh, flykick, cut = player.attack()
        if punch and player.cur_frame() in (1, 2, 5, 7):
            self.__upd_hit(player, hit, body)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(10)
                print(player_2.get_health())
            print('Punch', bool(pygame.sprite.collide_mask(hit, body_2)), sep=' - ')

        elif kick and player.cur_frame() == 5:
            self.__upd_hit(player, hit, body, kick=True)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(20)
                print(player_2.get_health())
            print('Kick', bool(pygame.sprite.collide_mask(hit, body_2)), sep=' - ')

        elif cut:
            self.__upd_hit(player, hit, body)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(100, cut=True)
                self.hit.kill()
                print(player_2.get_health())

        elif kickh and player.cur_frame() in (2, 3):
            self.__upd_hit(player, hit, body)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(50)
                print(player_2.get_health())
            print('KickHead', bool(pygame.sprite.collide_mask(hit, body_2)), sep=' - ')

        elif flykick:
            self.__upd_hit(player, hit, body, flykick=flykick)
            if bool(pygame.sprite.collide_mask(hit, body_2)):
                player_2.get_punch(50, crit=True)
                player.flykick = player.jump_over = False

        else:
            hit.kill()

    def __connect_detected(self):
        if pygame.sprite.collide_mask(self.body, self.body2):
            self.player.stop()
            self.player2.stop()
        else:
            self.player.go()
            self.player2.go()

    def __flip_detected(self):
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


game = Game()
game.run()
