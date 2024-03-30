from random import randint
from strategy_position import StrategyPosition


class StrategyPositionRandom(StrategyPosition):
    def __init__(self, n_colors, sequences_lengths, computer_delay_seconds=0, press_key_before_computer_moves=False):
        super().__init__(n_colors, sequences_lengths, computer_delay_seconds, press_key_before_computer_moves)

    def _select_position(self, tokens):
        return randint(0, len(tokens))
