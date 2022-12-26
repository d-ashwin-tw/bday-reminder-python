# setting django environment
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "birthday_reminder.settings")
import django
django.setup()

from datetime import date
from pytz import timezone
from apps.gateway import gateway_email
from apps.auth_manager.models import Developer
from apps.auth_manager.common_helper import response_data
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()



# Triggered every day 24 hours
@sched.scheduled_job("interval", hours=24)
def anniversary():
    print('This job is run every one minutes.')
    try:    
        dev = Developer.objects.all()
        for data in dev:
            name = data.account.user.username
            today = date.today()
            today_date = today.strftime("%m-%d")
            join_date = data.doj.strftime("%m-%d")
            if today_date == join_date:
                to_emails = data.account.user.email
                from_email = "ashwin@thoughtwin.com"
                extra_params = {}
                extra_params["name"] = name
                gateway_email.send_email(
                    from_email=from_email,
                    to_emails=[to_emails],
                    template_name="happy work anniversary",
                    extra_params=extra_params,
                )
    except Exception as e:
        print(e)
        

@sched.scheduled_job("interval", hours=24)
def mensday():
    try:
        developer = Developer.objects.filter(gender="M")
        for data in developer:
            name = data.account.user.username
            today = date.today()
            today_date = today.strftime("%m-%d")
            # join_date = data.doj.strftime("%m-%d")
            mens_day = "11-19"
            if today_date == mens_day:
                to_emails = data.account.user.email
                from_email = "ashwin@thoughtwin.com"
                extra_params = {}
                extra_params["name"] = name
                gateway_email.send_email(
                    from_email=from_email,
                    to_emails=[to_emails],
                    template_name="Men's Day",
                    extra_params=extra_params,
                )
    except Exception as e:
        print(e)
    # Celery recognizes this as the `movies.tasks.add` task


# the name is purposefully omitted here.


@sched.scheduled_job("interval", hours=24)
def womensday():
    try:
        developer = Developer.objects.filter(gender="F")
        for data in developer:
            name = data.account.user.username
            today = date.today()
            today_date = today.strftime("%m-%d")
            # join_date = data.doj.strftime("%m-%d")
            womens_day = "03-08"
            if today_date == womens_day:
                to_emails = data.account.user.email
                from_email = "ashwin@thoughtwin.com"
                extra_params = {}
                extra_params["name"] = name
                gateway_email.send_email(
                    from_email=from_email,
                    to_emails=[to_emails],
                    template_name="Women's Day",
                    extra_params=extra_params,
                )
    except Exception as e:
        print(e)


sched.start()
