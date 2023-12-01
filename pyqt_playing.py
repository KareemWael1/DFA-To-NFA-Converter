import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget
import networkx as nx


# Your existing functions and data
def update_view(graph):
    global ax, canvas, state  # Access the ax and canvas variables from the global scope
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

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax, rotate=True, label_pos=0.8,
                                 font_weight='bold', font_size=12)

    # Refresh canvas
    canvas.draw()


# inputs to the program
graph_data = [
    [(1, 2), "a,b"],
    [(2, 3), "a"],
    [(2, 2), "b"],
    [(3, 4), "a"],
    [(3, 1), "b"],
    [(4, 1), "b"],
    [(4, 2), "a"],
    [(5, 1), "a"],
    [(5, 5), "a,b"]
]
state = [-1, 2, 0, 0, 1, 0]

next_count = 0


class NetworkGraph(QMainWindow):
    def __init__(self):
        super().__init__()
        global ax, canvas
        self.setWindowTitle("DFA Viewer")

        # Create a matplotlib figure
        self.figure, ax = plt.subplots(figsize=(12, 12))

        # Create a canvas for the figure within the PyQt5 window
        canvas = FigureCanvas(self.figure)
        self.setCentralWidget(QWidget(self))
        layout = QVBoxLayout()
        layout.addWidget(canvas)

        # Buttons to interact with the graph
        self.update_button = QPushButton("Next step", self)
        self.update_button.clicked.connect(self.draw_next)
        self.final_button = QPushButton("Final DFA", self)
        self.final_button.clicked.connect(self.final)
        layout.addWidget(self.update_button)
        layout.addWidget(self.final_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initially, update the view
        empty_graph = nx.DiGraph()
        update_view(empty_graph)

    def final(self):
        graph = nx.DiGraph()

        # Add edges and weights to the graph
        for edge in graph_data:
            node = edge[0]
            weight = edge[1]
            #     G.add_node(node[0])
            graph.add_edge(node[0], node[1], weight=weight)
        update_view(graph)

    def draw_next(self):
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
    app = QApplication(sys.argv)
    window = NetworkGraph()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
