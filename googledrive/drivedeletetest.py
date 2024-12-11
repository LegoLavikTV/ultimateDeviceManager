from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

# Function to authenticate and build the Drive service

SCOPES = ['https://www.googleapis.com/auth/drive']
def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'service_account.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

# Function to delete files from a specific folder
def delete_files_in_folder(folder_id):
    drive_service = authenticate()
    # List all files in the folder
    results = drive_service.files().list(q=f"'{folder_id}' in parents").execute()
    items = results.get('files', [])
    # Delete each file
    if not items:
        print('No files found.')
    else:
        for item in items:
            drive_service.files().delete(fileId=item['id']).execute()
            print(f"Deleted file: {item['name']}")

# Folder ID of the folder from which you want to delete files
folder_id = '1GsWugTO4H1_yCqHsFdbMgmT_er5bC8hw'
delete_files_in_folder(folder_id)