from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"


def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds


def update_file_content(file_id, new_content):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Build the request to update the file content
    request = service.files().update(
        fileId=file_id,
        media_body=new_content
    )

    # Execute the request
    request.execute()
    print("File content updated successfully.")


# Example usage
file_id = '1Bfr7ooPTKRVZEPPwOa5VdS5BPYvXrhMr'  # Replace with the ID of the file you want to update
new_content = 'NewData.txt'  # Replace with the new content of the file
update_file_content(file_id, new_content)