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
        self.player_1 = None
        self.player_2 = None

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


s = Settings()
