import term


class Subset:
    """
    CDISC controlled terminology subset provided as part of an enumerated Conceptual Domain
    """
    def __init__(self, c_code, name):
        """
        :param c_code: subset list concept code
        :param name:  subset list name
        """
        self.c_code = c_code
        self.name = name
        self.terms = []

    def add_term(self, c_code, sub_val, default="No"):
        """
        add a new term to the list of terms in the CT subset
        :param c_code: CT term concept code
        :param sub_val: CT term submission value
        :param default: if the CT term is the default value in this subset
        """
        self.terms.append(term.Term(c_code, sub_val, default))