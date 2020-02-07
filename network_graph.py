import networkx as nx


class NetworkGraph:
    """
    NetworkGraph uses the networkx module to create a GraphML representation of the CMAP graph
    """
    def __init__(self, cmap):
        """
        :param cmap is a graph structure build from the CMAP CXL format
        """
        self.g = nx.DiGraph()               # this is a directed graph
        self.cmap = cmap                    # this graph is built from the cmap graph
        self._add_nodes()
        self.node_count = self.g.number_of_nodes()
        self._add_edges()
        self.edge_count = self.g.number_of_edges()

    def _add_nodes(self):
        """
        add the cmap nodes to the GraphML version of the graph
        """
        node_number = 0
        for id, v in self.cmap.vertexes.items():
            node_number += 1
            self.g.add_node(id, id=id, name=v.label, type=v.type, description=v.label, color=v.color)

    def _add_edges(self):
        """
        add the cmap edges to the GraphML version of the graph
        """
        for id, v in self.cmap.vertexes.items():
            for s in v.source:
                self.g.add_edge(s[0].id, id, description=s[1])
            for t in v.target:
                self.g.add_edge(id, t[0].id, description=s[1])

    def save_graphml(self, file_name):
        """
        save the GraphML version of the graph to the
        :param file_name
        """
        nx.write_graphml(self.g, file_name)
