import dbConnection


class DomainAccess:
    def __init__(self):
        """
        constructor for a domainAccess object
        """
        self.dbconnect = dbConnection.connection

    def add_discipline(self, discipline):
        """
        adds a discipline to the list of disciplines
        :param discipline: the new discipline
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("INSERT INTO discipline (subject, active) VALUES (%s, 'true')", (discipline,))
            self.dbconnect.commit()

        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to add discipline!\n(%s)' % (error))

    def reactivate_discipline(self, discipline):
        """
        adds a discipline to the list of disciplines
        :param discipline: the new discipline
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("UPDATE discipline SET active = 'true' WHERE subject = %s", (discipline,))
            self.dbconnect.commit()


        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to re-add discipline!\n(%s)' % (error))

    def remove_discipline(self, discipline):
        """
        removes a discipline
        :param discipline:
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("UPDATE discipline set active = 'false' WHERE subject = %s", (discipline,))
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to remove discipline!:\n(%s)' % (error))

    def remove_type(self, type):
        """
        removes a discipline
        :param discipline:
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("UPDATE projecttype set active = 'false' WHERE type = %s", (type,))
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to remove type!:\n(%s)' % (error))

    def get_disciplines(self):
        """
        gets all disciplines
        :return: a list of disciplines
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from discipline')
        disciplines = list()
        for row in cursor:
            if row[1] == 'true':
                disciplines.append(row[0])
        return disciplines

    def get_disciplinesWithActivity(self):
        """
        gets all disciplines
        :return: a list of disciplines
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from discipline')
        disciplines = list()
        for row in cursor:
            if row[1] == 'true':
                disciplines.append((row[0],row[1]))
        return disciplines

    def get_alldisciplines(self):
        """
        gets all disciplines
        :return: a list of disciplines
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from discipline')
        disciplines = list()
        for row in cursor:
            disciplines.append(row[0])
        return disciplines

    def add_title(self, title):
        """
        adds a title to the list of titles
        :param title:
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO title values(%s)', (title,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add title!')

    def get_titles(self):
        """
        gets all titles out of the database
        :return: a list of titles
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from title')
        titles = list()
        for row in cursor:
            titles.append(row[0])
        return titles

    def add_intextOrigin(self, origin):
        """
        adds a new intextOrigin to the database
        :param origin: the new thing
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO INTEXT values(%s)', (origin,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add intext origin!')

    def get_intextOrigin(self):
        """
        gets all intextorigins out of the database
        :return: a list of origins (intern, extern, etc
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from INTEXT')
        origins = list()
        for row in cursor:
            origins.append(row[0])
        return origins

    def add_registrationStatus(self, status):
        """
        adds a new refistration status to the list
        :param status: the new status
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO registration values(%s)', (status,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add registration status!')

    def get_registrationStatus(self):
        """
        gets all registrationStatusses
        :return: a list of statusses
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from registration')
        status = list()
        for row in cursor:
            status.append(row[0])
        return status

    def add_language(self, lang):
        """
        adds a new language to the list of languages
        :param lang: the new language
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO language values(%s)', (lang,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add language!')

    def get_languages(self):
        """
        gets all languages out of the database
        :return: a list of languages
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from language')
        langs = list()
        for row in cursor:
            langs.append(row[0])
        return langs

    def add_projectType(self, type):
        """
        adds a new projectType to the database
        :param type: the new type
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("INSERT INTO projectType (type, active) VALUES (%s, 'true')", (type,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add projectType!')

    def reactivate_projectType(self, type):
        """
        adds a new projectType to the database
        :param type: the new type
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("UPDATE projectType SET active = 'true' WHERE type = %s", (type,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add projectType!')

    def get_projectType(self):
        """
        gets all projectTyppes out of the database
        :return: a list of projecTypes
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectType ')
        types = list()
        for row in cursor:
            if row[1] == 'true':
                types.append(row[0])
        return types

    def get_allprojectType(self):
        """
        gets all projectTyppes out of the database
        :return: a list of projecTypes
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectType ')
        types = list()
        for row in cursor:
           types.append(row[0])
        return types
