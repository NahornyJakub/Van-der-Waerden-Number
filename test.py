import data_reader
from game import Game

config = data_reader.read_json_data('config.json')

filename = f'results-r={int(config["n_colors"])},k={int(config["sequences_lengths"][0])}.txt'
with open(filename, 'a') as file:
    for i in range(int(config["n_tests"])):
        game = Game(config)
        game.play()
        turns = game.turn_counter
        file.write(f'{turns}\n')
