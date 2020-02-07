
class Vertex:
    """ a Vertex is a node in the CMAP graph that has related source and target nodes """
    def __init__(self, id, label, color="#0000FF", type=None, parent_id=None, **kwargs):
        """
        :param id: concept identifier string from the CMAP CXL file
        :param label: concept label string from the CMAP CXL file
        :param type: concept type assigned by the ConceptType class; currently a string, but will be changed to an object
        :param parent_id: CMAP CXL parent id means this is in a bundle - typically of attributes or keys
        """
        self.source = []
        self.target = []
        self.id = id
        self.label = label
        self.type = type
        self.parent_id = parent_id
        self.color = color
        self.is_root = False
        self.ct_subset = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def add_source(self, node, relationship):
        """
        add a Vertex node as a source of this Vertex object
        :param node: a Vertex object representing a graph node that is added as a source to this object (node)
        :param relationship: string describing the relationship of the source node to this object (node)
        """
        if isinstance(node, Vertex):
            self.source.append((node, relationship))
        else:
            self._print_node_type_error(node)

    def add_target(self, node, relationship):
        """
        add a Vertex node as a target of this Vertex object
        :param node: a Vertex object representing a graph node that is added as a target from this object (node)
        :param relationship: string describing the relationship of this object (node) to the target node
        """
        if isinstance(node, Vertex):
            self.target.append((node, relationship))
        else:
            self._print_node_type_error(node)

    def add_ct_subset(self, subset):
        self.ct_subset = subset

    def _print_node_type_error(self, node):
        """
        the node requested to be added as a source or target of this Vertex is not a Vertex object
        :param node: node of unknown type; not of type Vertex as expected
        """
        raise ValueError(f"Unknown node type {type(node)} when adding a source or target in Vertex {self.id}")