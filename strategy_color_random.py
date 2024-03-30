from random import randint
from strategy_color import StrategyColor


class StrategyColorRandom(StrategyColor):
    def __init__(self, n_colors, sequences_lengths, computer_delay_seconds=0, press_key_before_computer_moves=False):
        super().__init__(n_colors, sequences_lengths, computer_delay_seconds, press_key_before_computer_moves)

    def _select_token(self, tokens, position):
        return self.color_to_token(randint(0, self.n_colors - 1))
