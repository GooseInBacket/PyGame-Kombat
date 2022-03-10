from game import Game
from settings import s

if __name__ == '__main__':
    game = Game(*s.size)
    game.run()
