import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np

def open_new_window():
    global root
    new_window = tk.Toplevel(root)
    new_window.title("New Window")

    # Labels and entry fields for states, transitions, final state, start state, and sigma
    labels = ["States:", "Transitions:", "Final State:", "Start State:", "Sigma:"]
    entry_texts = ["State1,State2,State3", "A->B, B->C, C->A", "State1", "State1", "A,B,C"]

    for i, label_text in enumerate(labels):
        label = tk.Label(new_window, text=label_text)
        label.grid(row=i, column=0, padx=10, pady=5)

        entry_text = tk.Entry(new_window)
        entry_text.insert(tk.END, entry_texts[i])
        entry_text.grid(row=i, column=1, padx=10, pady=5)
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


def update_view(graph):
    global ax, canvas  # Access the ax and canvas variables from the global scope
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

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax, rotate=False, label_pos=0.8,
                                 font_weight='bold', font_size=12)

    # Refresh canvas
    canvas.draw()


# inputs to the program
graph_data = [
    [(1, 2), "a,b"],
    [(2, 6), "a"],
    [(2, 9), "b"],
    [(3, 8), "a"],
    [(3, 6), "b"],
    [(4, 11), "b"],
    [(4, 4), "a"],
    [(5, 7), "a"],
    [(5, 3), "a,b,c,d,e,f"],
    [(5, 11), "a"],
    [(5, 10), "b"],
    [(6, 9), "b"],
    [(8, 8), "a"],
    [(10, 1), "b"]

]
state = [-1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]


# -------------------------

def final():
    graph = nx.DiGraph()
    for edge in graph_data:
        node = edge[0]
        graph.add_node(node[0])
        graph.add_node(node[0])
    # Add edges and weights to the graph
    for edge in graph_data:
        node = edge[0]
        weight = edge[1]
        #     G.add_node(node[0])
        graph.add_edge(node[0], node[1], weight=weight)
    update_view(graph)


next_count = 0


def draw_next():
    global next_count
    graph = nx.DiGraph()

    for edge in graph_data:
        node = edge[0]
        graph.add_node(node[0])
        graph.add_node(node[0])

    if next_count == 0:
        update_view(graph)
    else:
        for edge in graph_data:
            node = edge[0]
            w = edge[1]
            if node[0] <= next_count:
                graph.add_edge(node[0], node[1], weight=w)
        update_view(graph)
    next_count += 1


def main():
    global ax, canvas, root # Define ax and canvas globally

    # Create the GUI window
    root = tk.Tk()
    root.title("DFA Viewer")

    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 6))
    fig2,ax2 = plt.subplots(figsize=(6, 6))
    # Create a canvas for the figure within the GUI
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)

    canvas_widget = canvas.get_tk_widget()
    canvas_widget2 = canvas2.get_tk_widget()

    canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10,side=tk.RIGHT)
    canvas_widget.config(borderwidth=2, relief=tk.SOLID)
    canvas_widget2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, side=tk.LEFT)
    canvas_widget2.config(borderwidth=2, relief=tk.SOLID)

    # Button to update the view
    update_button = tk.Button(root, text="Next step", command=draw_next)
    final_button = tk.Button(root, text="Final DFA", command=final)
    update_button.pack()
    final_button.pack()
    zoom_in_button = tk.Button(root, text="Zoom In", command=zoom_in)
    zoom_out_button = tk.Button(root, text="Zoom Out", command=zoom_out)
    zoom_in_button.pack()
    zoom_out_button.pack()

    open_window_button = tk.Button(root, text="Open New Window", command=open_new_window)
    open_window_button.pack(padx=20, pady=10)

    # Initially, update the view
    empty_graph = nx.DiGraph()
    update_view(empty_graph)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
