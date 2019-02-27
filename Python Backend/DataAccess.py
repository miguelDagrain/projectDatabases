from Document import *
from ResearchGroup import *


class DataAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_document(self):
        cursor=self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document')
        documents=list()
        for row in cursor:
            document=Document(row[0])
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
            rgroup=ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            rgroups.append(rgroup)
        return rgroups

    def add_researchGroup(self,group):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO researchGroup values(%s,%s,%s,%s,%s,%s,%s)',
                           (group.name,group.abbreviation,group.discipline,group.active,group.adress,group.telNr,group.groupDescription))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save document!')


    def get_employee(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from employee')
        employees= list()
        for row in cursor:
            employee = dbEmployee(row[0], row[1], row[2], row[3], row[4], row[5])
            employees.append(employee)
        return employees

    def add_employee(self,empl):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO employee values(%s,%s,%s,%s,%s,%s)',
                           (empl.email,empl.office,empl.researchGruoup,empl.title,empl.internOrExtern,empl.active))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save Employee!')