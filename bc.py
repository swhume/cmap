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
import json


class BiomedicalConcept:
    def __init__(self, **kwargs):
        """
        constructor initializing the BC attributes
        :param kwargs: the BC attributes as a dictionary
        """
        self.designation = kwargs.get("name", "")
        self.conceptId = kwargs.get("c_code", "")
        self.label = kwargs.get("label", "")
        self.definition = kwargs.get("definition", "")
        self.testCode = kwargs.get("test_cd", "")
        self.testConceptId = kwargs.get("test_c_code", "")
        self.testName = kwargs.get("test_name", "")
        self.loincCode = kwargs.get("loinc", "")
        self.resultType = kwargs.get("result_type", "")
        self.unitList = kwargs.get("unit_list", [])
        self.defaultUnit = kwargs.get("default_unit", "")
        self.standardUnit = kwargs.get("standard_unit", [])
        self.dataElementConcepts = kwargs.get("dataElementConcepts", {})
        self._links = {}
        # properties below are not included in the BC output
        self.ct_subsets = []

    def add_ct_subsets(self, subset):
        """
        append a CT subset object to the BC
        :param subset: an object representing an CT subset found in the CMAP graph
        """
        self.ct_subsets.append(subset)

    def serialize_json(self):
        """
        serialize the current BC object as JSON
        :return: JSON serialization of the BC object
        """
        bc_dict = self.__dict__
        bc_dict.pop("ct_subsets")
        return json.dumps(bc_dict)
