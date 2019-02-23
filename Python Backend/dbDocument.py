class dbDocument:
    m_text = None

    def dbDocument(self, text=""):
        """
        constructor for dbdocument with text given
        :param text: the text that is contained in the document
        :return: a new dbDocument object
        """
        self.m_text = text
