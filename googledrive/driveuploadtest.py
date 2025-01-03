from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"
PARENT_FOLDER_ID = "1GsWugTO4H1_yCqHsFdbMgmT_er5bC8hw"


def authenticate():
    creds = service_account.Credentials. from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_photo(file_path):
    creds = authenticate()
    service = build('drive','v3', credentials=creds)
    file_metadata ={
        'name':"OnlineMachines",
        'parents' : [PARENT_FOLDER_ID]
    }
    file =service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()

upload_photo("OnlineMachines.txt")