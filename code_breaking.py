from enigma import *
import itertools


def find_crib(crib, phrase):
    if crib in phrase:
        return True


def product(values, length=3):
    combs = itertools.product(values, repeat=length)
    return [i for i in combs]


def all_unique_perms(unique_values, length=3):
    combs = itertools.permutations(unique_values, length)
    return [i for i in combs]


def all_possible_combs(available_settings, length):
    combs = itertools.combinations(available_settings, length)
    return [i for i in combs]


class CodeBreak(Machine):
    def __init__(self, rotor_assembly, plug_board):
        super().__init__(rotor_assembly, plug_board)

    def reset_rotors(self, positions=None):
        # Reset rotors to new positions
        if positions:
            self.rotor_assembly.third_rotor.update_window_position(ALPHABET[positions[0]])
            self.rotor_assembly.second_rotor.update_window_position(ALPHABET[positions[1]])
            self.rotor_assembly.first_rotor.update_window_position(ALPHABET[positions[2]])
            if self.rotor_assembly.fourth_rotor:
                self.rotor_assembly.fourth_rotor.update_window_position(positions[3])
        # Return rotors to their default window positions
        else:
            self.rotor_assembly.first_rotor.update_window_position()
            self.rotor_assembly.second_rotor.update_window_position()
            self.rotor_assembly.third_rotor.update_window_position()
            if self.rotor_assembly.fourth_rotor:
                self.rotor_assembly.fourth_rotor.update_window_position()

    def without_reflector(self, code, crib):
        for reflector in ('A', 'B', 'C'):
            self.reset_rotors()
            self.rotor_assembly.reflector.change_mapping(reflector)
            out = self.encode_phrase(code)
            if find_crib(crib, out):
                return f'CODE: {out}\nREFLECTOR: {reflector}'

    def without_rotor_starting_positions(self, code, crib):
        stating_positions = product([i for i in range(26)])
        for positions in stating_positions:
            self.reset_rotors(positions)
            out = self.encode_phrase(code)
            if find_crib(crib, out):
                return f'CODE: {out}\nROTOR POSITIONS: {ALPHABET[positions[0]]}, {ALPHABET[positions[1]]}, ' \
                       f'{ALPHABET[positions[2]]}'


if __name__ == "__main__":
    # CODE 1:
    code = 'DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ'
    crib = 'SECRETS'
    rotor3 = Rotor('Beta', initial_position='M', ring_setting=4)
    rotor2 = Rotor('Gamma', initial_position='J', ring_setting=2)
    rotor1 = Rotor('V', initial_position='M', ring_setting=14)
    dummy_reflector = Reflector()
    rotor_assembly = RotorAssembly(dummy_reflector, rotor1, rotor2, rotor3)
    plug_board = Plugboard()
    plug_board.add(PlugLead('KI'), PlugLead('XN'), PlugLead('FL'))
    code_break = CodeBreak(rotor_assembly, plug_board)
    print(code_break.without_reflector(code, crib))

    # CODE 2:
    code = 'CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH'
    crib = 'UNIVERSITY'
    rotor3 = Rotor('Beta', ring_setting=23)
    rotor2 = Rotor('I', ring_setting=2)
    rotor1 = Rotor('III', ring_setting=10)
    reflector = Reflector('B')
    rotor_assembly = RotorAssembly(reflector, rotor1, rotor2, rotor3)
    plug_board = Plugboard()
    plug_board.add(PlugLead('VH'), PlugLead('PT'), PlugLead('ZG'),
                   PlugLead('BJ'), PlugLead('EY'), PlugLead('FS'))
    code_break = CodeBreak(rotor_assembly, plug_board)
    print(code_break.without_rotor_starting_positions(code, crib))

    # CODE 3:
    code = 'ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY'
    crib = 'THOUSANDS'
    reflectors = ('A', 'B', 'C')
    possible_rotors = ('II', 'IV', 'Beta', 'Gamma')
    possible_ring_settings = (2, 4, 6, 8, 20, 22, 24)
    for current_reflector in reflectors:
        for rotor_comb in all_unique_perms(possible_rotors):
            for ring_settings_comb in product(possible_ring_settings):
                rotor3 = Rotor(rotor_comb[0], 'E', ring_settings_comb[0])
                rotor2 = Rotor(rotor_comb[1], 'M', ring_settings_comb[1])
                rotor1 = Rotor(rotor_comb[2], 'Y', ring_settings_comb[2])
                plug_board = Plugboard()
                plug_board.add(PlugLead('FH'), PlugLead('TS'), PlugLead('BE'), PlugLead('UQ'), PlugLead('KD'),
                               PlugLead('AL'))
                reflector = Reflector(current_reflector)
                rotor_assembly = RotorAssembly(reflector, rotor1, rotor2, rotor3)
                code_break = CodeBreak(rotor_assembly, plug_board)
                out = code_break.encode_phrase(code)
                if find_crib(crib, out):
                    print(f'CODE: {out}\nREFLECTOR: {reflector}\nROTORS: {rotor3.label} {rotor2.label} {rotor1.label}\n'
                          f'RING SETTINGS: {rotor3.ring_setting} {rotor2.ring_setting} {rotor1.ring_setting}')

    # CODE 4:
    code = 'SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW'
    crib = 'TUTOR'
    available_chars = {'D', 'E', 'K', 'L', 'M', 'O', 'Q', 'T', 'U', 'X', 'Y', 'Z'}
    for char_comb in all_unique_perms(available_chars, 2):
        rotor3 = Rotor('V', 'S', 24)
        rotor2 = Rotor('III', 'W', 12)
        rotor1 = Rotor('IV', 'U', 10)
        reflector = Reflector('A')
        rotor_assembly = RotorAssembly(reflector, rotor1, rotor2, rotor3)
        plug_board = Plugboard()
        plug_board.add(PlugLead('WP'), PlugLead('RJ'), PlugLead('VF'), PlugLead('HN'), PlugLead('CG'), PlugLead('BS'),
                       PlugLead('A' + char_comb[0]), PlugLead('I' + char_comb[1]))
        code_break = CodeBreak(rotor_assembly, plug_board)
        out = code_break.encode_phrase(code)
        if find_crib(crib, out):
           print(f'CODE: {out}\n{code_break.plug_board}\n')

    # CODE 5:
    reflector = Reflector('B')
    pairs = []
    used_pairs = []
    for x, y in reflector.mapping.items():
        if y not in pairs:
            pairs.append(x)
            pairs.append(y)
            used_pairs.append([x, y])
            used_pairs.append([y, x])

    paired = []
    count = 0
    for i in range(13):
        paired.append(pairs[count:count + 2])
        count += 2
    # This gets us all the possible combinations of four wires
    for group in all_possible_combs(paired, 4):
        numbers = []
        for pair in group:
            for num in pair:
                numbers.append(num)
        # This gets us all the possible rewirings
        combs = all_possible_perms(numbers, 8)
        usable_combs = []
        for comb in combs:
            reflector = Reflector('B')
            bad_comb = False
            split_comb = []
            count = 0
            for i in range(4):
                split_comb.append([comb[count], comb[count + 1]])
                count += 2
            # Check to see all the wires have been changed
            for pair in split_comb:
                if pair in used_pairs:
                    bad_comb = True
            if bad_comb is False:
                usable_combs.append(comb)
                new_mapping = reflector.mapping.copy()
                for pair in split_comb:
                    new_mapping[pair[0]] = pair[1]
                    new_mapping[pair[1]] = pair[0]
                reflector.mapping = new_mapping
                out = ''
                rotor3 = Rotor('V', 'A', 6)
                rotor2 = Rotor('II', 'J', 18)
                rotor1 = Rotor('IV', 'L', 7)
                plug_board = PlugBoard()
                plug_board.add(PlugLead('UG'), PlugLead('IE'), PlugLead('PO'), PlugLead('NX'), PlugLead('WT'))
                rotor_assembly = RotorAssembly(reflector, rotor1, rotor2, rotor3)
                enigma_machine = Machine(rotor_assembly, plug_board)
                for i in code:
                    out += enigma_machine.encode(i)
                for crib in possible_cribs:
                    if crib in out:
                        print(out)
                        print(reflector.mapping)

