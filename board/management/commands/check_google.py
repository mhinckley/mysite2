from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from libs import google_sheet_accessor
from board import models as board_models

# See here for example https://github.com/jessamynsmith/analysocial/blob/master/graph/management/commands/email_login_reminder.py

class Command(BaseCommand):
    help = "Check Google Sheet for new Post data and add to local database"

    def handle(self, *args, **options):
        spreadsheetId = '1tVFfZdv2OdfA5MKwNGqtM8gjzzbzpFGiZYnzbQ-tcKo'
        # TODO need a mechanism for retrieving multiple rows
        # Will need to check for any new rows and add them to database
        # Best option is probably to add a unique ID to each row in the google doc
        # That Google ID can be stored in the Post model in the Django DB
        # You probably need to loop over the rows in the google doc until you reach one
        # you have already stored (if you keep them in order from newest to oldest,
        # this will work)
        data = google_sheet_accessor.get_post_from_google(spreadsheetId)

        for row_data in range(0, len(data)):
            google_id = data[row_data]['google_id_sheet']
            current_post_len = len(board_models.Post.objects.filter(google_id=google_id))
            if current_post_len == 1:
                # post already exists in the model
                break
            else:
                # will be called if post isn't already in the model 
                post = board_models.Post()
                # Map google data fields to Post object
                post.to_field = data[row_data]['to_field_sheet']
                post.do_field = data[row_data]['do_field_sheet']
                post.person = data[row_data]['person_sheet']
                post.summary = data[row_data]['summary_sheet']
                post.source_url = data[row_data]['source_url_sheet']
                post.google_id = int(data[row_data]['google_id_sheet'])
                email_address = data[row_data]['author_sheet']
                # TODO What happens if there is no user with that email?
                post.author = User.objects.filter(email=email_address).first()
                if post.to_field and post.do_field:
                    post.save() # only save if has values in to and do fields
        