
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage




# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Toolkiit'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_post_from_google():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1tVFfZdv2OdfA5MKwNGqtM8gjzzbzpFGiZYnzbQ-tcKo'
    index_rangeName = 'Final Data!I1:I1'

    index_result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=index_rangeName).execute()
    index_value = index_result.get('values')[0][0]

    if not index_value:
        print('No index value found.')
    else:
        post_rangeName = 'Final Data!B' + index_value +':G' + index_value
        post_result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=post_rangeName).execute()
        post_value = post_result.get('values')
        if not post_value:
            print('No post value found.')
        else:
            accessor_output = {
                'to_field_sheet' : post_value[0][0]
                , 'do_field_sheet' : post_value[0][1]
                , 'person_sheet' : post_value[0][2]
                , 'summary_sheet' : post_value[0][3]
                , 'source_url_sheet' : post_value[0][4]
                , 'author_sheet' : post_value[0][5]
                }
            return accessor_output


# User.objects.all().last().email 
if __name__ == "__main__":
    get_post_from_google()
