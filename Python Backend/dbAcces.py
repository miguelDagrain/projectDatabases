from dbDocument import *
class dbAcces:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_Document(self):
        cursor=self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document')
        documents=list()
        print("hello world")
        for row in cursor:
            document=dbDocument(row[0])
            documents.append(document)
        return documents
        # cursor = self.dbconnect.get_cursor()
        # cursor.execute('SELECT id, text, author FROM Quote')
        # quote_objects = list()
        # for row in cursor:
        #     quote_obj = Quote(row[0], row[1], row[2])
        #     quote_objects.append(quote_obj)
        # return quote_objects

    def get_quote(self, iden):
        return 0
        # cursor = self.dbconnect.get_cursor()
        # # See also SO: https://stackoverflow.com/questions/45128902/psycopg2-and-sql-injection-security
        # cursor.execute('SELECT id, text, author FROM Quote WHERE id=%s', (iden,))
        # row = cursor.fetchone()
        # return Quote(row[0], row[1], row[2])

    def add_quote(self, quote_obj):
        return 0
        # cursor = self.dbconnect.get_cursor()
        # try:
        #     cursor.execute('INSERT INTO Quote(text,author) VALUES(%s,%s)', (quote_obj.text, quote_obj.author,))
        #     # get id and return updated object
        #     cursor.execute('SELECT LASTVAL()')
        #     iden = cursor.fetchone()[0]
        #     quote_obj.id = iden
        #     self.dbconnect.commit()
        #     return quote_obj
        # except:
        #     self.dbconnect.rollback()
        #     raise Exception('Unable to save quote!')
