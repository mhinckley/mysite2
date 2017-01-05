
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#     print(type(flags))
#     print(flags)
# except ImportError:
#     flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = os.path.join(os.getcwd(), 'libs', 'client_secret.json')
APPLICATION_NAME = 'Toolkiit'


# Hack up a class to handle the required  flags to oauth flow
"""
usage: manage.py [-h] [--auth_host_name AUTH_HOST_NAME]
                 [--noauth_local_webserver]
                 [--auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]]
                 [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
"""
class FlowFlags(object):
    noauth_local_webserver = None
    auth_host_name = ''
    auth_host_port = ''
    logging_level = 'DEBUG'


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
    #if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    flags = FlowFlags()
    #if flags:
    #credentials = tools.run_flow(flow, store, flags)
    credentials = tools.run_flow(flow, store, flags)
    #else: # Needed only for compatibility with Python 2.6
    #    credentials = tools.run(flow, store)
    print('Storing credentials to ' + credential_path)
    return credentials


def get_post_from_google(spreadsheetId):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    print(credentials.get_access_token())
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    index_rangeName = 'Final Data!J1:J1'

    index_result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=index_rangeName).execute()
    index_value = index_result.get('values')[0][0]

    ascending_accessor_output = []
    descending_accessor_output = []

    if not index_value:
        print('No index value found.')
    else:
        for row_value in range(2, int(index_value)+1):  #start at second row because there are column headers in row 1
            row_value = str(row_value)
            post_rangeName = 'Final Data!B' + row_value +':H' + row_value
            post_result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=post_rangeName).execute()
            post_value = post_result.get('values')
            if not post_value:
                print('No post value found in', row_value)
            else:
                row_output = {
                    'to_field_sheet' : post_value[0][0]
                    , 'do_field_sheet' : post_value[0][1]
                    , 'person_sheet' : post_value[0][2]
                    , 'summary_sheet' : post_value[0][3]
                    , 'source_url_sheet' : post_value[0][4]
                    , 'author_sheet' : post_value[0][5]
                    , 'google_id_sheet' : post_value[0][6]
                    }
                ascending_accessor_output.append(row_output)
        descending_accessor_output = ascending_accessor_output[::-1]       
        return descending_accessor_output

if __name__ == "__main__":
    spreadsheetId = '1tVFfZdv2OdfA5MKwNGqtM8gjzzbzpFGiZYnzbQ-tcKo'
    get_post_from_google(spreadsheetId)



"""
# Setting up a push notification instead of pull notification above. Reading API.

https://www.googleapis.com/drive/v3/files/1tVFfZdv2OdfA5MKwNGqtM8gjzzbzpFGiZYnzbQ-tcKo/watch
https://www.googleapis.com/drive/v3/changes/watch
u'ya29.CjDBAxLLuevljX0nz-0Z-D1S_2CgDMCj4CsOEhzY9q3Y0DG5Y10oLuRBV41COsMmB1s'

# Curl hits urls in the terminal
 
curl -v -k -X POST -H "Content-Type: application/json" -H 'Authorization: Bearer ya29.CjDBAxLLuevljX0nz-0Z-D1S_2CgDMCj4CsOEhzY9q3Y0DG5Y10oLuRBV41COsMmB1s' "https://www.googleapis.com/drive/v3/changes/watch"

# Setting up a notification channel for messages about changes to a particular resource. 
# Send a POST request to the watch method for the resource.

"""
