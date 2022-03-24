class Settings:
    def __init__(self):
        # game
        self.fps = 30
        self.size = (1200, 800)
        self.sound = 0.1
        self.music = 0.1

        # player
        self.speed = 7
        self.jump = 15
        self.width_jump = 8
        self.size_c = 2.5
        self.anim = 0.4
        self.player_1 = 'subzero'
        self.player_2 = 'subzero'

        self.moveset = {
            'johny': {'punch': (5, 7), 'kick': (3, ), 'kickh': (2, )},
            'kano': {'punch': (2, 3, 4, 5, 7), 'kick': (4, ), 'kickh': (2, )},
            'liu kang': {'punch': (2, 5, 7), 'kick': (4, ), 'kickh': (3, )},
            'raiden': {'punch': (2, 5), 'kick': (3, ), 'kickh': (2, )},
            'scorpion': {'punch': (1, 2, 5, 7), 'kick': (5, ), 'kickh': (2, 3)},
            'sonya': {'punch': (2, 5, 6, 7), 'kick': (2, 6), 'kickh': (3, )},
            'subzero': {'punch': (1, 2, 5, 7), 'kick': (5, ), 'kickh': (2, 3)},
        }

    def set_sound(self, volume: float):
        self.sound = volume

    def set_music(self, volume: float):
        self.music = volume

    def set_player_1(self, name: str):
        self.player_1 = name

    def set_player_2(self, name: str):
        self.player_2 = name

    def get_sound(self):
        return self.sound

    def get_music(self):
        return self.music

    def get_player1(self):
        return self.player_1

    def get_player2(self):
        return self.player_2

    def get_punch_set(self, name: str) -> tuple:
        return self.moveset[name]['punch']

    def get_kick_set(self, name: str) -> tuple:
        return self.moveset[name]['kick']

    def get_kickh_set(self, name: str) -> tuple:
        return self.moveset[name]['kickh']


s = Settings()
