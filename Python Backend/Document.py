class Document:
    def __init__(self,id, text):
        """
        constructor for dbdocument with text given
        :param text: the text that is contained in the document
        :return: a new dbDocument object
        """
        self.ID=id
        self.text = text


    def __str__(self):
        return "id"+self.ID+", content:"+self.text
