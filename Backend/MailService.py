import subprocess
from DataAccess import employeeAccess

class MailService:
    def __init__(self):
        self.service = "smtp.uantwerpen.be"



    def sendSingleMail(self, sender, receiver, subject, message):
        # ja we kunnen de sender en de receiver gebruiken maar dan beginnen we gewoon emails in het rond te sturen wat niet de bedoeling is.
        subprocess.call(["sendemail", "-f", "Freek.DeSagher@student.uantwerpen.be", "-t", "Miguel.Dagrain@student.uantwerpen.be",
                         "-u", subject, "-m", message, "-s", self.service])


    def sendMailExtendingFirst(self):
        eAccess = employeeAccess()

        subject = "verlengen projecten, extending projects"

        message =   "Beste <br><br>" \
                    "Het is bijna weer het nieuwe academiejaar, dus gelieve alle projecten die u wenst te verlengen naar <br>" \
                    "het nieuwe academiejaar aan te duiden op u profiel pagina.<br>" \
                    "link naar u profiel pagina: <br>" \
                    "<a href=''>duid verlengingen aan</a> <br><br>" \
                    "Met vriendelijke groeten <br><br><br><br>" \
                    "Dear <br><br>" \
                    "It is almost the new academic year, so please indicate all projects that you wish to extend to \n" \
                    "the new academic year on your profile page.<br>" \
                    "link to your profile page: <br>" \
                    "<a href=''>indicate extensions</a>> <br><br>" \
                    "kind regards"

        for employee in eAccess.get_employees():
            if employee.getEmpl():
                #opnieuw hier kunnen we gebruik maken van de employee email
                #employee.email



                subprocess.call(["sendemail", "-f", "Freek.DeSagher@studentantwerpen.be", "-t", "Miguel.Dagrain@student.uantwerpen.be",
                                 "-u", subject, "-o", "message-content-type=html", "-m", message, "-s", self.service])


    def sendMailExtendingSecond(self):
        eAccess = employeeAccess()

        subject = "herinnering verlengen projecten, reminder extending projects"

        message =   "Beste <br><br>" \
                    "Zoals al in een eerdere mail gezegd moeten alle promotors aanduiden welke projecten ze wensen te <br>" \
                    "naar het volgende jaar. Indien u dit al heeft gedaan, dan mag u deze mail gerust negeren. <br>" \
                    "Anders wil ik er u nog even op attent maken dat de projecten die niet worden aangeduid om verlengd <br>" \
                    "te worden over 5 dagen op inactief zullen worden gezet. <br>" \
                    "Indien u nog aanpassingen wenst aan te brengen kan dat <a href=''>hier</a>. <br><br>" \
                    "Met vriendelijke groeten <br><br><br><br>" \
                    "Dear <br><br>" \
                    "As already stated in an earlier e-mail, all promoters must indicate which projects they wish to extend <br>" \
                    "to the following year. If you have already done this, you can safely ignore this email. <br>" \
                    "Otherwise I would like to draw your attention to the fact that the projects that are not <br>" \
                    "designated to be extended will be put inactive in 5 days. <br>" \
                    "If you wish to make adjustments, you can do this <a href=''>here</a>. <br><br>" \
                    "Kind regards"

        for employee in eAccess.get_employees():
            if employee.getEmpl():
                #opnieuw hier kunnen we gebruik maken van de employee email
                #employee.email



                subprocess.call(["sendemail", "-f", "Freek.DeSagher@studentantwerpen.be", "-t", "Miguel.Dagrain@student.uantwerpen.be",
                                 "-u", subject, "-o", "message-content-type=html", "-m", message, "-s", self.service])