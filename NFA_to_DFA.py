import json
from collections import deque
from NFA_testing import NFA_ex0, NFA_ex1, NFA_ex2, NFA_ex3

def epsilon_closure(states, transitions):
    """
    Computes the epsilon closure of a set of states in a given NFA.

    Parameters:
    states (iterable): The set of states for which epsilon closure needs to be computed.
    transitions (dict): The transition table of the NFA.

    Returns:
    tuple: The epsilon closure of the input states as a sorted tuple.
    """
    epsilon_closure_set = set(states)
    queue = deque(states)

    while queue:
        current_state = queue.popleft()

        if "ε" in transitions[current_state]:
            epsilon_closure_set.update(transitions[current_state]["ε"])

            for state in transitions[current_state]["ε"]:
                if state not in epsilon_closure_set:
                    queue.append(state)

    return tuple(sorted(list(epsilon_closure_set)))

def move(states, symbol, transitions):
        """
        Returns the set of states that can be reached from the given set of states
        using the specified symbol and transitions.

        Parameters:
        - states (tuple): The set of states to move from.
        - symbol (str): The symbol to use for the transition.
        - transitions (dict): The dictionary representing the transitions between states.

        Returns:
        - tuple: The set of states that can be reached from the given set of states
            using the specified symbol and transitions.
        """
        
        result = set()

        for state in states:
                if symbol in transitions[state]:
                        result.update(transitions[state][symbol])

        return tuple(sorted(list(result)))

def nfa_to_dfa(nfa):
    """
    Converts a given NFA (Non-Deterministic Finite Automaton) to a DFA (Deterministic Finite Automaton).

    Args:
        nfa (dict): The NFA represented as a dictionary with the following keys:
            - "states": List of states in the NFA.
            - "alphabet": List of symbols in the input alphabet.
            - "transitions": Dictionary representing the transition function of the NFA.
            - "start_state": The start state of the NFA.
            - "accept_states": List of accept states in the NFA.

    Returns:
        dict: The resulting DFA (Deterministic Finite Automaton) represented as a dictionary with the following keys:
            - "states": List of states in the DFA.
            - "alphabet": List of symbols in the input alphabet.
            - "transitions": Dictionary representing the transition function of the DFA.
            - "start_state": The start state of the DFA.
            - "accept_states": List of accept states in the DFA.
    """
    
    # Print the original NFA
    print("\nOriginal NFA:")
    print(json.dumps(nfa, indent=2))

    dfa_states = []
    dfa_transitions = {}
    start_state = epsilon_closure([nfa["start_state"]], nfa["transitions"])
    queue = deque([start_state])

    print("\nNFA to DFA Conversion Steps:")

    while queue:
        current_states = queue.popleft()

        if current_states not in dfa_states:
            dfa_states.append(current_states)

        # Print the current set of states being processed
        print("\nProcessing states:", current_states)

        for symbol in nfa["alphabet"]:
            next_states = epsilon_closure(move(current_states, symbol, nfa["transitions"]), nfa["transitions"])

            if next_states:
                current_states_str = str(current_states)
                next_states_str = str(next_states)

                if current_states_str not in dfa_transitions:
                    dfa_transitions[current_states_str] = {}

                # Print the transition being added to the DFA
                print(f"Adding transition: {current_states_str} --({symbol})--> {next_states_str}")

                dfa_transitions[current_states_str][symbol] = next_states_str

                if next_states not in dfa_states:
                    queue.append(next_states)

    dfa_accept_states = [state for state in dfa_states if any(s in nfa["accept_states"] for s in state)]

    # Print the resulting DFA
    print("\nResulting DFA:")
    dfa = {
        "states": dfa_states,
        "alphabet": nfa["alphabet"],
        "transitions": dfa_transitions,
        "start_state": start_state,
        "accept_states": dfa_accept_states
    }
    print(json.dumps(dfa, indent=2))

    return dfa


# Convert NFA to DFA
dfa_json = nfa_to_dfa(NFA_ex1)
