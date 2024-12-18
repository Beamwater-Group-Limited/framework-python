class GstreamerSentenceInputEntity:
    def __init__(self, element: str, element_property: str):
        self.element = element
        self.element_property = element_property
        self.single_sentence = ""

    def get_single_sentence(self):
        """拼接元素和对应的参数和值"""
        self.single_sentence = self.element + " " + self.element_property
        return self.single_sentence
