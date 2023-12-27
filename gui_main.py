import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np
import controller
import nx_pylab as nxm
import nfa_tracing_methods as nfa

# 0 normal , 1 final , 2 start
nfa_graph = []
nfa_state = {}
dfa_graph = []
dfa_state = {}
dfa = {}
root = {}


def save_and_display_text(root):
    global curr_state
    curr_state = dfa_graph[0][0][0]
    global curr_states_nfa
    curr_states_nfa = {nfa_graph[0][0][0]}

    def save_text():
        global char_counter
        char_counter = 1
        global curr_state, curr_states_nfa
        curr_state = dfa_graph[0][0][0]
        curr_states_nfa = {nfa_graph[0][0][0]}
        global input_text
        input_text = textbox.get("1.0", "end-1c")
        label.config(state="normal")
        label.delete(1.0, tk.END)
        for line in input_text:
            label.insert(tk.END, line)
        label.config(state="disabled")

    def advance_color(end):
        global char_counter, ax, canvas, ret, curr_state
        global dfa_graph, curr_states_nfa
        edge_idx = -1

        for idx, data in enumerate(dfa_graph):
            if data[0][0] == curr_state and input_text[end - 1] in data[1]:
                edge_idx = idx
                curr_state = data[0][1]
                break
        edge_colors = []
        for i in range(len(dfa_graph)):
            if i != edge_idx:
                edge_colors.append('black')
            else:
                edge_colors.append('red')

        graph = nx.DiGraph()
        for edge in dfa_graph:
            node = edge[0]
            graph.add_node(node[0])
            graph.add_node(node[1])
        # Add edges and weights to the graph
        for edge in dfa_graph:
            node = edge[0]
            weight = edge[1]
            #     G.add_node(node[0])
            graph.add_edge(node[0], node[1], weight=weight)

        ## make graph for nfa
        graph_nfa = nx.DiGraph()
        for edge in nfa_graph:
            node = edge[0]
            graph_nfa.add_node(node[0])
            graph_nfa.add_node(node[1])
        # Add edges and weights to the graph
        for edge in nfa_graph:
            node = edge[0]
            weight = edge[1]
            graph_nfa.add_edge(node[0], node[1], weight=weight)
        edges, nxt_states = nfa.get_next_states_from_set_of_states(curr_states_nfa, input_text[end - 1], nfa_graph)
        curr_states_nfa = nxt_states
        edge_colors_nfa = []
        for node in graph_nfa.edges:
            if (node[0], node[1]) in edges:
                edge_colors_nfa.append('red')
            else:
                edge_colors_nfa.append('black')

        trace(graph, dfa_state, ax, canvas, edge_colors)
        trace(graph_nfa, nfa_state, ax2, canvas2, edge_colors_nfa)
        char_counter = 1 + char_counter
        highlight_text(tag_name='tag1', lineno=1, start_char=0, end_char=end, fg_color='red')

    def highlight_text(tag_name, lineno, start_char, end_char, bg_color=None, fg_color=None):
        label.tag_add(tag_name, f'{lineno}.{start_char}', f'{lineno}.{end_char}')
        label.tag_config(tag_name, background=bg_color, foreground=fg_color)

    global char_counter, ret
    ret = 0

    char_counter = 1
    new_window = tk.Toplevel(root)
    new_window.title("Input Text")
    custom_font = ("Arial", 14)
    textbox = tk.Text(new_window, height=4, width=30, font=custom_font)
    textbox.pack(padx=10, pady=10)

    save_button = tk.Button(new_window, text="Save", command=save_text)
    save_button.pack(padx=10, pady=5)

    label = tk.Text(new_window, height=4, width=30, state="disabled", font=custom_font)
    label.pack(padx=10, pady=5)

    advance_button = tk.Button(new_window, text="Advance", command=lambda: advance_color(char_counter))
    advance_button.pack(padx=10, pady=5)


def save_input(states_entry, sigma_entry, start_state_entry, final_state_entry, transitions_entry, window):
    global dfa_graph
    global dfa_state
    global nfa_graph
    global nfa_state
    global dfa

    states = states_entry.get("1.0", "end-1c")
    sigma = sigma_entry.get("1.0", "end-1c")
    transitions = transitions_entry.get("1.0", "end-1c")
    start_state = start_state_entry.get("1.0", "end-1c")
    final_states = final_state_entry.get("1.0", "end-1c")

    # Process and save the input
    print("States:", states)
    print("Sigma:", sigma)
    print("Transitions:\n", transitions)
    print("Start State:", start_state)
    print("Final State:", final_states)

    nfa_graph, nfa_state, dfa_graph, dfa_state, dfa = controller.process_input(
        states, sigma, transitions, start_state, final_states
    )

    # Close the window after saving
    window.destroy()

    # draw the NFA
    draw_nfa(graph=nfa_graph, ax=ax2, canvas=canvas2, state=nfa_state)

    # draw the DFA
    draw_graph(ax, canvas, dfa_state, dfa_graph)

    # Show DFA description
    dfa_description_window(root)


def clear_text(entry_fields):
    for entry in entry_fields:
        entry.delete("1.0", tk.END)  # Clear content from each Text widget


def nfa_description_window(root):
    new_window = tk.Toplevel(root)
    new_window.title("NFA Definition")

    labels = ["States:", "Sigma:", "Start State:", "Final States:", "Transitions:"]
    entry_texts = ["{q0, q1, q2}", "{0, 1}", "q0", "{q2}", "{\n"
                                                           "    (q0, 0) = {q0}\n"
                                                           "    (q0, 1) = {q0, q1}\n"
                                                           "    (q1, 0) = {q2}\n"
                                                           "    (q1, 1) = {q2}\n"
                                                           "    (q2, 0) = {q2}\n"
                                                           "}"]

    entry_fields = []
    for i, label_text in enumerate(labels):
        label = tk.Label(new_window, text=label_text, font=("Arial", 14))  # Increase font size
        label.grid(row=i, column=0, padx=10, pady=5)
        entry_text = tk.Text(new_window, font=("Arial", 12), height=get_height(i, 1), width=30)
        entry_text.insert(tk.END, entry_texts[i])
        entry_text.grid(row=i, column=1, padx=10, pady=5)
        entry_fields.append(entry_text)

    note = tk.Label(new_window, text="Note: Use the letter 'e' to denote epsilon transitions.", font=("Arial", 14))
    note.grid(row=5, columnspan=2, padx=10, pady=5)

    save_button = tk.Button(new_window, text="Save Input", font=("Arial", 12),
                            command=lambda: save_input(*entry_fields, new_window))  # Increase font size
    save_button.grid(row=len(labels) + 1, columnspan=2, pady=10)

    clear_button = tk.Button(new_window, text="Clear Input", font=("Arial", 12),
                             command=lambda: clear_text(entry_fields))
    clear_button.grid(row=len(labels) + 2, columnspan=2, pady=10)


def dfa_description_window(root):
    new_window = tk.Toplevel(root)
    new_window.title("DFA Definition")

    labels = ["States:", "Sigma:", "Start State:", "Final States:", "Transitions:"]
    entry_texts = ['{ ' + str(dfa["states"]).strip('[]').replace('\'', '') + ' }',
                   str(dfa["alphabet"]).replace('[', '{').replace(']', '}').replace('\'', ''),
                   str(dfa["start_state"]).replace('\'', ''),
                   '{ ' + str(dfa["accept_states"]).strip('[]').replace('\'', '') + ' }',
                   controller.formalize_dfa_transitions(dfa["transitions"])]

    entry_fields = []
    for i, label_text in enumerate(labels):
        label = tk.Label(new_window, text=label_text, font=("Arial", 14))  # Increase font size
        label.grid(row=i, column=0, padx=10, pady=5)
        entry_text = tk.Text(new_window, font=("Arial", 12), height=get_height(i, 5), width=60)
        entry_text.insert(tk.END, entry_texts[i])
        entry_text.grid(row=i, column=1, padx=10, pady=5)
        entry_fields.append(entry_text)
        entry_text.config(state=tk.DISABLED)


def get_height(i, default):
    # height if the textboxes, the height of transitions textbox is not the default
    if i == 4:
        return 20
    return default


def update_view(graph, ax, canvas, state):
    # global ax, canvas  # Access the ax and canvas variables from the global scope
    # Clear the previous plot
    ax.clear()

    colors = []
    for node in graph.nodes:
        if state[node] == 0:  # normal
            colors.append((0.1, 0.2, 0.5, 0.5))
        elif state[node] == 1:  # final
            colors.append('green')
        elif state[node] == 2:  # start
            colors.append('red')
        else:
            colors.append('yellow')

    # Draw the directed graph with edge labels
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, ax=ax, with_labels=True, node_color=colors, node_size=2000, arrows=True)
    edge_labels = {(u, v): graph.edges[u, v]['weight'] for u, v in graph.edges()}
    label_pos = {}
    for edge in graph.edges():
        label_pos[edge] = 0.3

    nxm.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax, rotate=False, label_pos=0.8,
                                  font_weight='bold', font_size=12)

    # Refresh canvas
    canvas.draw()


def trace(graph, state, ax, canvas, edge_colors):
    # global ax, canvas  # Access the ax and canvas variables from the global scope
    # Clear the previous plot
    ax.clear()

    colors = []
    for node in graph.nodes:
        if state[node] == 0:  # normal
            colors.append((0.1, 0.2, 0.5, 0.5))
        elif state[node] == 1:  # final
            colors.append('green')
        elif state[node] == 2:  # start
            colors.append('red')
        else:
            colors.append('yellow')

    # Draw the directed graph with edge labels
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, ax=ax, with_labels=True, node_color=colors, node_size=2000, arrows=True, edge_color=edge_colors,
            width=2.0)
    edge_labels = {(u, v): graph.edges[u, v]['weight'] for u, v in graph.edges()}
    label_pos = {}
    for edge in graph.edges():
        label_pos[edge] = 0.3

    nxm.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax, rotate=False, label_pos=0.8,
                                  font_weight='bold', font_size=12)

    # Refresh canvas
    canvas.draw()


def draw_graph(ax, canvas, state, graph_data):
    graph = nx.DiGraph()
    for edge in graph_data:
        node = edge[0]
        graph.add_node(node[0])
        graph.add_node(node[1])
    # Add edges and weights to the graph
    for edge in graph_data:
        node = edge[0]
        weight = edge[1]
        #     G.add_node(node[0])
        graph.add_edge(node[0], node[1], weight=weight)
    update_view(graph, ax, canvas, state)


def draw_nfa(graph, ax, canvas, state):
    draw_graph(ax, canvas, state, graph)


def main():
    global ax, canvas, ax2, canvas2  # Define ax and canvas globally
    global root

    # Create the GUI window
    root = tk.Tk()
    root.title("NFA to DFA Converter")

    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 6))
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    # Create a canvas for the figure within the GUI
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)

    canvas_widget = canvas.get_tk_widget()
    canvas_widget2 = canvas2.get_tk_widget()

    canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, side=tk.RIGHT)
    canvas_widget.config(borderwidth=2, relief=tk.SOLID)
    canvas_widget2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, side=tk.LEFT)
    canvas_widget2.config(borderwidth=2, relief=tk.SOLID)

    # Button to update the view
    nfa_window_button = tk.Button(root, text="NFA formal description", command=lambda: nfa_description_window(root))
    trace_button = tk.Button(root, text="trace a string", command=lambda: save_and_display_text(root))
    nfa_window_button.pack(padx=20, pady=10)
    trace_button.pack(padx=20, pady=10)

    # Initially, update the view
    empty_graph = nx.DiGraph()
    update_view(empty_graph, ax, canvas, dfa_state)
    draw_nfa(graph=nfa_graph, ax=ax2, canvas=canvas2, state=nfa_state)

    # Start the GUI event loop
    root.state('zoomed')
    root.mainloop()


if __name__ == "__main__":
    main()
