from App.all import *
from TagCalculator import findTags

# nodig voor scheduling mails en automatisch verwijderen projecten

from apscheduler.schedulers.background import BackgroundScheduler
# from MailService import MailService

def deactivate_projects():
    Paccess = ProjectAccess()

    projects = Paccess.get_projects()

    #maak alle projecten inactief
    for i in projects:
        if i.active:
            Paccess.change_project_active(i.ID, True)

    #selecteer de projecten die dit jaar moeten geheractiveerd worden
    projectsIdReactivate = Paccess.get_id_projects_reactivate()

    for i in projectsIdReactivate:
        Paccess.change_project_active(i, False)

    #reset het reactiveringboolean van alle projecten
    Paccess.reset_projects_reactivate()


if __name__ == "__main__":
    if config_data['calc_tags']:
        findTags()
    mailer = MailService()

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(mailer.sendMailExtendingFirst,trigger='cron', minute='0', hour='0', day='10', month='9', year='*')
    # scheduler.add_job(mailer.sendMailExtendingSecond, trigger='cron', minute='0', hour='0', day='20', month='9',year='*')
    # scheduler.add_job(deactivate_projects, trigger='cron', minute='0', hour='0', day='25', month='9',year='*')
    # scheduler.add_job(deactivate_projects, trigger='cron', minute='*/1')
    # scheduler.start()
    app.run(debug=config_data['debug'], host=ip, port=port)
