from time import sleep


class Strategy:
    def __init__(self, n_colors, sequences_lengths, computer_delay_seconds=0, press_key_before_computer_moves=False):
        self.n_colors = n_colors
        self.sequences_lengths = sequences_lengths.copy()
        self.computer_delay_seconds = computer_delay_seconds
        self.press_key_before_computer_moves = press_key_before_computer_moves
        super().__init__()

    def wait_before_move(self):
        if self.computer_delay_seconds < 0.01:
            return
        for i in range(5):
            sleep(self.computer_delay_seconds / 5)
            if i != 0 and i != 4:
                print('.', sep=' ', end='', flush=True)
            if i == 4:
                print('\n')

    def find_best_sequences(self, tokens):
        checked_gaps = [set() for i in range(len(tokens))]
        best_sequences_info = {
            chr(ord('A') + i if i < 26 else ord('a') + i - 26): {'best_sequence_length': 0, 'sequences_indices': []} for
            i in range(self.n_colors)}

        for i, current_token in enumerate(tokens):
            if best_sequences_info[current_token]['best_sequence_length'] == 0:
                best_sequences_info[current_token]['best_sequence_length'] = 1
                best_sequences_info[current_token]['sequences_indices'].append([i])
            for j, following_token in enumerate(tokens[i + 1:]):
                current_longest_sequence_counter = 1
                current_longest_sequence_indices = [i]
                index = i + j + 1
                gap = index - i
                if current_token != following_token or gap in checked_gaps[index]:
                    continue
                current_longest_sequence_counter += 1
                current_longest_sequence_indices.append(index)
                checked_gaps[index].add(gap)
                for k, token_in_sequence in enumerate(tokens[index + gap::gap]):
                    current_index = index + gap + k * gap
                    if gap in checked_gaps[current_index]:
                        break
                    if token_in_sequence != current_token:
                        break
                    else:
                        current_longest_sequence_counter += 1
                        current_longest_sequence_indices.append(current_index)
                        checked_gaps[current_index].add(gap)
                if current_longest_sequence_counter == best_sequences_info[current_token]['best_sequence_length']:
                    best_sequences_info[current_token]['sequences_indices'].append(current_longest_sequence_indices)
                elif current_longest_sequence_counter > best_sequences_info[current_token]['best_sequence_length']:
                    best_sequences_info[current_token]['best_sequence_length'] = current_longest_sequence_counter
                    best_sequences_info[current_token]['sequences_indices'].clear()
                    best_sequences_info[current_token]['sequences_indices'].append(current_longest_sequence_indices)

        return best_sequences_info

    def find_all_closing_positions_of_sequences(self, tokens, best_sequences_info):
        closing_positions = {i: set() for i in range(len(tokens) + 1)}
        for token, info in best_sequences_info.items():
            winning_length = self.sequences_lengths[
                ord(token) - ord('A') if self.n_colors < 26 else ord(token) - ord('a') + 26]
            if info['best_sequence_length'] != winning_length - 1:
                continue
            for sequence in info['sequences_indices']:
                gap = sequence[1] - sequence[0]
                if sequence[0] - gap + 1 >= 0:
                    closing_positions[sequence[0] - gap + 1].add(token)
                if sequence[-1] + gap <= len(tokens):
                    closing_positions[sequence[-1] + gap].add(token)
                if gap == 1:
                    for position in sequence[1:]:
                        closing_positions[position].add(token)
        return closing_positions

    def find_winning_position(self, closing_positions):
        for position, winning_tokens in closing_positions.items():
            if len(winning_tokens) == self.n_colors:
                return position

    def check_for_winning_sequence(self, best_sequences):
        for token, info in best_sequences.items():
            winning_length = self.sequences_lengths[
                ord(token) - ord('A') if self.n_colors < 26 else ord(token) - ord('a') + 26]
            if info["best_sequence_length"] >= winning_length:
                return info["sequences_indices"][0]

    @staticmethod
    def color_to_token(color):
        if color <= 25:
            return chr(ord('A') + color)
        else:
            return chr(ord('a') + color - 26)

    @staticmethod
    def token_to_color(token):
        if ord(token) <= ord('Z'):
            return ord(token) - ord('A')
        else:
            return ord(token) - ord('a') + 26
