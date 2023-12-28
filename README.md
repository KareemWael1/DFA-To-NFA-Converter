# NFA to DFA Converter
This tool is an NFA (Nondeterministic Finite Automaton) to DFA (Deterministic Finite Automaton) converter implemented in Python using Tkinter.

## Description
The NFA to DFA converter is a graphical application that allows users to convert any given NFA into an equivalent DFA. It takes an NFA as input and generates a corresponding DFA that accepts the same language.

## Features
- Graphical user interface (GUI) built with Tkinter for ease of use. 
- Converts any NFA provided as input into an equivalent DFA.
- Displays the resulting DFA in a clear and understandable format.
- Written in Python for cross-platform compatibility.
## Usage
- Input NFA: Enter the NFA formal description into the application.
- Convert: Click on the 'Save Input' button to initiate the conversion process.
- View DFA: Once the conversion is complete, the resulting NFA and DFA as well as the DFA formal description will be displayed.
## Implementation Details
- Implemented in Python 3.x using Tkinter for the graphical interface.
- The application takes NFA transitions and states as input and employs an algorithm to convert it to an equivalent DFA.
- Utilizes algorithms such as subset construction to convert the NFA to DFA.
## Usage Instructions
To run the code:
- Ensure Python 3.x is installed.
- Run the application using the command: python nfa_to_dfa.py.
To run the executable file:
- under this project folder double-click on dist/nfa_to_dfa/nfa_to_dfa.exe and enjoy!
## Accepted Language
The converter accepts languages defined by the input NFA and generates an equivalent DFA that accepts the same language.