
import httplib2

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from smetisufod.private_settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from googleapiclient.http import MediaFileUpload
import urllib2
from smetisufod.settings import DOFUS_COOKIES
from django.core.files.temp import NamedTemporaryFile
from oauth2client.file import Storage


# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
CREDENTIAL_FILE = "credentials"

FOLDER_ID = "0B7K23HtYjKyBfnhYbkVyUld3YUVqSWgzWm1uMXdrMzQ0NlEwOXVUd3o0MWVYQ1ZVMlFSNms"
DRIVE_FOLDER_LINK = "http://googledrive.com/host/{folder_id}/{file_name}"

def upload_image_file(dofus_url):
    # Download image from dofus static into a temporary file
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', DOFUS_COOKIES))
    
    file_name = dofus_url.split('/')[-1]
    resp = opener.open(dofus_url)
    BUFFER_SIZE = 8192
    
    temp_file = NamedTemporaryFile()
    
    buff = resp.read(BUFFER_SIZE)
    while buff:
        temp_file.write(buff)
        buff = resp.read(BUFFER_SIZE)
    
    # Get stored credentials
    storage = Storage(CREDENTIAL_FILE)
    credentials = storage.get()
    if not credentials:
        # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, redirect_uri=REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        print 'Go to the following link in your browser: ' + authorize_url
        code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)
        storage.put(credentials)
    
    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # Build the drive API service object
    service = build('drive', 'v2', http=http)
    
    # Upload the file to GDrive
    mime_type = "image/png"
    media_body = MediaFileUpload(temp_file.name, mimetype=mime_type)
    body = {
        "title": file_name,
        'mimeType': mime_type,
        'parents': [{'id': FOLDER_ID}]
    }
    
    service.files().insert(body=body, media_body=media_body).execute()
    temp_file.close() # Close also destroys the temp file
    
    return DRIVE_FOLDER_LINK.format(folder_id=FOLDER_ID, file_name=file_name)

if __name__ == "__main__":
    print upload_image_file("http://staticns.ankama.com/dofus/www/game/items/200/2082.png")
