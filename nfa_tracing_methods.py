

def get_next_states_from_one_state(curr_state, char, graph):
    current_states = {curr_state}
    edges_used = set()
    # getting all epsilon*
    while True:
        old = len(current_states)
        for node in graph:
            if node[0][0] in current_states and 'E' in node[1]:
                current_states.add(node[0][1])
                edges_used.add((node[0][0], node[0][1]))
        if old == len(current_states):
            break
    # getting the char transition
    next_states = set()
    for node in graph:
        if node[0][0] in current_states and char in node[1]:
            next_states.add(node[0][1])
            edges_used.add((node[0][0], node[0][1]))

    # getting epsilon* transitions
    while True:
        old = len(next_states)
        for node in graph:
            if node[0][0] in next_states and 'E' in node[1]:
                next_states.add(node[0][1])
                edges_used.add((node[0][0], node[0][1]))
        if old == len(next_states):
            break
    return edges_used, next_states


"""
:returns edges used and next states
"""


def get_next_states_from_set_of_states(curr_states, char, graph):
    next_states = set()
    edges_used = set()
    for state in curr_states:
        e, s = get_next_states_from_one_state(state, char, graph)
        next_states.update(s)
        edges_used.update(e)
    print(next_states)
    print(edges_used)
    return edges_used, next_states


