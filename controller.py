import NFA_to_DFA


def process_input(states, sigma, transitions, start_state, final_states):
    nfa = {"states": states.strip('{}').split(', '),
           "alphabet": sigma.strip('{}').split(', '),
           "transitions": extract_transitions(transitions),
           "start_state": start_state,
           "accept_states": final_states.strip('{}').split(', ')}
    dfa = NFA_to_DFA.nfa_to_dfa(nfa)
    print(dfa)
    nfa_graph = get_graph(nfa)
    dfa_graph = get_graph(dfa)
    print(dfa_graph)
    return nfa_graph[0], nfa_graph[1], dfa_graph[0], dfa_graph[1]


def get_graph(automaton):
    transitions = automaton['transitions']

    # Collect all transitions with their symbols
    all_transitions = []
    for from_state, symbols in transitions.items():
        for symbol, to_states in symbols.items():
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
