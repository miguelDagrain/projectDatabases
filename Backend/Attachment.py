class Attachment:
    def __init__(self, docid, content):
        self.docid = docid
        self.content = content

    def get_document(self, connect):
        access = __import__('DataAccess', fromlist=['DocumentAccess'])
        da = access.DocumentAccess(connect)
        return da.get_document(self.docid)
