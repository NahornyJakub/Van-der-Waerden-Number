import data_reader
from game import Game

config = data_reader.read_json_data('config.json')

while True:
    game = Game(config)
    play_next = game.play()
    if not play_next:
        break
