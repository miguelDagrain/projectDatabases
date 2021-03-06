class ResearchGroup:
    def __init__(self, id, name, abbreviation, discipline, active, address, telephone, desc):
        """
        constructor for a dbResearchGroup
        :param name: a string representing a name for the researchGroup
        :param abbreviation: a string that is an abbreviation for the researchgorup
        :param discipline: a subject Enum that says which discipline this group belongs to
        :param active: a bool saying if the group is active or not
        :param address: a string that is an adress for the group
        :param telephone: a string that is the phone number for the group
        :param desc: an all the documents that are this groups descriptions
        :return:a new dbResearchGroup object
        """
        self.ID = id
        self.name = name
        self.abbreviation = abbreviation
        self.discipline = discipline
        self.active = active
        self.address = address
        self.telNr = telephone
        self.desc = desc
        self.contactID = None
