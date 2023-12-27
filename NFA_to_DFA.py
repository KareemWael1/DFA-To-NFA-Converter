from collections import deque
from NFA_testing import NFA_ex0, NFA_ex1, NFA_ex2, NFA_ex3, NFA_ex4


def epsilon_closure(states, transitions):
    epsilon_closure_set = set(states)
    queue = deque(states)

    while queue:
        current_state = queue.popleft()

        if "e" in transitions[current_state]:
            for state in transitions[current_state]["e"]:
                if state not in epsilon_closure_set:
                    queue.append(state)

            epsilon_closure_set.update(transitions[current_state]["e"])

    return sorted(list(epsilon_closure_set))


def move(states, symbol, transitions):
    result = set()

    for state in states:
        if symbol in transitions[state]:
            result.update(transitions[state][symbol])

    return sorted(list(result))


def nfa_to_dfa(nfa):
    dfa_states = []
    dfa_transitions = {}
    start_state = epsilon_closure([nfa["start_state"]], nfa["transitions"])
    queue = deque([start_state])

    while queue:
        current_states = queue.popleft()

        if current_states not in dfa_states:
            dfa_states.append(current_states)

        for symbol in nfa["alphabet"]:
            next_states = epsilon_closure(move(current_states, symbol, nfa["transitions"]), nfa["transitions"])

            if next_states:
                current_states_str = str(current_states)
                next_states_str = str(next_states)

                if current_states_str not in dfa_transitions:
                    dfa_transitions[current_states_str] = {}

                dfa_transitions[current_states_str][symbol] = next_states_str

                if next_states not in dfa_states:
                    queue.append(next_states)

    dfa_accept_states = [state for state in dfa_states if any(s in nfa["accept_states"] for s in state)]

    dfa = {
        "states": dfa_states,
        "alphabet": nfa["alphabet"],
        "transitions": dfa_transitions,
        "start_state": start_state,
        "accept_states": dfa_accept_states
    }

    return dfa
