from dateutil.relativedelta import relativedelta
from datetime import datetime, date, time
from smtplib import SMTPDataError

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.utils import timezone

from django.contrib.auth.models import User

from libs import email_sender, helpers

# See here for example https://github.com/jessamynsmith/analysocial/blob/master/graph/management/commands/email_login_reminder.py

class Command(BaseCommand):
    help = "Reminder users of the posts they wanted to be reminded of"

    def handle(self, *args, **options):
        now = datetime.now()
        
        # Get all users with monthly subscriptions                
        users_daily = User.objects.filter(follow__frequency=1).distinct()
        users_weekly = User.objects.filter(follow__frequency=3).distinct()
        users_monthly = User.objects.filter(follow__frequency=6).distinct()
        
        # Send monthly email
        if now.day == 1:            
        # Get list of posts each user is subscribed to on a monthly basis  
            for user in users_monthly:
                context = {
                    'admin_name': settings.ADMINS[0][0],
                    'user_name': str(user.username),
                    'full_domain': helpers.get_full_domain(),
                    'follows': user.follow_set.filter(frequency=6),
                    'frequency': 'month'
                }
                template_name = 'post_reminder'
                subject = "Here are your Monthly Tools"
                plaintext = get_template('email/%s.txt' % template_name)
                html = get_template('email/%s.html' % template_name)

                try:
                    email_sender.send(user, subject, plaintext.render(context),
                                      html.render(context))
                except SMTPDataError as e:
                    print(e)
        
        # Send weekly email on Sunday
        if now.weekday() == 7:            
        # Get list of posts each user is subscribed to on a weekly basis  
            for user in users_weekly:
                context = {
                    'admin_name': settings.ADMINS[0][0],
                    'user_name': str(user.username),
                    'full_domain': helpers.get_full_domain(),
                    'follows': user.follow_set.filter(frequency=3),
                    'frequency': 'week'
                }
                template_name = 'post_reminder'
                subject = "Here are your Weekly Tools"
                plaintext = get_template('email/%s.txt' % template_name)
                html = get_template('email/%s.html' % template_name)

                try:
                    email_sender.send(user, subject, plaintext.render(context),
                                      html.render(context))
                except SMTPDataError as e:
                    print(e)

        # Send daily email everyday
        # Get list of posts each user is subscribed to on a daily basis  
        for user in users_daily:
            context = {
                'admin_name': settings.ADMINS[0][0],
                'user_name': str(user.username),
                'full_domain': helpers.get_full_domain(),
                'follows': user.follow_set.filter(frequency=1),
                'frequency': 'day'
            }
            template_name = 'post_reminder'
            subject = "Here are your Daily Tools"
            plaintext = get_template('email/%s.txt' % template_name)
            html = get_template('email/%s.html' % template_name)

            try:
                email_sender.send(user, subject, plaintext.render(context),
                                  html.render(context))
            except SMTPDataError as e:
                print(e)
        
        