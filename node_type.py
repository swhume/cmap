"""
NodeType identifies the type of a node (or concept) found in a CMAP. In CMAPs node types are identified by visual
characteristics such as the background color, border color, or border shape. Each node has a name and a label,
in addition to the specific identifying characteristics for that node. The node types are created from the config file,
not from the individual key concepts found in the CMAPs.
"""
class NodeType:
    def __init__(self, name, label, node_color="#0000FF", source_links=[], target_links=[],
                 background_color=None, border_color=None, border_shape=None):
        self.name = name
        self.label = label
        self.border_color = border_color
        self.background_color = background_color
        self.border_shape = border_shape
        self.node_color = node_color
        self.valid_source_links = source_links
        self.valid_target_links = target_links

    def is_root_concept(self):
        """
        returns true when the node type is the root concept, or observation concept for BCs
        :return: boolean
        """
        if self.name == "root_concept":
            return True
        else:
            return False


