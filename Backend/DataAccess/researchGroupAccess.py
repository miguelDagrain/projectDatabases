import dbConnection

from documentAccess import DocumentAccess

class ResearchGroupAccess:
    def __init__(self):
        """
        creates a researchGroup object
        """
        self.dbconnect = dbConnection.connection
        self.doc = DocumentAccess()

    def get_researchgroupDescriptions(self, groupid):
        """
        gets all descriptions of a researchgroup out of the database
        :param groupid: the id of the researchgroup
        :return: a list of descriptions
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from groupDescription where groupID=%s', (groupid,))
        desc = list()
        for row in cursor:
            desc.append(self.doc.get_document(row[1]))
        return desc

    def add_researchGroupDescription(self, document, groupid):
        """
        adds a new researchgroupDescription to the database
        :param document: the description you are adding
        :param groupid: the id of the researchgroup you are adding it to
        """
        cursor = self.dbconnect.get_cursor()
        try:
            docid = self.doc.add_document(document)
            cursor.execute('INSERT INTO groupDescription values(%s,%s)',
                           (groupid, docid))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroupdescription!')

    def get_researchGroups(self):
        """
        gets all researchgroups out of the database
        :return: a list of researchgroups
        """
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from researchGroup')
        rgroups = list()
        for row in cursor:
            rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
            rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
            newcursor = self.dbconnect.get_cursor()
            newcursor.execute('select * from contactPerson where rgroup=%s', (rgroup.ID,))
            if newcursor.rowcount > 0:
                rgroup.contactID = newcursor.fetchone()[0]
            rgroups.append(rgroup)
        return rgroups

    def get_researchGroupOnName(self, name):
        """
        gets a researchgroups based of a name
        :param name: the name of said researchgroup
        :return: a researchgroup object
        """
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGroup WHERE name=%s', (name,))
        row = cursor.fetchone()
        rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        cursor.execute('select * from contactPerson where rgroup=%s', (rgroup.ID,))
        if cursor.rowcount > 0:
            rgroup.contactID = cursor.fetchone()[0]
        return rgroup

    def get_researchGroupsOnIDs(self, ids):
        """
        gets a researchgroup from teh database based on an id
        :param id: the id
        :return: a researchgroup object
        """
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()

        rgroups = list()

        for id in ids:
            cursor.execute('SELECT * FROM researchGroup WHERE groupID=%s', (id,))
            row = cursor.fetchone()
            rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
            rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
            cursor.execute('select * from contactPerson where rgroup=%s', (rgroup.ID,))
            if cursor.rowcount > 0:
                rgroup.contactID = cursor.fetchone()[0]
            rgroups.append(rgroup)

        return rgroups

    def get_singleResearchGroupOnID(self, id):
        """

        :param id:
        :return:
        """
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGroup WHERE groupID=%s', (id,))
        row = cursor.fetchone()
        rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        cursor.execute('select * from contactPerson where rgroup=%s', (rgroup.ID,))
        if cursor.rowcount > 0:
            rgroup.contactID = cursor.fetchone()[0]
        return rgroup

    def remove_researchGroup(self, id):
        """
        removes a researchgroup from the database based on an id
        :param id: the id
        """

        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM researchGroup WHERE groupID=%s', (id,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to remove researchgroup')

    def changeContactPerson(self, eid, groupID):
        """
        changes a contact person for a researchgroup
        :param eid: the new employee that will become the contactperson
        :param groupID: the researchgroup id
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('SELECT * FROM contactPerson WHERE rgroup=%s', (groupID,))
            if cursor.rowcount == 0:
                cursor.execute('insert into contactperson values(%s,%s)', (eid, groupID))
            else:
                if (cursor.fetchone()[0] != eid):
                    # waarom zegt pycharm hier constant dat hem '=' verwacht terwijl dat er staat ???
                    cursor.execute('update contactPerson set employee= %s where rgroup=%s', (eid, groupID))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to check contactperson !')

    def add_researchGroup(self, group):
        """
        adds a new researchgroup to the database
        :param group: the new resrachgroup (without an id)
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO researchGroup values(default ,%s,%s,%s,%s,%s,%s)',
                           (group.name, group.abbreviation, group.discipline, group.active, group.address,
                            str(group.telNr)))
            cursor.execute('SELECT LASTVAL()')
            gid = cursor.fetchone()[0]
            group.ID = gid
            if group.contactID != None:
                self.checkContactPerson(group.contactId, group.ID)
            for i in group.desc:
                self.add_researchGroupDescription(i, gid)
            self.dbconnect.commit()
        except Exception as e:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroup!'+str(e))

    def change_researchGroup(self, group):
        """
        changes a researchgroup in the database
        :param group: the researchgroup that it will be changed into
        """
        cursor = self.dbconnect.get_cursor()
        try:
            if group.ID is None:
                raise Exception('no id given')
            cursor.execute('select * from researchgroup where groupID=%s', (group.ID,))
            if cursor.rowcount == 0:
                raise Exception('no researchGroup found with that id')
            cursor.execute(
                'update researchGroup set name= %s,abbreviation= %s,discipline= %s,active= %s,address= %s,telNr= %s where groupId=%s',
                (group.name, group.abbreviation, group.discipline, group.active, group.address, str(group.telNr),
                str(group.ID)))
            cursor.execute('delete from groupDescription where groupID=%s', (group.ID,))
            for i in group.desc:
                self.add_researchGroupDescription(i, str(group.ID))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change researchGroup')
