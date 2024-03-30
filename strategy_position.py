from abc import ABC, abstractmethod
from strategy import Strategy


class StrategyPosition(Strategy, ABC):
    def __init__(self, n_colors, sequences_lengths, computer_delay_seconds=0, press_key_before_computer_moves=False):
        super().__init__(n_colors, sequences_lengths, computer_delay_seconds, press_key_before_computer_moves)

    def select_position(self, tokens):
        self.wait_before_move()
        if self.press_key_before_computer_moves:
            input('Computer\'s move, press any key...')
        position = self._select_position(tokens)
        print(f'Computer has chosen position: {position}')
        return position

    @abstractmethod
    def _select_position(self, tokens):
        pass
