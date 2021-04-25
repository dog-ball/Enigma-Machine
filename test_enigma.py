from enigma import *
from code_breaking import *


def test_pluglead():
    lead = PlugLead("AG")
    assert (lead.encode("A") == "G")
    assert (lead.encode("D") == "D")


def test_plugboard():
    plugboard = Plugboard()
    plugboard.add(PlugLead("SZ"))
    plugboard.add(PlugLead("GT"))
    plugboard.add(PlugLead("DV"))
    plugboard.add(PlugLead("KU"))
    assert (plugboard.encode("K") == "U")
    assert (plugboard.encode("A") == "A")


def test_primary_rotors():
    beta_rotor = Rotor("Beta")
    assert (beta_rotor.encode_right_to_left("A") == "L")
    assert (beta_rotor.encode_left_to_right("A") == "R")
    gamma_rotor = Rotor("Gamma")
    assert (gamma_rotor.encode_right_to_left("A") == "F")
    assert (gamma_rotor.encode_left_to_right("A") == "E")
    i_rotor = Rotor("I")
    assert (i_rotor.encode_right_to_left("A") == "E")
    assert (i_rotor.encode_left_to_right("A") == "U")
    ii_rotor = Rotor("II")
    assert (ii_rotor.encode_right_to_left("A") == "A")
    assert (ii_rotor.encode_left_to_right("A") == "A")
    iii_rotor = Rotor("III")
    assert (iii_rotor.encode_right_to_left("A") == "B")
    assert (iii_rotor.encode_left_to_right("A") == "T")
    iv_rotor = Rotor("IV")
    assert (iv_rotor.encode_right_to_left("A") == "E")
    assert (iv_rotor.encode_left_to_right("A") == "H")
    v_rotor = Rotor("V")
    assert (v_rotor.encode_right_to_left("A") == "V")
    assert (v_rotor.encode_left_to_right("A") == "Q")


def test_reflectors():
    a_reflector = Reflector('A')
    assert (a_reflector.encode("A") == "E")
    b_reflector = Reflector('B')
    assert (b_reflector.encode("A") == "Y")
    c_reflector = Reflector('C')
    assert (c_reflector.encode("A") == "F")


def test_additional_rotors():
    vi_rotor = Rotor("VI")
    assert (vi_rotor.encode_right_to_left("A") == "J")
    assert (vi_rotor.encode_left_to_right("A") == "S")
    vii_rotor = Rotor("VII")
    assert (vii_rotor.encode_right_to_left("A") == "N")
    assert (vii_rotor.encode_left_to_right("A") == "Q")
    viii_rotor = Rotor("VIII")
    assert (viii_rotor.encode_right_to_left("A") == "F")
    assert (viii_rotor.encode_left_to_right("A") == "Q")


def test_3_rotor_assembly_encode():
    rotor3 = Rotor('I', initial_position='A', ring_setting=1)
    rotor2 = Rotor('II', initial_position='A', ring_setting=1)
    rotor1 = Rotor('III', initial_position='A', ring_setting=1)
    reflector = Reflector('B')
    rotor_assembly = RotorAssembly(reflector, rotor1, rotor2, rotor3)
    assert (rotor_assembly.encode('A') == 'B')


def test_4_rotor_assembly_encode():
    rotor4 = Rotor('I', initial_position='Q', ring_setting=7)
    rotor3 = Rotor('II', initial_position='E', ring_setting=11)
    rotor2 = Rotor('III', initial_position='V', ring_setting=15)
    rotor1 = Rotor('IV', initial_position='Z', ring_setting=19)
    reflector = Reflector('C')
    assembly = RotorAssembly(reflector, rotor1, rotor2, rotor3, rotor4)
    assert (assembly.encode("Z") == "V")


def test_machine_encode():
    rotor3 = Rotor('I', initial_position='A', ring_setting=1)
    rotor2 = Rotor('II', initial_position='A', ring_setting=1)
    rotor1 = Rotor('III', initial_position='A', ring_setting=1)
    reflector = Reflector('B')
    plug_board = Plugboard()
    rotor_assembly = RotorAssembly(reflector, rotor1, rotor2, rotor3)
    enigma_machine = Machine(rotor_assembly, plug_board)
    assert enigma_machine.encode_phrase('FYGDHWNLDTBM') == 'EMILMARGRAIN'


def advanced_machine_encode():
    rotor4 = Rotor('IV', initial_position='E', ring_setting=18)
    rotor3 = Rotor('V', initial_position='Z', ring_setting=24)
    rotor2 = Rotor('Beta', initial_position='G', ring_setting=3)
    rotor1 = Rotor('I', initial_position='P', ring_setting=5)
    reflector = Reflector('A')
    assembly = RotorAssembly(reflector, rotor1, rotor2, rotor3, rotor4)
    plug_board = Plugboard()
    plug_board.add(PlugLead('PC'), PlugLead('XZ'), PlugLead('FM'), PlugLead('QA'), PlugLead('ST'),
                   PlugLead('NB'), PlugLead('HY'), PlugLead('OR'), PlugLead('EV'), PlugLead('IU'))
    enigma_machine = Machine(assembly, plug_board)
    assert (enigma_machine.encode_phrase("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI") ==
            "CONGRATULATIONSONPRODUCINGYOURWORKINGENIGMAMACHINESIMULATOR")


def test_code_breaking():
    reflectors = ['A', 'B', 'C']
    for reflector in reflectors:
        print(f'reflector = {reflector}')
        crib = 'SECRETS'
        text = 'DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ'
        rotor3 = Rotor('Beta', initial_position='M', ring_setting=4)
        rotor2 = Rotor('Gamma', initial_position='J', ring_setting=2)
        rotor1 = Rotor('V', initial_position='M', ring_setting=14)
        plug_board = Plugboard()
        plug_board.add(PlugLead('KI'), PlugLead('XN'), PlugLead('FL'))
        reflector = Reflector(reflector)
        rotor_assembly = RotorAssembly(reflector, rotor1, rotor2, rotor3)
        enigma_machine = CodeBreak(rotor_assembly, plug_board)
        out = enigma_machine.encode_phrase(text)
        if crib in out:
            break
    assert out == 'NICEWORKYOUVEMANAGEDTODECODETHEFIRSTSECRETSTRING'