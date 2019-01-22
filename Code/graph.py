import matplotlib.pyplot as plt
import networkx as nx
from networkx import DiGraph
from networkx.drawing.nx_agraph import graphviz_layout

class Tree:

    def __init__(self, root):
        self.root = root
        self.G = DiGraph()

    def draw_graph(self):
        if len(self.root.next_node) is 0:
            self.G.add_node(self.root.node_number, name=self.root.value)
        else:
            self.G.add_node(self.root.node_number, name=self.root.attribute)
        self.add_nodes(self.root)
        pos = graphviz_layout(self.G)
        edge_labels = nx.get_edge_attributes(self.G, 'label')
        node_labels = nx.get_node_attributes(self.G, 'name')
        nx.draw(self.G, pos)
        nx.draw_networkx_labels(self.G,  pos, labels=node_labels)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.title("Decision tree")
        plt.savefig("graph.pdf")
        plt.show()

    def add_nodes(self, node):
        for key in node.next_node.keys():
            if len(node.next_node[key].next_node) is 0:
                self.G.add_node(node.next_node[key].node_number, name=node.next_node[key].value)
            else:
                self.G.add_node(node.next_node[key].node_number, name=node.next_node[key].attribute)
                self.add_nodes(node.next_node[key])
            self.G.add_edge(node.node_number, node.next_node[key].node_number, label=key)

