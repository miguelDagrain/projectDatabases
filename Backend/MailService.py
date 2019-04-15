import subprocess

class MailService:
    def __init__(self):
        service = "smtp.uantwerpen.be"



    def sendSingleMail(self, sender, receiver, subject, message):
        # ja we kunnen de sender en de receiver gebruiken maar dan beginnen we gewoon emails in het rond te sturen wat niet de bedoeling is.
        subprocess.call(["sendemail", "-f", "Freek.DeSagher@student.uantwerpen.be", "-t","Miguel.Dagrain@student.uantwerpen.be",
                         "-u", subject, "-m", message, "-s", self.service])