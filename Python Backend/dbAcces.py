from dbDocument import *
from dbResearchGroup import *
from dbEmployee import *
from dbProject import *
from dbProjectRegistration import *
from dbSession import *
from dbStudent import *

class dbAcces:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_Document(self):
        cursor=self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document')
        documents=list()
        for row in cursor:
            document=dbDocument(row[0])
            documents.append(document)
        return documents

    def add_document(self, doc):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO document VALUES(%s)', (doc.text,))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save document!')

    def get_researchGroup(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from researchGroup')
        rgroups=list()
        for row in cursor:
            rgroup=dbResearchGroup(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
            rgroups.append(rgroup)
        return rgroups

    def add_researchGroup(self,group):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO researchGroup values(%s,%s,%s,%s,%s,%s,%s,)',
                           (group.name,group.abbreviation,group.discipline,"B'"+str(int(group.active))+"'",group.adress,group.telNr,group.groupDescription,))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save quote!')
