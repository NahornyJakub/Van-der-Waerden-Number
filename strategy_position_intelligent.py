from random import randint

from strategy_position import StrategyPosition


class StrategyPositionIntelligent(StrategyPosition):
    def __init__(self, n_colors, sequences_lengths, computer_delay_seconds=0, press_key_before_computer_moves=False):
        self.closing_positions = {}
        super().__init__(n_colors, sequences_lengths, computer_delay_seconds, press_key_before_computer_moves)

    def _select_position(self, tokens):
        position = None
        if len(tokens) == 0 or self.n_colors == 1:
            return 0
        if self.n_colors == 2:
            return self.select_position_two_colors(tokens)

        best_sequences_info = self.find_best_sequences(tokens)
        self.closing_positions = self.find_all_closing_positions_of_sequences(tokens, best_sequences_info)
        winning_position = self.find_winning_position(self.closing_positions)
        if winning_position:
            return winning_position

        if self.n_colors == 3:
            position = self.select_position_three_colors(tokens)
        if position is None:
            position = self.select_most_promising_position()
            if position is None:
                position = randint(0, len(tokens))
        return position

    def select_position_two_colors(self, tokens):
        for i, token in enumerate(tokens):
            if i == 0:
                continue
            if token != tokens[i - 1]:
                return i
        return len(tokens)

    def select_position_three_colors(self, tokens):
        if 2 in self.sequences_lengths:
            return self.select_position_three_colors_when_some_color_equals_two(tokens)
        elif 3 in self.sequences_lengths:
            return self.select_position_three_colors_when_some_color_equals_three_and_others_are_equal(tokens)
        return None

    def select_position_three_colors_when_some_color_equals_two(self, tokens):
        index_2 = self.sequences_lengths.index(2)
        special_token = self.color_to_token(index_2)
        index_special_token = tokens.index(special_token) if special_token in tokens else None
        if index_special_token is None:
            return self.select_position_two_colors(tokens)
        return index_special_token + self.select_position_two_colors(tokens[index_special_token + 1:]) + 1

    def select_position_three_colors_when_some_color_equals_three_and_others_are_equal(self, tokens):
        index_3 = self.sequences_lengths.index(3)
        other_sequences_lengths = self.sequences_lengths[:index_3] + self.sequences_lengths[index_3 + 1:]
        if other_sequences_lengths[0] != other_sequences_lengths[1]:
            return None
        needed_length = other_sequences_lengths[0]
        special_token = self.color_to_token(index_3)
        indices_special_tokens = [i for i, token in enumerate(tokens) if token == special_token]
        tokens_string = ''.join(tokens)
        colors = list(range(self.n_colors))
        colors.pop(index_3)
        token1 = self.color_to_token(colors[0])
        token2 = self.color_to_token(colors[1])
        indices_sequences = [i for i in range(len(tokens)) if
                             tokens_string.startswith(token1 * (needed_length - 1), i) or
                             tokens_string.startswith(token2 * (needed_length - 1), i)]
        if len(indices_sequences) < 2:
            return None

        # patrzymy czy jest jakas podwojna sekwencja monochromatyczna bez odstepow, jak nie to nic nie mozemy zrobic
        distances_between_sequences = [a - b for a, b in zip(indices_sequences[1:], indices_sequences)]
        if needed_length - 1 not in distances_between_sequences:
            return None

        # jesli sa dwa tokeny koloru k_i=3 a pomiedzy nimi podwojna monochromatyczna sekwencja, to wybieramy srodek
        # gdy taki token jest jeden, a obok podwojna chromatyczna sekwencja, to stawiamy kolejny token z drugiej strony
        # (chodzi o sekwencje bez odstepow)
        for i, sequence_index in enumerate(indices_sequences[:-1]):
            if distances_between_sequences[i] != needed_length - 1:
                continue
            if sequence_index - 1 in indices_special_tokens and sequence_index + (
                    needed_length - 1) * 2 in indices_special_tokens:
                return sequence_index + needed_length - 1
            elif sequence_index - 1 in indices_special_tokens:
                return sequence_index + (needed_length - 1) * 2
            elif sequence_index + (needed_length - 1) * 2 in indices_special_tokens:
                return sequence_index

        # gdy nie ma zadnych tokenow koloru k_i-3, to patrzymy czy jest podwojna (lub lepiej jak potrojna) sekwencja
        # monochromatyczna bez odstepow
        first_double_sequence_index = None
        first_triple_sequence_index = None
        for sequence_index in indices_sequences:
            if sequence_index + needed_length - 1 in indices_sequences and first_double_sequence_index is None:
                first_double_sequence_index = sequence_index
            if sequence_index + needed_length - 1 in indices_sequences and sequence_index + (
                    needed_length - 1) * 2 in indices_sequences:
                first_triple_sequence_index = sequence_index
                break
        if first_triple_sequence_index is not None:
            return first_triple_sequence_index + needed_length - 1
        elif first_double_sequence_index is not None:
            return first_double_sequence_index

    def select_most_promising_position(self):
        best_position_index = max(self.closing_positions, key=lambda k: len(self.closing_positions[k]))
        best_number_of_closing_tokens = len(self.closing_positions[best_position_index])
        if best_number_of_closing_tokens == 0:
            return None
        best_positions = [k for k, v in self.closing_positions.items() if len(v) == best_number_of_closing_tokens]
        return best_positions[randint(0, len(best_positions) - 1)]
