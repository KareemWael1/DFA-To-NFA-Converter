import json
from collections import deque
from NFA_testing import NFA_ex0, NFA_ex1, NFA_ex2, NFA_ex3, NFA_ex4


def epsilon_closure(states, transitions):
    epsilon_closure_set = set(states)
    queue = deque(states)

    while queue:
        current_state = queue.popleft()

        if "ε" in transitions[current_state]:
            for state in transitions[current_state]["ε"]:
                if state not in epsilon_closure_set:
                    queue.append(state)

            epsilon_closure_set.update(transitions[current_state]["ε"])

    return tuple(sorted(list(epsilon_closure_set)))


def move(states, symbol, transitions):
    result = set()

    for state in states:
        if symbol in transitions[state]:
            result.update(transitions[state][symbol])

    return tuple(sorted(list(result)))


def nfa_to_dfa(nfa):
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
dfa_json = nfa_to_dfa(NFA_ex4)
