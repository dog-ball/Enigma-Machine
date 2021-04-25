# Enigma-Machine
A simulation of a WWII Enigma machine using Python. 
This code was submitted as a project for a programming module of my MSc in Artifical Intelligence at the University of Bath and it recieved 84/100. 

Alongside the simulation of the functionality of the machine found in enigma.py and some examples of code_breaking techniques in code_breaking.py I have also provided some additional work around error handling, security and testing the simulation outlined below:


## Additional work
### Error Handling

This can be found in my enigma.py file.

I have added my own custom exception classes for dealing with invalid inputs. My InputValueError class allows The code to handle invalid letters and numbers. The code will fail and provide a custom error message if the user enters an invalid character (e.g., Japanese letter, an arabic number or a floating point number) and then let the user know which values are accepted. My InputLengthError class allows the code to handle input of the wrong length. For example, if a user tries to input a string of length 5 when only a single character is expected, the class provides the user with a custom error message which lets them known that their input was invalid and the length of a valid input. Both of these classes are used often within the classes of my enigma.py file, from the initialisation of plug leads to the encoding function of the rotor_assembly.

### Security

This can be found in my enigma.py file.

When writing my program, I have tried to keep security at the forefront of my mind. I originally stored the rotor and reflector mappings on a CSV file which I imported into enigma.py but I then read about how CSV files can be used to make malicious attacks so I decided to store the mappings data in a class within the .py file instead since the crpytographic nature of the enimga machine makes it an obvious target for malicious attacks.

### Pytest

This can be found in my test_enigma.py file.

While programming my enigma machine, I wanted to include rigorous testing to make sure that any changes that I had to make at a later stage would not affecting the overall functioning of the machine. I spend some time researching different python testing workflows before deciding the on popular pytest framework. In my test_enigma.py file included with my submission, I have written 9 tests that ensure the correct functioning of my engima machine. To do this, I started by including some of the tests used in this jupyter notebook, rewriting them to function within the pytest framework, and then included some of my own which test my further work and code_breaking code. The tests can be run by inputting pytest into the terminal.


### Additional Navel Rotors

This can be found in my enigma.py file.

I've added the additional navel rotors and their unusual double notches into my Mappings class. I have demonstrated their individual functionality in the Single Rotor Demonstration. Since the navel rotors have two notches rather than one, I have also had to make an adjustment to my step_check rotor function.
