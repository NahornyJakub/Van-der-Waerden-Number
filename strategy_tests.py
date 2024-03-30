import data_reader
from game import Game
from strategies import strategies_position, strategies_color

config = data_reader.read_json_data('config.json')

game = Game(config)
game.press_key_before_computer_moves = False,
game.enable_colors_in_terminal = False,
game.show_additional_token_sequence_without_indices = True
game.show_detailed_sequence_info = False
game.computer_delay_seconds = 0

# --------------------------------------------------------
game.n_colors = 3
game.sequences_lengths = [5, 3, 5]
game.max_tokens = 30
game.strategy_position = strategies_position[config['strategy_position']](game.n_colors, game.sequences_lengths,
                                                                          game.computer_delay_seconds,
                                                                          game.press_key_before_computer_moves)

assert game.strategy_position.select_position(list('AAAACCCCAAAA')) == 4
assert game.strategy_position.select_position(list('AAAACCCCAAA')) == 0
assert game.strategy_position.select_position(list('AAAACCCCACACAAAACCCCAAAA')) == 16
assert game.strategy_position.select_position(list('AAAABCCCCACACAAAACCCCAAAA')) == 17
assert game.strategy_position.select_position(list('BAAAACCCCACACAAAACCCCAAAA')) == 9
assert game.strategy_position.select_position(list('AAAACCCCBACACAAAACCCCAAAA')) == 0
assert game.strategy_position.select_position(list('BCCCCAAAAB')) == 5
assert game.strategy_position.select_position(list('')) == 0
assert game.strategy_position.select_position(list('AAAACCCCBACACAAAABCCCCAAAA')) == 0
assert game.strategy_position.select_position(list('AAAACCCCACACAAAACCCCAAAAB')) == 16
assert game.strategy_position.select_position(list('AAAACCCCACACAAAACCCCBAAAA')) == 12
assert game.strategy_position.select_position(list('AAAACCCCACACAAAABCCCCAAAA')) == 25
assert game.strategy_position.select_position(list('AAAACCCCACACBAAAACCCCAAAA')) == 21
