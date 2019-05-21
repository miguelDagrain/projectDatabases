
from App.all import *
from TagCalculator import findTags

if __name__ == "__main__":
    if config_data['calc_tags']:
        findTags()
    # mailer = MailService()
    #
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(mailer.sendMailExtendingFirst(),trigger='cron', minute='0', hour='0', day='10', month='9', year='*')
    # scheduler.add_job(mailer.sendMailExtendingSecond(), trigger='cron', minute='0', hour='0', day='20', month='9',year='*')
    # scheduler.add_job(deactivate_projects(), trigger='cron', minute='0', hour='0', day='25', month='9',year='*')
    app.run(debug=config_data['debug'], host=ip, port=port)
