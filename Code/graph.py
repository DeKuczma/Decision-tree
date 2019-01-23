import matplotlib.pyplot as plt
import matplotlib.image as image
import networkx as nx
import pydot


class Tree:

    def __init__(self, root):
        self.root = root
        self.G = pydot.Dot(graph_type='digraph')

    def draw_graph(self):
        if len(self.root.next_node) is 0:
            self.G.add_node(pydot.Node(str(self.root.node_number), label=self.root.value))
        else:
            self.G.add_node(pydot.Node(str(self.root.node_number), label=self.root.attribute))
        self.add_nodes(self.root)

        self.G.write("DecisionTree.png", format='png')
        img = image.imread("DecisionTree.png", format='png')
        plt.imshow(img, aspect='equal')
        plt.axis('off')
        plt.show()

    def add_nodes(self, node):
        for key in node.next_node.keys():
            if len(node.next_node[key].next_node) is 0:
                self.G.add_node(pydot.Node(str(node.next_node[key].node_number), label=node.next_node[key].value))
            else:
                self.G.add_node(pydot.Node(str(node.next_node[key].node_number), label=node.next_node[key].attribute))
                self.add_nodes(node.next_node[key])
            self.G.add_edge(pydot.Edge(str(node.node_number), str(node.next_node[key].node_number), label=key))

