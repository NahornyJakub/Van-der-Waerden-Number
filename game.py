from strategies import strategies_position, strategies_color


class Game:
    def __init__(self, config):
        self.config = config
        self.check_config_parameters()
        self.n_colors = int(config['n_colors'])
        self.sequences_lengths = config['sequences_lengths']
        self.max_tokens = int(config['max_tokens'])
        self.game_type = config['game_type']
        self.computer_delay_seconds = float(config['computer_delay_seconds'])
        self.press_key_before_computer_moves = config['press_key_before_computer_moves']
        self.enable_colors_in_terminal = config['enable_colors_in_terminal']
        self.show_additional_token_sequence_without_indices = config['show_additional_token_sequence_without_indices']
        self.show_detailed_sequence_info = config['show_detailed_sequence_info']
        self.strategy_position = strategies_position[config['strategy_position']](self.n_colors, self.sequences_lengths,
                                                                                  self.computer_delay_seconds,
                                                                                  self.press_key_before_computer_moves)
        self.strategy_color = strategies_color[config['strategy_color']](self.n_colors, self.sequences_lengths,
                                                                         self.computer_delay_seconds,
                                                                         self.press_key_before_computer_moves)
        self.test_mode = config['test_mode']
        self.tokens = []
        self.turn_counter = 0
        self.winning_sequence = []

    @staticmethod
    def print_hello():
        start_info = """
-------------------------------------------------------------------------
|     Welcome to the game Off-diagonal Van der Waerden numbers game!    |
|                                                                       |
| Rules:                                                                |
| - There are r colors                                                  |
| - {k1, k2, ..., kr} are the required sequences lenghts for each color |
| - n is the maximum number of tokens                                   |
|                                                                       |
| - Two players build a string of colored tokens                        |
| - First player chooses where to place the token                       |
| - Tokens are placed next to each other in one line                    |
| - In each turn a token can be placed just before,                     |
|   immediately behind, or somewhere in between the line                |
| - Second player chooses the color of the token to be placed           |
| - First player wins when a MONOCHROME ARITHMETIC SEQUENCE             |
|   of color ki (i = 1, ..., r) is present in the line                  |
| - Second player wins after placing n tokens and when no               |
|   above-mentioned sequences are present                               |
-------------------------------------------------------------------------
        """
        print(start_info)
        input('Press any key to continue...')

    def print_end(self):
        winner = 1 if self.winning_sequence else 2
        COLOR_BLUE = '\033[94m' if self.enable_colors_in_terminal else ''
        COLOR_END = '\033[0m' if self.enable_colors_in_terminal else ''
        if winner == 1:
            print(
                f'\n{COLOR_BLUE}Player 1 won! Winning sequence: {", ".join(list(map(lambda y: str(y + 1), self.winning_sequence)))}{COLOR_END}\n')
            for i, token in enumerate(self.tokens):
                token_to_be_printed = token
                if i in self.winning_sequence:
                    if self.enable_colors_in_terminal:
                        token_to_be_printed = COLOR_BLUE + token_to_be_printed + COLOR_END
                    if len(self.winning_sequence) > 1 and (
                            self.winning_sequence[1] - self.winning_sequence[0] > 1 or self.winning_sequence[-1] == i):
                        token_to_be_printed = ' ' + token_to_be_printed + ' '
                    else:
                        token_to_be_printed = ' ' + token_to_be_printed
                print(f'{token_to_be_printed}', sep=' ', end='', flush=True)
            print('\n')
        else:
            print(
                f'\n{COLOR_BLUE}Player 2 won! {self.max_tokens} tokens were placed and no winning sequence was found{COLOR_END}\n')

    @staticmethod
    def ask_if_wanna_play_again():
        while True:
            value = input('Do you want to play again...? (y/n): ')
            if value == 'y' or value == 'Y':
                return True
            elif value == 'n' or value == 'N':
                return False
            else:
                print('Incorrect value, try again!')

    def check_config_parameters(self):
        n_colors = int(self.config['n_colors'])
        if not (1 <= n_colors <= 52):
            raise Exception('Invalid number of colors! Should be between 1 and 52')
        sequences_lengths = self.config['sequences_lengths']
        if len(sequences_lengths) != n_colors:
            raise Exception(
                f'Array of sequences lengths ({len(sequences_lengths)}) should match number of colors ({n_colors})!')
        for i, sequence_length in enumerate(sequences_lengths):
            if not (1 <= int(sequence_length) <= 1000):
                raise Exception(
                    f'Invalid sequence length on position {i} ({sequence_length})! Should be between 1 and 1000')
        max_tokens = int(self.config['max_tokens'])
        if not (1 <= max_tokens <= 100000):
            raise Exception('Invalid number of max tokens! Should be between 1 and 100000')
        game_type = self.config['game_type']
        allowed_game_types = ['human vs computer', 'computer vs human', 'computer vs computer']
        if game_type not in allowed_game_types:
            raise Exception(
                f'"{game_type}" is an invalid game type! Game type should be one of: {", ".join(allowed_game_types)}')
        strategy_position = self.config['strategy_position']
        if strategy_position not in strategies_position.keys():
            raise Exception(
                f'"{strategy_position}" is not known strategy for choosing position! It should be one of: {", ".join(strategies_position.keys())}')
        strategy_color = self.config['strategy_color']
        if strategy_color not in strategies_color.keys():
            raise Exception(
                f'"{strategy_color}" is not known strategy for choosing color! It should be one of: {", ".join(strategies_color.keys())}')
        boolean_parameters = ['enable_colors_in_terminal', 'show_additional_token_sequence_without_indices',
                              'show_detailed_sequence_info', 'press_key_before_computer_moves', 'test_mode']
        for boolean_parameter in boolean_parameters:
            if type(self.config[boolean_parameter]) != bool:
                raise Exception(f'"{boolean_parameter}" parameter should be boolean!')
        computer_delay_seconds = float(self.config['computer_delay_seconds'])
        if computer_delay_seconds < 0:
            raise Exception(f'"computer_delay_seconds" should be a non-negative float value!')

    def play(self):
        if not self.test_mode:
            self.print_hello()
        while self.turn_counter < self.max_tokens:
            position = self.select_position()
            token = self.select_token(position)
            self.place_token(position, token)
            self.turn_counter += 1
            best_sequences = self.strategy_position.find_best_sequences(self.tokens)
            self.print_stats(best_sequences)
            self.visualize_board()
            self.winning_sequence = self.strategy_position.check_for_winning_sequence(best_sequences)
            if self.winning_sequence:
                break
        self.print_end()
        if not self.test_mode:
            return self.ask_if_wanna_play_again()

    def select_position(self):
        if self.game_type == 'human vs computer':
            if self.turn_counter == 0:
                print('First turn - you can only place token at position 0. Press any key to continue...')
                return 0
            else:
                while True:
                    position = input(
                        f'Where do you want to place your token? Allowed positions - from 0 to {len(self.tokens)}: ')
                    bad_value = False
                    try:
                        position = int(position)
                        if not (0 <= position <= len(self.tokens)):
                            bad_value = True
                    except ValueError:
                        bad_value = True
                    if bad_value:
                        print(f'\nIncorrect value! Should be a non-negative integer from range 0 to {len(self.tokens)}')
                    else:
                        return position
        else:
            return self.strategy_position.select_position(self.tokens)

    def select_token(self, position):
        if self.game_type == 'computer vs human':
            while True:
                if self.strategy_color.n_colors <= 26:
                    possible_tokens_text = f'from A to {chr(ord("A") + self.strategy_color.n_colors - 1)}'
                elif self.strategy_color.n_colors == 27:
                    possible_tokens_text = f'from A to Z, a'
                else:
                    possible_tokens_text = f'from A to Z, from a to {chr(ord("a") + self.strategy_color.n_colors - 27)}'
                possible_tokens_text += f' ({self.strategy_color.n_colors} possibilities)'
                token = input(f'Which token do you want it to be? Allowed tokens: {possible_tokens_text}: ')
                if self.is_token_allowed(token):
                    return token
                else:
                    print('Incorrect token! Choose again')
        else:
            return self.strategy_color.select_token(self.tokens, position)

    def is_token_allowed(self, token):
        if len(token) != 1:
            return False
        if self.n_colors <= 26:
            return ord('A') <= ord(token) <= ord('A') + self.n_colors - 1
        else:
            return ord('A') <= ord(token) <= ord('Z') or ord('a') <= ord(token) <= ord('a') + self.n_colors - 27

    def place_token(self, position, token):
        self.tokens.insert(position, token)
        COLOR_GREEN = '\033[92m' if self.enable_colors_in_terminal else ''
        COLOR_END = '\033[0m' if self.enable_colors_in_terminal else ''
        print(
            f'\nToken {COLOR_GREEN}{token}{COLOR_END} was placed on position {COLOR_GREEN}{position}{COLOR_END}\n')

    def visualize_board(self):
        print('-' * 80)

        if len(self.tokens) == 0:
            return

        COLOR_YELLOW = '\033[33m'
        COLOR_GREY = '\033[90m'
        COLOR_END = '\033[0m'

        for i, token in enumerate(self.tokens):
            if self.enable_colors_in_terminal:
                print(f'{COLOR_YELLOW}{token}{COLOR_END} ', sep=' ', end='', flush=True)
                print(f'{COLOR_GREY}{i + 1}{COLOR_END}  ', sep=' ', end='', flush=True)
            else:
                print(f'{token} ', sep=' ', end='', flush=True)
                print(f'({i + 1})  ', sep=' ', end='', flush=True)

        print('\n')
        if self.show_additional_token_sequence_without_indices:
            if self.enable_colors_in_terminal:
                print(f'board: {COLOR_YELLOW}{"".join(self.tokens)}{COLOR_END}')
            else:
                print(f'board: {"".join(self.tokens)}')

    def print_stats(self, best_stats):
        if not self.show_detailed_sequence_info:
            return
        for token, info in best_stats.items():
            winning_length_index = ord(token) - ord('A') if self.n_colors < 26 else ord(token) - ord('a') + 26
            winning_length = self.sequences_lengths[winning_length_index]
            print(f'{token} - best sequence length {info["best_sequence_length"]} (winning length: {winning_length})')
            if info["best_sequence_length"] > 0:
                print(
                    f'    best sequences for {token} found at: {", ".join(map(lambda x: str(list(map(lambda y: y + 1, x))), info["sequences_indices"]))}')
