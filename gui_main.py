import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np
import nx_pylab as nxm


def save_and_display_text(root):
    global curr_state
    curr_state = 1
    def save_text():
        global char_counter
        char_counter = 1
        global curr_state
        curr_state = 1
        global input_text
        input_text = textbox.get("1.0", "end-1c")
        label.config(state="normal")
        label.delete(1.0, tk.END)
        for line in input_text:
            label.insert(tk.END, line)
        label.config(state="disabled")

    def advance_color(end):
        global char_counter, ax, canvas, ret,curr_state
        graph_data = [
            [(1, 2), "a,b"],
            [(2, 3), "a"],
            [(3, 4), "b"],
            [(4, 1), "a"],
            [(4, 2), "b"]
        ]
        edge_idx = -1

        for idx, data in enumerate(graph_data):
            if data[0][0] == curr_state and input_text[end-1] in data[1]:
                edge_idx = idx
                curr_state = data[0][1]
                break
        edge_colors = []
        for i in range(len(graph_data)):
            if i != edge_idx:
                edge_colors.append('black')
            else:
                edge_colors.append('red')

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
            trace(graph, [-1, 1, 2, 0, 0, 0, 0], ax, canvas, edge_colors)

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


def save_input(states_entry, transitions_entry, final_state_entry, start_state_entry, sigma_entry, window):
    states = states_entry.get()
    transitions = transitions_entry.get()
    final_state = final_state_entry.get()
    start_state = start_state_entry.get()
    sigma = sigma_entry.get()

    # Process and save the input
    print("States:", states)
    print("Transitions:", transitions)
    print("Final State:", final_state)
    print("Start State:", start_state)
    print("Sigma:", sigma)

    # Close the window after saving
    window.destroy()


def open_new_window(root):
    new_window = tk.Toplevel(root)
    new_window.title("NFA Definition")

    labels = ["States:", "Transitions:", "Final State:", "Start State:", "Sigma:"]
    entry_texts = ["State1,State2,State3", "s1 s2 alpha, s2 s3 alpha", "State1", "State1", "A,B,C"]

    entry_fields = []
    for i, label_text in enumerate(labels):
        label = tk.Label(new_window, text=label_text, font=("Arial", 14))  # Increase font size
        label.grid(row=i, column=0, padx=10, pady=5)

        entry_text = tk.Entry(new_window, font=("Arial", 12))  # Increase font size
        entry_text.insert(tk.END, entry_texts[i])
        entry_text.grid(row=i, column=1, padx=10, pady=5)
        entry_fields.append(entry_text)

    save_button = tk.Button(new_window, text="Save Input", font=("Arial", 12),
                            command=lambda: save_input(*entry_fields, new_window))  # Increase font size
    save_button.grid(row=len(labels), columnspan=2, pady=10)


def zoom_in():
    zoom(1.1)


def zoom_out():
    zoom(0.9)


def zoom(zoom_factor):
    # Get the current limits of the plot
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Calculate the new limits after zooming
    x_center = np.mean(xlim)
    y_center = np.mean(ylim)
    new_xlim = (xlim[0] - x_center) * zoom_factor + x_center, (xlim[1] - x_center) * zoom_factor + x_center
    new_ylim = (ylim[0] - y_center) * zoom_factor + y_center, (ylim[1] - y_center) * zoom_factor + y_center

    # Set the new limits to the plot
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)

    # Redraw the plot
    canvas.draw()


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
        else:  # start
            colors.append('red')

    # Draw the directed graph with edge labels
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, ax=ax, with_labels=True, node_color=colors, node_size=500, arrows=True)
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
        else:  # start
            colors.append('red')

    # Draw the directed graph with edge labels
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, ax=ax, with_labels=True, node_color=colors, node_size=500, arrows=True, edge_color=edge_colors)
    edge_labels = {(u, v): graph.edges[u, v]['weight'] for u, v in graph.edges()}
    label_pos = {}
    for edge in graph.edges():
        label_pos[edge] = 0.3

    nxm.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax, rotate=False, label_pos=0.8,
                                  font_weight='bold', font_size=12)

    # Refresh canvas
    canvas.draw()


# inputs to the program
graph_data = [
    [(1, 2), "a,b"],
    [(2, 3), "a"],
    [(3, 4), "b"],
    [(4, 1), "a"],
    [(4, 2), "b"]
]
state = [0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]

nfa_graph = [
    [(1, 2), "a,b"],
    [(2, 3), "a"],
    [(3, 4), "b"],
    [(4, 1), "a"],
    [(4, 2), "b"]
]
nfa_state = [0, 2, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]


# -------------------------

def final(ax, canvas, state, graph_data):
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


next_count = 0


def draw_next(ax, canvas, state):
    global next_count
    graph = nx.DiGraph()

    for edge in graph_data:
        node = edge[0]
        graph.add_node(node[0])
        graph.add_node(node[1])

    if next_count == 0:
        update_view(graph, ax, canvas, state)
    else:
        for edge in graph_data:
            node = edge[0]
            w = edge[1]
            if node[0] <= next_count:
                graph.add_edge(node[0], node[1], weight=w)
        update_view(graph, ax, canvas, state)
    next_count += 1


def draw_nfa(graph, ax, canvas, state):
    final(ax, canvas, state, graph)


def main():
    global ax, canvas  # Define ax and canvas globally

    # Create the GUI window
    root = tk.Tk()
    root.title("DFA Viewer")

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
    update_button = tk.Button(root, text="Next step", command=lambda: draw_next(ax, canvas, state))
    final_button = tk.Button(root, text="Final DFA", command=lambda: final(ax, canvas, state, graph_data))
    update_button.pack()
    final_button.pack()
    zoom_in_button = tk.Button(root, text="trace a string", command=lambda: save_and_display_text(root))
    zoom_out_button = tk.Button(root, text="Zoom Out", command=zoom_out)
    zoom_in_button.pack()
    zoom_out_button.pack()

    open_window_button = tk.Button(root, text="NFA formal description", command=lambda: open_new_window(root))
    open_window_button.pack(padx=20, pady=10)

    # Initially, update the view
    empty_graph = nx.DiGraph()
    update_view(empty_graph, ax, canvas, state)
    draw_nfa(graph=nfa_graph, ax=ax2, canvas=canvas2, state=nfa_state)
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
