from dateutil.relativedelta import relativedelta
from smtplib import SMTPDataError

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models import Post, Follow 

from libs import email_sender, helpers

# See here for example https://github.com/jessamynsmith/analysocial/blob/master/graph/management/commands/email_login_reminder.py

class Command(BaseCommand):
    help = "Reminder users of the posts they wanted to be reminded of"

    def handle(self, *args, **options):

        # Get all users with daily subscriptions                
        users_daily = User.objects.filter(follow__frequency=1)
        
        # Get list of posts each user is subscribed to on a daily basis  
        for user in users_daily:
            context = {
                'admin_name': settings.ADMINS[0][0],
                'user_name': user.username,
                'full_domain': helpers.get_full_domain(),
                'daily_follows': user.follow_set.filter(frequency=1)
            }
            template_name = 'daily_post_reminder'
            subject = "Daily reminder to use these tools"
            plaintext = get_template('email/%s.txt' % template_name)
            html = get_template('email/%s.html' % template_name)

            try:
                email_sender.send(user, subject, plaintext.render(context),
                                  html.render(context))
            except SMTPDataError as e:
                print(e)