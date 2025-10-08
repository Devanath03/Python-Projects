from __future__ import print_function
import os
import glob
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file as oauth2file, client, tools
from datetime import datetime, timedelta
import time
import io 
1,34
SCOPES = 'https://www.googleapis.com/auth/drive'
CREDENTIAL_FILE = 'D:\Python Projects\GoogleDrive\gdrive_sync_credential.json'
TOKEN_FILE = 'gdrive_sync_token.json'
FOLDER_ID = '175RfWggTCeCTBIf61mVfaicfByCvK5Fk' # Replace with your folder ID

def sync_folder(local_folder, gdrive_folder_name):
    store = oauth2file.Storage(TOKEN_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CREDENTIAL_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    drive_service = service
    # Check if the folder already exists...
    response = drive_service.files().list(q="name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false".format(name=gdrive_folder_name)).execute()
    items = response.get('files', [])
    if not items:
        # Create a new folder if it doesn't exist
        print("'{0}'' not found, create new".format(gdrive_folder_name))
        file_metadata = {
            'name': gdrive_folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    else:
        # Use the existing folder
        print("'{0}'' found".format(gdrive_folder_name))
        folder = items[0]
    folder_id = folder.get('id')
    print("folderId={0}".format(folder_id))
    # check files on gdrive
    response = drive_service.files().list(q="'{folderId}' in parents and trashed=false".format(folderId=folder_id)).execute()
    drive_filenames = {}
    for _file in response.get('files', []):
        drive_filenames[_file.get('name')] = _file.get('id')
    print("drive_filenames={0}".format(len(drive_filenames)))


    # delete files no longer exist in local
    for _file, _id in drive_filenames.items():
        if os.path.basename(_file) not in [os.path.basename(f) for f in glob.glob(os.path.join(local_folder, '*'))]:
            print("Delete '{0}', {1}".format(_file, _id))
            drive_service.files().delete(fileId=_id).execute()
        


    local_filenames = [os.path.basename(f) for f in glob.glob(os.path.join(local_folder, '*'))]

    # Delete files from local folder that are not in Google Drive
    for filename in local_filenames:
        if filename not in drive_filenames:
            local_file = os.path.join(local_folder, filename)
            print("Delete '{0}'".format(local_file))
            os.remove(local_file)
        

if __name__ == '__main__':
    local_folder = 'D:\Google Drive' # Use 'r' to specify raw string literal to avoid escaping backslashes
    gdrive_folder_name = 'Local Folder Access'
    interval_minutes = 0.1
    last_sync_time = datetime.now() - timedelta(minutes=interval_minutes)
    
    while True:
        # Check if enough time has passed since the last synchronization
        if datetime.now() - last_sync_time >= timedelta(minutes=interval_minutes):
            # Synchronize the folder
            sync_folder(local_folder, gdrive_folder_name)
            # Update the last synchronization time
            last_sync_time = datetime.now()
        # Wait for the next synchronization interval
        time.sleep(10)  # Sleep for 1 seconds before checking again