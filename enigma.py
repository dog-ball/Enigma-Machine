"""
This program simulates the enigma_machine machine using a Rotor and Reflector class that connect
to a RotorAssembly making up the Rotor portion of the machine and a PlugLead and PlugBoard class
that make up the Plug Board section of the machine. These are then brought together in the
Machine class which can encode through all the machines components.
"""

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class InputValueError(Exception):
    """The InputValueError class is a custom error class for handling invalid character inputs."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"'{self.value}' is an invalid input, inputs must be upper-case letters A-Z."


class InputLengthError(Exception):
    """The InputValueError class is a custom error class for handling invalid length inputs."""

    def __init__(self, value, length):
        self.value = value
        self.length = length

    def __str__(self):
        return f"'{self.value}' is an invalid input, inputs must be {self.length} characters long."


def verify_input(input, length=None):
    for i in input:
        if i not in ALPHABET:
            raise InputValueError(input)
    if length:
        if len(input) != length:
            raise InputLengthError(input, length)


class Mappings:
    """The Mappings class is a superclass containing mapping data for rotors and reflectors."""

    def __init__(self):
        self.rotor_mappings = {
            'Beta': {0: 11, 1: 4, 2: 24, 3: 9, 4: 21, 5: 2, 6: 13, 7: 8, 8: 23, 9: 22, 10: 15, 11: 1, 12: 16, 13: 12,
                     14: 3, 15: 17, 16: 19, 17: 0, 18: 10, 19: 25, 20: 6, 21: 5, 22: 20, 23: 7, 24: 14, 25: 18},
            'Gamma': {0: 5, 1: 18, 2: 14, 3: 10, 4: 0, 5: 13, 6: 20, 7: 4, 8: 17, 9: 7, 10: 12, 11: 1, 12: 19, 13: 8,
                      14: 24, 15: 2, 16: 22, 17: 11, 18: 16, 19: 15, 20: 25, 21: 23, 22: 21, 23: 6, 24: 9, 25: 3},
            'I': {0: 4, 1: 10, 2: 12, 3: 5, 4: 11, 5: 6, 6: 3, 7: 16, 8: 21, 9: 25, 10: 13, 11: 19, 12: 14, 13: 22,
                  14: 24, 15: 7, 16: 23, 17: 20, 18: 18, 19: 15, 20: 0, 21: 8, 22: 1, 23: 17, 24: 2, 25: 9},
            'II': {0: 0, 1: 9, 2: 3, 3: 10, 4: 18, 5: 8, 6: 17, 7: 20, 8: 23, 9: 1, 10: 11, 11: 7, 12: 22, 13: 19,
                   14: 12, 15: 2, 16: 16, 17: 6, 18: 25, 19: 13, 20: 15, 21: 24, 22: 5, 23: 21, 24: 14, 25: 4},
            'III': {0: 1, 1: 3, 2: 5, 3: 7, 4: 9, 5: 11, 6: 2, 7: 15, 8: 17, 9: 19, 10: 23, 11: 21, 12: 25, 13: 13,
                    14: 24, 15: 4, 16: 8, 17: 22, 18: 6, 19: 0, 20: 10, 21: 12, 22: 20, 23: 18, 24: 16, 25: 14},
            'IV': {0: 4, 1: 18, 2: 14, 3: 21, 4: 15, 5: 25, 6: 9, 7: 0, 8: 24, 9: 16, 10: 20, 11: 8, 12: 17, 13: 7,
                   14: 23, 15: 11, 16: 13, 17: 5, 18: 19, 19: 6, 20: 10, 21: 3, 22: 2, 23: 12, 24: 22, 25: 1},
            'V': {0: 21, 1: 25, 2: 1, 3: 17, 4: 6, 5: 8, 6: 19, 7: 24, 8: 20, 9: 15, 10: 18, 11: 3, 12: 13, 13: 7,
                  14: 11, 15: 23, 16: 0, 17: 22, 18: 12, 19: 9, 20: 16, 21: 14, 22: 5, 23: 4, 24: 2, 25: 10},
            # Additional Navy Rotors
            'VI': {0: 9, 1: 15, 2: 6, 3: 21, 4: 14, 5: 20, 6: 12, 7: 5, 8: 24, 9: 16, 10: 1, 11: 4, 12: 13, 13: 7,
                   14: 25, 15: 17, 16: 3, 17: 10, 18: 0, 19: 18, 20: 23, 21: 11, 22: 8, 23: 2, 24: 19, 25: 22},
            'VII': {0: 13, 1: 25, 2: 9, 3: 7, 4: 6, 5: 17, 6: 2, 7: 25, 8: 12, 9: 24, 10: 18, 11: 22, 12: 1, 13: 14,
                    14: 20, 15: 5, 16: 0, 17: 8, 18: 21, 19: 11, 20: 15, 21: 4, 22: 10, 23: 16, 24: 3, 25: 19},
            'VIII': {0: 5, 1: 10, 2: 16, 3: 7, 4: 19, 5: 11, 6: 23, 7: 14, 8: 2, 9: 1, 10: 9, 11: 18, 12: 15, 13: 3,
                     14: 25, 15: 17, 16: 0, 17: 12, 18: 4, 19: 22, 20: 13, 21: 8, 22: 20, 23: 24, 24: 6, 25: 21}}

        self.reflector_mappings = {
            'A': {0: 4, 1: 9, 2: 12, 3: 25, 4: 0, 5: 11, 6: 24, 7: 23, 8: 21, 9: 1, 10: 22, 11: 5, 12: 2, 13: 17,
                  14: 16, 15: 20, 16: 14, 17: 13, 18: 19, 19: 18, 20: 15, 21: 8, 22: 10, 23: 7, 24: 6, 25: 3},
            'B': {0: 24, 1: 17, 2: 20, 3: 7, 4: 16, 5: 18, 6: 11, 7: 3, 8: 15, 9: 23, 10: 13, 11: 6, 12: 14, 13: 10,
                  14: 12, 15: 8, 16: 4, 17: 1, 18: 5, 19: 25, 20: 2, 21: 22, 22: 21, 23: 9, 24: 0, 25: 19},
            'C': {0: 5, 1: 21, 2: 15, 3: 9, 4: 8, 5: 0, 6: 14, 7: 24, 8: 4, 9: 3, 10: 17, 11: 25, 12: 23, 13: 22,
                  14: 6, 15: 2, 16: 19, 17: 10, 18: 20, 19: 16, 20: 18, 21: 1, 22: 13, 23: 12, 24: 7, 25: 11}}

        self.notches = {'I': 16, 'II': 4, 'III': 21, 'IV': 9, 'V': 25, 'Beta': None, 'Gamma': None, 'VI': (25, 12),
                        'VII': (25, 12), 'VIII': (25, 12)}


class Rotor(Mappings):
    """The Rotor class initialises the particular rotor mechanism to be instantiated and,
    using the mappings inherited from the Mappings superclass, provides functionality
    for encoding from right to left and left to right."""

    def __init__(self, label='Beta', initial_position='A', ring_setting=1):
        # Data from the Mappings superclass is used to initialise Rotor instantiations.
        super().__init__()
        self.initial_position = initial_position
        self.mapping = self.rotor_mappings[label]
        self.window_position = ALPHABET.index(initial_position)
        self.notch = self.notches[label]
        self.ring_setting = ring_setting
        self.offset = ring_setting - 1
        self.label = label

    def __str__(self):
        return f'Rotor: {self.label} | Window position: {ALPHABET[self.window_position]} | ' \
               f'Ring setting: {self.ring_setting}'

    def encode_right_to_left(self, char_index):
        if type(char_index) is int:
            return self.mapping[(char_index + self.window_position - self.offset) % 26]
        else:
            verify_input(char_index, length=1)
            return ALPHABET[self.mapping[ALPHABET.index(char_index)]]

    def encode_left_to_right(self, char_index):
        reversed_mapping = {y: x for x, y in self.mapping.items()}
        if type(char_index) is int:
            return reversed_mapping[(char_index + self.window_position - self.offset) % 26]
        else:
            verify_input(char_index, length=1)
            return ALPHABET[reversed_mapping[ALPHABET.index(char_index)]]

    def step_check(self):
        if self.label in {'I', 'II', 'III', 'IV', 'V', 'Beta', 'Gamma'}:
            return self.window_position == self.notch
        elif self.label in {'VI', 'VII', 'VII'}:
            return self.window_position == self.notch[0] or self.notch[1]

    def apply_step(self):
        self.window_position = (self.window_position + 1) % 26

    def apply_offset(self, char_index):
        return char_index - self.window_position + self.offset

    def update_window_position(self, new_position=None):
        if new_position:
            self.window_position = ALPHABET.index(new_position)
        else:
            self.window_position = ALPHABET.index(self.initial_position)


class Reflector(Mappings):
    """The Reflector class initialises the particular reflector mechanism to be instantiated and,
    using the mappings inherited from the Mappings superclass, provides encoding functionality."""

    def __init__(self, label='A'):
        # Data from the Mappings superclass is used to initialise Reflector instantiations.
        super().__init__()
        self.mapping = self.reflector_mappings[label]
        self.label = label

    def __str__(self):
        return f'Reflector: {self.label}'

    def encode(self, char_index):
        if type(char_index) is int:
            return self.mapping[char_index % 26]
        else:
            verify_input(char_index, length=1)
            return ALPHABET[self.mapping[ALPHABET.index(char_index)]]

    def change_mapping(self, new_label):
        self.mapping = self.reflector_mappings[new_label]
        self.label = new_label


class RotorAssembly:
    """The RotorAssembly class acts as the part of the enigma machine which aggregates the three/four rotors
    and reflector."""

    def __init__(self, reflector, first_rotor, second_rotor, third_rotor, fourth_rotor=None):
        # The naming of the rotors corresponds with their position in the enigma machine from right to left.
        self.reflector = reflector
        self.first_rotor = first_rotor
        self.second_rotor = second_rotor
        self.third_rotor = third_rotor
        self.fourth_rotor = fourth_rotor
        self.rotors = [self.first_rotor, self.second_rotor, self.third_rotor, self.fourth_rotor]

    def __str__(self):
        string = f'Active Rotors (numbered from right to left):\n' \
                 f'{str(self.first_rotor)}\n{str(self.second_rotor)}\n{str(self.third_rotor)}\n'
        if self.fourth_rotor:
            return string + f'{str(self.fourth_rotor)}\n'
        return string

    def step(self):
        # Checks which rotors require turnover and then rotates and updates their window positions.
        if self.second_rotor.step_check():
            self.second_rotor.apply_step()
            self.third_rotor.apply_step()
        elif self.first_rotor.step_check():
            self.second_rotor.apply_step()
        self.first_rotor.apply_step()

    def encode(self, char):
        # Passes the input character through each encode function of each element of the Rotor Assembly.
        verify_input(char, length=1)
        self.step()
        char_index = ALPHABET.index(char)
        char_index = self.first_rotor.encode_right_to_left(char_index)
        char_index = self.second_rotor.encode_right_to_left(
            self.first_rotor.apply_offset(char_index))
        char_index = self.third_rotor.encode_right_to_left(
            self.second_rotor.apply_offset(char_index))
        if self.fourth_rotor is not None:
            char_index = self.fourth_rotor.encode_right_to_left(
                self.third_rotor.apply_offset(char_index))
            char_index = self.reflector.encode(
                self.fourth_rotor.apply_offset(char_index))
            char_index = self.fourth_rotor.encode_left_to_right(char_index)
            char_index = self.third_rotor.encode_left_to_right(
                self.fourth_rotor.apply_offset(char_index))
        else:
            char_index = self.reflector.encode(self.third_rotor.apply_offset(char_index))
            char_index = self.third_rotor.encode_left_to_right(char_index)
        char_index = self.second_rotor.encode_left_to_right(
            self.third_rotor.apply_offset(char_index))
        char_index = self.first_rotor.encode_left_to_right(
            self.second_rotor.apply_offset(char_index))
        return ALPHABET[(self.first_rotor.apply_offset(char_index)) % 26]


class PlugLead:
    """This class sets up the data and functionality for each individual plug lead"""

    def __init__(self, mapping):
        # Check if plug connects two distinct valid characters
        verify_input(mapping, length=2)
        if mapping[0] == mapping[1]:
            raise ValueError('It is not possible to connect a letter to itself.')
        else:
            self.mapping = mapping

    def __str__(self):
        return f'Pluglead: {self.mapping}'

    def encode(self, char):
        verify_input(char, length=1)
        if char == self.mapping[0]:
            return self.mapping[1]
        elif char == self.mapping[1]:
            return self.mapping[0]
        else:
            return char


class Plugboard:
    """The PlugBoard class combines the encoding functionality of multiple PlugLeads once they have been
    instantiated."""

    def __init__(self):
        self.plug_count = 0
        self.connected_plugs = []
        self.available_chars = {x: x for x in ALPHABET}
        self.standard_board = True

    def __str__(self):
        if self.connected_plugs:
            output = [str(plug) for plug in self.connected_plugs]
            return f'Connected plugs:\n{str(output)}'
        else:
            return 'No plug leads connected.'

    def add(self, *leads):
        for plug_lead in leads:
            # Check if maximum plug count is surpassed
            if self.standard_board is True and self.plug_count >= 10:
                print('Maximum plug count met (10/10)')
                response = input('Increase maximum plug count? (y/n): ')
                if response == 'y':
                    self.standard_board = False
                    print('Maximum plug count increased + 3')
                else:
                    break
            self.connected_plugs.append(plug_lead.mapping)
            self.plug_count += 1
            self.available_chars[plug_lead.mapping[0]] = plug_lead.mapping[1]
            self.available_chars[plug_lead.mapping[1]] = plug_lead.mapping[0]

    def encode(self, char):
        verify_input(char, length=1)
        for key, value in self.available_chars.items():
            if char == key:
                return value


class Machine:
    """This class combines the encoding functionality of the RotorAssembly and the PlugBoard."""

    def __init__(self, rotor_assembly, plug_board):
        self.rotor_assembly = rotor_assembly
        self.plug_board = plug_board

    def __str__(self):
        return f'\n{str(self.rotor_assembly)}\n{str(self.plug_board)}'

    def encode_char(self, char):
        # The final encoding function which goes through all elements of the machine
        verify_input(char, length=1)
        output = self.plug_board.encode(char)
        output = self.rotor_assembly.encode(output)
        output = self.plug_board.encode(output)
        return output

    def encode_phrase(self, phrase):
        output = ''
        for char in phrase:
            verify_input(char, length=1)
            output += self.encode_char(char)
        return output
