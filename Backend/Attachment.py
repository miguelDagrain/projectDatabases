class Attachment:
    #Voor alle duidelijkheid content verwijst hier naar de naam van de file die attached is. niet naar een tekst in de vorm van een string
    def __init__(self, docid, content):
        self.docid = docid
        self.content = content

    def get_document(self):
        from DataAccess.documentAccess import DocumentAccess
        da = DocumentAccess()
        return da.get_document(self.docid)
