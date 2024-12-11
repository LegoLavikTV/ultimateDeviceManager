import socket
import time
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
import io
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"
PARENT_FOLDER_ID = "1GsWugTO4H1_yCqHsFdbMgmT_er5bC8hw"
file_id = '1Bfr7ooPTKRVZEPPwOa5VdS5BPYvXrhMr'  # Replace with the ID of the file you want to download
output_file = 'OnlineMachines.txt'  # Specify the name of the downloaded file


def get_ip_address():
    # Get the IP address of the local machine
    return socket.gethostbyname(socket.gethostname())


def get_pc_name():
    # Get the name of the local machine
    return socket.gethostname()








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



def modify_text_file(file_path, new_content):
    with open(file_path, 'w') as file:
        file.write(new_content)
        file.close()

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    return str(file_contents)


# Main loop
while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pc_name = get_pc_name()
    ip_address = get_ip_address()
    pc_info = f"<PC-ONLINE> NUMBER=3; IP_ADDRESS={ip_address}; PC_NAME={pc_name}; LAST_TIME_ACTIVE={current_time}"
    try: os.remove(output_file)
    except Exception: pass
    try: os.remove("NewData.txt")
    except Exception:pass
    download_file(file_id, output_file)
    print(f"<PC-ONLINE> NUMBER=3; IP_ADDRESS={ip_address}; PC_NAME={pc_name}; LAST_TIME_ACTIVE={current_time}")
    file_path = 'OnlineMachines.txt'  # Specify the path to your text file
    file_contents = read_text_file(file_path)
    modify_text_file("NewData.txt", f"{file_contents}\n"f"{pc_info}")
    update_file_content(file_id, "NewData.txt")
    time.sleep(116)