
import httplib2
import urllib2

from apiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

from django.core.files.temp import NamedTemporaryFile

from smetisufod.settings import DOFUS_COOKIES
from smetisufod.private_settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
CREDENTIAL_FILE = "credentials"

FOLDER_ID = "0B7K23HtYjKyBfnhYbkVyUld3YUVqSWgzWm1uMXdrMzQ0NlEwOXVUd3o0MWVYQ1ZVMlFSNms"
DRIVE_FOLDER_LINK = "http://googledrive.com/host/{folder_id}/{file_name}"


def _get_service():
    # Get stored credentials
    storage = Storage(CREDENTIAL_FILE)
    credentials = storage.get()
    if not credentials:
        # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, redirect_uri=REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        print "Go to the following link in your browser: " + authorize_url
        code = raw_input("Enter verification code: ").strip()
        credentials = flow.step2_exchange(code)
        storage.put(credentials)
    
    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # Build the drive API service object
    service = build('drive', 'v2', http=http)
    return service

def get_original_name(image_url):
    image_id = image_url.split("/")[-1]
    service = _get_service()
    result = service.files().get(fileId=image_id).execute()
    return result.originalFilename

def upload_image_file(dofus_url):
    file_name = dofus_url.split("/")[-1]
#     result_link = DRIVE_FOLDER_LINK.format(folder_id=FOLDER_ID, file_name=file_name)
#     if is_image_available(dofus_url):
#         return result_link
    
    # Download image from dofus into a temporary file
    opener = urllib2.build_opener()
    opener.addheaders.append(("Cookie", DOFUS_COOKIES))
    resp = opener.open(dofus_url)
    
    temp_file = NamedTemporaryFile()
    temp_file.write(resp.read())
    
    service = _get_service()
    
    # Upload the file to GDrive
    mime_type = "image/png"
    media_body = MediaFileUpload(temp_file.name, mimetype=mime_type)
    body = {
        "title": file_name,
        "mimeType": mime_type,
        "parents": [{"id": FOLDER_ID}]
    }
    
    uploaded_file = service.files().insert(body=body, media_body=media_body).execute()
    temp_file.close() # Close also destroys the temp file
    
    return uploaded_file.selfLink

if __name__ == "__main__":
#     print upload_image_file("http://staticns.ankama.com/dofus/www/game/items/200/2082.png")
#     print is_image_available("http://staticns.ankama.com/dofus/www/game/items/200/2082.png")
#     print is_image_available("http://staticns.ankama.com/dofus/www/game/items/200/0000.png")
    print get_original_name("https://www.googleapis.com/drive/v2/files/0B7K23HtYjKyBaXA3RU1lZEh6Z00")


