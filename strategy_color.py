from abc import ABC, abstractmethod
from strategy import Strategy


class StrategyColor(Strategy, ABC):
    def __init__(self, n_colors, sequences_lengths, computer_delay_seconds=0, press_key_before_computer_moves=False):
        super().__init__(n_colors, sequences_lengths, computer_delay_seconds, press_key_before_computer_moves)

    def select_token(self, tokens, position):
        self.wait_before_move()
        if self.press_key_before_computer_moves:
            input('Computer\'s move, press any key...')
        token = self._select_token(tokens, position)
        print(f'Computer has chosen token: {token}')
        return token

    @abstractmethod
    def _select_token(self, tokens, position):
        pass
