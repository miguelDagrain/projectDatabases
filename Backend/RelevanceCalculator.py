from DataAccess import *

class RelevanceCalculator():
    """
    this class will be used to calculate the relevance of a project for a student based on the previously clicked projects
    """
    def __init__(self,studentID):
        """
        the init function also calls onto the calculateTagValues which
        :param studentID:
        """
        self.tagValues = dict()
        self.student=studentID
        self.calculateTagValues()

    def calculateTagValues(self):
        sa = SessionAccess()
        pa=ProjectAccess()
        projs = sa.get_StudentProjectClicks(self.student)
        for proj in projs:
            project=pa.get_project(proj)
            for i in project.tag:
                splittedtag=i.split('_')
                for singleTag in splittedtag:
                    if singleTag in self.tagValues:
                        self.tagValues[singleTag]=self.tagValues[singleTag]+1
                    else:
                        self.tagValues[singleTag]=1
    def calculateProjectWeighting(self,projectTags):
        weighting=0
        for i in projectTags:
            splittedtag = i[0].split('_')
            for singleTag in splittedtag:
                if singleTag in self.tagValues:
                    weighting+=self.tagValues[singleTag]
        return weighting
