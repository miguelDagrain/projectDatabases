import dbConnection

class DocumentAccess:
    def __init__(self):
        """
        basic initialiser for a documentAcces
        :param dbconnect:
        """
        self.dbconnect = dbConnection.connection

    def update_document_text(self, documentID, newText):
        cursor = self.dbconnect.get_cursor()
        sql = 'UPDATE document SET content= %s WHERE documentid = %s'
        try:
            cursor.execute(sql, (str(newText), str(documentID)))
            self.dbconnect.commit()
            return True
        except:
            self.dbconnect.rollback()
            return False

    def get_documents(self):
        """
        gets all documents from the connected database
        :return: a list of documents
        """
        from Document import Document
        from Attachment import Attachment
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document')
        documents = list()
        for row in cursor:
            document = Document(row[0], row[1], row[2])
            cursorAttachment = self.dbconnect.get_cursor()
            cursorAttachment.execute('select * from attachment where %s=doc', (document.ID,))
            for att in cursorAttachment:
                document.attachment.append(Attachment(att[0], att[1]))
            documents.append(document)
        return documents

    def get_document(self, id):
        """
        gets a single document on a given id
        :param id: an id (will be casted to string)
        :return: a single doucment
        """
        from Document import Document
        from Attachment import Attachment
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document WHERE documentID=%s', (id,))
        row = cursor.fetchone()
        document = Document(row[0], row[1], row[2])
        cursorAttachment = self.dbconnect.get_cursor()
        cursorAttachment.execute('select * from attachment where doc=%s', (document.ID,))
        for att in cursorAttachment:
            document.attachment.append(Attachment(att[0], att[1]))
        return document

    def add_attachment(self, documentID, attachment):
        """
        adds a new attachment to the database an couples it with a document
        :param documentID: the doucment id (will be casted to a string)
        :param attachment: the attachment
        """
        try:
            cursor = self.dbconnect.get_cursor()
            cursor.execute('select * from attachment where doc=%s and attachment=%s',
                           (documentID, attachment))
            if cursor.rowcount == 0:
                cursor.execute('insert into attachment values(%s,%s)', (documentID, str(attachment)))
                self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save attachment!')

    # returns the document id of the added document
    def add_document(self, doc):
        """
        adds a document to the database and sets the id of the given document to the new one in the database
        :param doc: the document you are about to add (should not have an id)
        """
        cursor = self.dbconnect.get_cursor()
        try:
            id = int()
            if doc.ID is None or doc.ID == -1:
                cursor.execute('INSERT INTO document VALUES(default ,%s,%s)', (doc.language, str(doc.text)))
                cursor.execute('SELECT LASTVAL()')
                id = cursor.fetchone()[0]
                doc.ID = id
                for att in doc.attachment:
                    self.add_attachment(id, att)
            # get id and return updated object
            self.dbconnect.commit()
            return id
        except (Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('Unable to save document!%s' % error)

    def change_Document(self, document):
        """
        changes the doucment that is currcently already in the database
        :param document: a document with an id that is already in the database
        """
        try:
            if document.ID is not None:
                cursor = self.dbconnect.get_cursor()
                cursor.execute('select * from document where documentID=%s', (document.ID,))
                if cursor.rowcount == 0:
                    raise Exception('no document with that ID found')
                cursor.execute('update document set lang= %s, content= %s where documentID=%s',
                               (document.language, document.text, document.ID))

                cursor.execute('delete from attachment where doc=%s', (document.ID,))
                for i in document.attachment:
                    self.add_attachment(document.ID, i.content)
                self.dbconnect.commit()

            else:
                raise Exception('Document doesnt have ID')
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to change document!')
