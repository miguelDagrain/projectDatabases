import unittest
import dbConnection

from Attachment import Attachment
from Bookmark import Bookmark
from Employee import Employee

class TestClass(unittest.TestCase):
    def setUp(self):
        from dbConnection import setConnection
        from config import config_data

        # setting up the database connection
        ip = config_data['ip']
        port = config_data['port']
        setConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                      dbhost=config_data['dbhost'])



    def test_Attachment(self):
        from DataAccess.documentAccess import DocumentAccess

        content = "./Attachment.py"  # We voegen voor de test deze file toe als attachment

        att = Attachment(1, content)

        # normaal gezien gebeurt dit via app maar deze test is enkel voor deze file
        da = DocumentAccess()
        da.add_attachment(1,
                          content)  # we voegen de attachment toe in de database, we schrijven hier content omdat dit in de database zelf is

        assert att.get_document().attachment[0].content == da.get_document(1).attachment[0].content

        # we willen in de app zelf niet kunnen verwijderen maar we willen geen testresultaten in de database
        cursor = dbConnection.connection.get_cursor()
        cursor.execute('delete from attachment where doc=%s and attachment=%s',
                       (1, content))
        dbConnection.connection.commit()

    def test_Bookmark(self):
        from DataAccess.projectAccess import ProjectAccess
        from DataAccess.studentAccess import StudentAccess

        bkm = Bookmark(1, 1)  # het 2de project en de 2de student

        pro = ProjectAccess()
        assert bkm.getProject().title == pro.get_project(1).title
        stu = StudentAccess()
        assert bkm.getStudent().name == stu.get_student(1).name

        # we hebben hier niets gewijzigd aan de database en moeten dus ook niets verwijderen

    def test_Employee(self):
        from DataAccess.employeeAccess import EmployeeAccess
        from DataAccess.researchGroupAccess import ResearchGroupAccess

        res = ResearchGroupAccess()

        emp = EmployeeAccess()

        doe = Employee(None, "John Doe", "John.Doe@uantwerpen.be", None, 2, None, None, None, False)

        emp.add_employee(doe)

        assert doe.getEmpl().email == emp.get_employee(doe.id).email
        assert doe.getProjects() == emp.get_employeeProjects(doe.id)
        assert doe.getResearchGroup().name == res.get_singleResearchGroupOnID(2).name

        # herstel de database
        emp.remove_employee(emp.get_employeeOnName("John Doe").id)


if __name__ == '__main__':
    unittest.main()