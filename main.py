from game import Game
from data.settings import s

if __name__ == '__main__':
    game = Game(*s.size)
    game.run()
