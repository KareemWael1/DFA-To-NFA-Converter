import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes
G.add_nodes_from([1, 2, 3, 4])

# Add edges with specific colors and default label 'a'
edges = [
    (1, 2, {'color': 'red', 'label': 'a'}),
    (2, 3, {'color': 'blue', 'label': 'a'}),
    (3, 4, {'color': 'green', 'label': 'a'}),
    (4, 1, {'color': 'purple', 'label': 'a'})
]
G.add_edges_from(edges)

# Extract colors and labels from the edge attributes
edge_colors = [edge[2]['color'] for edge in G.edges(data=True)]
edge_labels = {(edge[0], edge[1]): edge[2]['label'] for edge in G.edges(data=True)}

# Draw the graph with edge colors and labels
pos = nx.circular_layout(G)  # Positions of the nodes
nx.draw(G, pos, with_labels=True, edge_color=edge_colors, node_size=500, node_color='skyblue', font_weight='bold')

# Draw edge labels
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

# Display the graph
plt.show()
