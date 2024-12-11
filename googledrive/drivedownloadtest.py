from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
import io

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def download_file(file_id, output_file):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_file, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    print("Download complete.")

# Example usage
file_id = '1Bfr7ooPTKRVZEPPwOa5VdS5BPYvXrhMr'  # Replace with the ID of the file you want to download
output_file = 'downloaded_file.txt'  # Specify the name of the downloaded file
download_file(file_id, output_file)