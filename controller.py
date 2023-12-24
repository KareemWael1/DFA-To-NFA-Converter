import NFA_to_DFA


def process_input(states, sigma, transitions, start_state, final_states):
    nfa = {"states": states.strip('{}').split(', '),
           "alphabet": sigma.strip('{}').split(', '),
           "transitions": extract_transitions(transitions),
           "start_state": start_state,
           "accept_states": final_states.strip('{}').split(', ')}
    print(nfa)
    dfa = NFA_to_DFA.nfa_to_dfa(nfa)
    dfa = process_output(dfa)
    print(dfa)
    nfa_graph = get_graph(nfa)
    dfa_graph = get_graph(dfa)
    print(nfa_graph)
    print(dfa_graph)
    return nfa_graph[0], nfa_graph[1], dfa_graph[0], dfa_graph[1]


def get_graph(automaton):
    transitions = automaton['transitions']

    # Collect all transitions with their symbols
    all_transitions = []
    for from_state, symbols in transitions.items():
        for symbol, to_states in symbols.items():
            if type(to_states) is str:
                all_transitions.append(((from_state, to_states), symbol))
            else:
                for to_state in to_states:
                    all_transitions.append(((from_state, to_state), symbol))

    # Remove duplicates
    unique_transitions = []
    seen = set()
    for transition, symbol in all_transitions:
        if (transition, symbol) not in seen:
            unique_transitions.append([(transition[0], transition[1]), symbol])
            seen.add((transition, symbol))

    # Merge transitions with the same start and end states
    merged_transitions = {}
    for transition, symbol in unique_transitions:
        if transition in merged_transitions:
            merged_transitions[transition].append(symbol)
        else:
            merged_transitions[transition] = [symbol]

    # Format the final output
    final_output = [[transition, ','.join(symbols)] for transition, symbols in merged_transitions.items()]

    # Determine states type
    states = {}
    for state in automaton["states"]:
        value = 0
        if state in automaton["accept_states"]:
            value += 1
        if state == automaton["start_state"]:
            value += 2
        states[state] = value

    return final_output, states


def extract_transitions(transition_lines):
    transition_lines = transition_lines.strip().split('\n')

    result = {}
    for line in transition_lines:
        state_symbol, transitions = line.split(' = ')
        state, symbol = state_symbol.strip('()').split(', ')
        transitions = transitions.strip('{}')

        if state not in result:
            result[state] = {}

        result[state][symbol] = transitions.split(', ')

    return result


def process_output(dfa):
    # Convert states, start_state, and accept_states
    states = [str(state).replace("'", "") for state in dfa['states']]
    start_state = str(dfa['start_state']).replace("'", "")
    accept_states = [str(state).replace("'", "") for state in dfa['accept_states']]

    # Convert transitions
    transitions = {}
    for key, value in dfa['transitions'].items():
        new_key = str(key).replace("'", "")
        transitions[new_key] = {k: str(v).replace("'", "") for k, v in value.items()}

    # Create the converted dictionary
    output = {
        'states': states,
        'alphabet': dfa['alphabet'],
        'transitions': transitions,
        'start_state': start_state,
        'accept_states': accept_states
    }

    return output