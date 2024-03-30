from strategy_color import StrategyColor


class StrategyColorIntelligent(StrategyColor):
    def __init__(self, n_colors, sequences_lengths, computer_delay_seconds=0, press_key_before_computer_moves=False):
        super().__init__(n_colors, sequences_lengths, computer_delay_seconds, press_key_before_computer_moves)

    def _select_token(self, tokens, position):
        if self.n_colors == 1:
            return self.color_to_token(0)

        best_sequences = self.find_best_sequences(tokens)
        prioritized_token_list = []

        for token, info in best_sequences.items():
            winning_length_index = ord(token) - ord('A') if self.n_colors < 26 else ord(token) - ord('a') + 26
            winning_length = self.sequences_lengths[winning_length_index]
            prioritized_token_list.append((token, winning_length - info['best_sequence_length']))
        prioritized_token_list.sort(key=lambda x: (-x[1], x[0]))

        colors_losing = [False] * self.n_colors

        for i, entry in enumerate(prioritized_token_list):
            token, priority = entry
            tokens_to_check = tokens.copy()
            tokens_to_check.insert(position, token)
            best_sequences_with_potential_token = self.find_best_sequences(tokens_to_check)
            winning_sequence = self.check_for_winning_sequence(best_sequences_with_potential_token)
            if winning_sequence:
                colors_losing[i] = True
                continue
            closing_positions = self.find_all_closing_positions_of_sequences(tokens_to_check,
                                                                             best_sequences_with_potential_token)
            winning_position = self.find_winning_position(closing_positions)
            if winning_position:
                continue
            return token

        if False not in colors_losing:
            return self.color_to_token(0)

        for i, is_loss in enumerate(colors_losing):
            if is_loss:
                continue
            return prioritized_token_list[i][0]
