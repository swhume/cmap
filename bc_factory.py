"""
Copyright (c) 2020 Sam Hume

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import bc
import os

class BCFactory:
    """ BCFactory creates a BC object using metadata extracted from the CMAP graph"""
    def __init__(self, cmap, config):
        """
        BCFactory constructor
        :param cmap: CMAP graph containing vertexes and edges used to generate BC content
        :param config: configuration object with config parameters
        """
        self.cmap = cmap
        self.cfg = config
        self.kwargs = {}
        self._node_types = {}
        self._qualifiers = []
        self._get_node_types()

    def save_bc(self, bc):
        """
        serializes a BC object as JSON and writes it to a file
        :param bc: a BC object
        """
        json_bc = bc.serialize_json()
        file_name = os.path.join(self.cfg.data_path_dir, bc.designation.replace(" ", "_") + ".json")
        with open(file_name, "w", encoding="utf-8") as fo:
            fo.write(json_bc)

    def create_bc(self):
        """
        use information in the graph created from the CMAP to create a BC object
        :return: a BC object
        """
        for node_name, vertex in self.cmap.vertexes.items():
            if vertex.is_root:
                self._set_name_c_code(vertex.label)
            elif vertex.type == self._node_types["dec"]:
                self._set_dec_attributes(vertex)
            # TODO process other vertext types as needed
        self.kwargs["dataElementConcepts"] = self._qualifiers
        return bc.BiomedicalConcept(**self.kwargs)

    def _set_dec_attributes(self, vertex):
        """
        for data element concept (DEC) typed nodes set the BC attributes based on the role
        :param vertex: node object from the graph created using the CMAP
        """
        try:
            # TODO fix hard coded roles
            if vertex.role.lower() == "qualifier.variable.units":
                self._set_units(vertex)
            elif vertex.role.lower() == "qualifier.result":
                self._set_result(vertex)
            elif vertex.role.lower() == "topic.test_code":
                self._set_test_code(vertex)
            elif vertex.role.lower() == "topic":
                self._set_qualifier(vertex)
            elif vertex.role.lower() == "qualifier.synonym.name":
                self._set_test_name(vertex)
            elif vertex.role.lower() == "qualifier.synonym.loinc":
                self._set_loinc_code(vertex)
            elif vertex.role.lower() == "qualifier.record" or vertex.role.lower() == "qualifier.variable" or \
                vertex.role.lower() == "qualifier.grouping":
                self._set_qualifier(vertex)
            elif vertex.role.lower() == "timing":
                self._set_timing(vertex)
            else:
                print(f"not processing role: {vertex.role}")
        except AttributeError:
            print(f"Concept {vertex.label} is missing the role attribute")

    def _set_timing(self, vertex):
        """
        sets the described CD value to the datetime format
        :param vertex: node object from the graph created using the CMAP
        """
        for node in vertex.target:
            if node[0].type == "Conceptual Domain":
                qualifier = {}
                self.kwargs["format"] = node[0].label.strip()
                dec_concept, dec_name = self._concept_id_name_from_label(vertex.label)
                qualifier[dec_concept] = {"decName": dec_name, "decConceptId": dec_concept,
                                    "conceptualDomainType": "described",
                                    "conceptualDomainName": self.kwargs["format"],
                                    "role": vertex.role, "mandatory": vertex.mandatory}
                self._qualifiers.append(qualifier)
                break

    def _set_qualifier(self, vertex):
        """
        for DECs with role qualifier set the BC attributes
        :param vertex: node object from the graph created using the CMAP
        """
        for node in vertex.target:
            qualifier = {}
            if node[0].type == "Conceptual Domain":
                dec_concept, dec_name = self._concept_id_name_from_label(vertex.label)
                if node[0].ct_subset:
                    qualifier[dec_concept] = self._set_qualifier_subset(node[0].ct_subset, vertex, dec_concept, dec_name)
                else:
                    qualifier[dec_concept] = self._set_qualifier_datatype(node[0].label, vertex, dec_concept, dec_name)
                self._qualifiers.append(qualifier)
                break

    def _set_qualifier_datatype(self, data_type, vertex, dec_concept, dec_name):
        return {"decName": dec_name, "decConceptId": dec_concept, "conceptualDomainType": "described",
                "conceptualDomainName": data_type, "role": vertex.role, "mandatory": vertex.mandatory}

    def _set_qualifier_subset(self, subset, vertex, dec_concept, dec_name):
        """
        return the name, c-code, and terms for a CT subset that defines a DEC CD (conceptual domain)
        :param subset: obj- CT subset object that includes the list of terms
        :param dec_concept: str - concept code for DEC
        :param subset: str- DEC name
        :return: qualifier CT subset dictionary
        """
        qualifier_subset = {"decName": dec_name, "decConceptId": dec_concept, "conceptualDomainType": "enumerated",
                            "conceptualDomainName": subset.name, "conceptualDomainConceptId": subset.c_code,
                            "role": vertex.role, "mandatory": vertex.mandatory,
                            "terms": self._set_qualifier_terms(subset.terms)}
        return qualifier_subset

    def _set_qualifier_terms(self, dec_terms):
        terms = []
        for term in dec_terms:
            term_label = term.label
            if term.is_default:
                term_label = term_label + " default"
            terms.append(term_label)
        return terms

    def _set_test_code(self, vertex):
        """
        sets the TESTCD and associated c-code for findings domain BCs; set to one value for the BC
        :param vertex: node object from the graph created using the CMAP
        """
        for node in vertex.target:
            qualifier = {}
            if node[0].type == "Conceptual Domain":
                self.kwargs["test_cd"] = node[0].label.split("(")[0].strip()
                self.kwargs["test_c_code"] = node[0].label.split("(")[1].strip()[:-1]
                dec_concept, dec_name = self._concept_id_name_from_label(vertex.label)
                qualifier[dec_concept] = {"decName": dec_name, "decConceptId": dec_concept,
                                    "conceptualDomainType": "enumerated",
                                    "conceptualDomainName": self.kwargs["test_cd"],
                                    "conceptualDomainConceptId": self.kwargs["test_c_code"],
                                    "role": vertex.role, "mandatory": vertex.mandatory,
                                    "terms": self._set_qualifier_terms(node[0].ct_subset.terms)}
                self._qualifiers.append(qualifier)
                break

    def _set_test_name(self, vertex):
        """
        sets the test name for findings domain BCs; set to one value for the BC
        :param vertex: node object from the graph created using the CMAP
        """
        for node in vertex.target:
            if node[0].type == "Conceptual Domain":
                qualifier = {}
                self.kwargs["test_name"] = node[0].label.split("(")[0].strip()
                test_name_c_code = node[0].label.split("(")[1].strip()[:-1]
                dec_concept, dec_name = self._concept_id_name_from_label(vertex.label)
                terms = self._set_qualifier_terms(node[0].ct_subset.terms)
                qualifier[dec_concept] = {"decName": dec_name, "decConceptId": dec_concept,
                                    "conceptualDomainType": "enumerated",
                                    "conceptualDomainName": self.kwargs["test_name"],
                                    "conceptualDomainConceptId": test_name_c_code, "role": vertex.role,
                                    "mandatory": vertex.mandatory,
                                    "terms": terms}
                self._qualifiers.append(qualifier)
                break

    def _set_loinc_code(self, vertex):
        """
        sets the loinc code for findings domain BCs; set to one value for the BC
        :param vertex: node object from the graph created using the CMAP
        """
        for node in vertex.target:
            if node[0].type == "Conceptual Domain":
                qualifier = {}
                self.kwargs["loinc"] = node[0].label.strip()
                dec_concept, dec_name = self._concept_id_name_from_label(vertex.label)
                qualifier[dec_concept] = {"decName": dec_name, "decConceptId": dec_concept,
                                    "conceptualDomainType": "described",
                                    "conceptualDomainName": self.kwargs["loinc"],
                                    "role": vertex.role, "mandatory": vertex.mandatory}
                self._qualifiers.append(qualifier)
                break

    def _set_result(self, vertex):
        """
        sets the result type (e.g. Numeric) for a BC
        :param vertex: node object from the graph created using the CMAP
        """
        for node in vertex.target:
            if node[0].type == "Conceptual Domain":
                qualifier = {}
                self.kwargs["result_type"] = node[0].label
                dec_concept, dec_name = self._concept_id_name_from_label(vertex.label)
                qualifier[dec_concept] = {"decName": dec_name, "decConceptId": dec_concept,
                                    "conceptualDomainType": "described",
                                    "conceptualDomainName": self.kwargs["result_type"],
                                    "role": vertex.role, "mandatory": vertex.mandatory}
                self._qualifiers.append(qualifier)
                break

    def _set_units(self, vertex):
        """
        sets the valid units for a BC measurement
        :param vertex: node object from the graph created using the CMAP
        """
        for node in vertex.target:
            if node[0].type == "Conceptual Domain":
                qualifier = {}
                unit_list = self._set_unit_list(node[0].ct_subset)
                dec_concept, dec_name = self._concept_id_name_from_label(vertex.label)
                qualifier[dec_concept] = {"decName": dec_name, "decConceptId": dec_concept,
                                    "conceptualDomainType": "enumerated",
                                     "conceptualDomainName": node[0].ct_subset.name,
                                     "conceptualDomainConceptId": node[0].ct_subset.c_code,
                                     "role": vertex.role, "mandatory": vertex.mandatory}
                qualifier[dec_concept]["terms"] = unit_list
                self._qualifiers.append(qualifier)
                break

    def _set_unit_list(self, subset):
        """
        builds and sets the valid units for a BC measurement
        :param subset: CT subset object that includes the list of terms
        """
        if subset is None:
            return
        unit_list = []
        for term in subset.terms:
            unit_list.append(term.label)
            if term.is_default:
                self.kwargs["default_unit"] = term.label
        self.kwargs["unit_list"] = unit_list
        return unit_list

    def _get_node_types(self):
        """
        loads the types of nodes that may be included in the graph generated from the CMAP
        """
        for type in self.cfg.node_types:
            self._node_types[type.name] = type.label

    def _set_name_c_code(self, label):
        """
        uses the observation concept, or root node, label from the CMAP graph to set the BC name, label, and c-code
        :param label: label from the root node, the observation concept node, in the CMAP
        """
        self.kwargs["c_code"] = label.split("(")[1].strip()[:-1]
        self.kwargs["name"] = label.split("(")[0].strip().replace(" ", "_").lower()
        self.kwargs["label"] = label.split("(")[0].strip()

    def _concept_id_name_from_label(self, label):
        """
        returns c_code and name as tuple
        :param label: str - cmap node label
        :return: tuple - c_code and name
        """
        return (label.split("(")[1].strip()[:-1], label.split("(")[0].strip().replace(" ", "_").lower())
