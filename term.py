
class Term:
    """ individual term that exists as part of a CT subset """
    def __init__(self, c_code, sub_val, default="No"):
        """
        :param c_code: CT term concept code
        :param sub_val:  CT term submission value
        :param default: Yes or No indicator determining of the term is the default value of the subset
        """
        self.c_code = c_code
        self.sub_val = sub_val
        self.default = default
        if self.default.lower() == "yes":
            self.is_default = True
        else:
            self.is_default = False
        self.label = sub_val + " (" + c_code + ")"