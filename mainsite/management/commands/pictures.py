
import httplib2
import urllib2

from apiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

from django.core.files.temp import NamedTemporaryFile

from smetisufod.settings import DOFUS_COOKIES
from smetisufod.private_settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import logging

log = logging.getLogger(__name__)

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
CREDENTIAL_FILE = "credentials"

FOLDER_ID = "0B7K23HtYjKyBfnhYbkVyUld3YUVqSWgzWm1uMXdrMzQ0NlEwOXVUd3o0MWVYQ1ZVMlFSNms"
DRIVE_FOLDER_LINK = "http://googledrive.com/host/{folder_id}/{file_name}"
FILE_URL = "https://googledrive.com/host/{file_id}"


class PictureManager():
    def __init__(self):
        log.debug("Initialising PictureManager")
        self._service = self._get_service()
        self._images = self._build_current_list()
        log.debug("{} images already stored.".format(len(self._images)))
        
    def get_image_url(self, original_url):
        file_name = original_url.split("/")[-1]
        image_url = self._images.get(file_name)
        if not image_url:
            log.debug("Image not found, uploading {}".format(file_name))
            image_url = self._upload_image_file(original_url)
            self._images[file_name] = image_url
        
        return image_url
    
    
    def _get_credentials(self):
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
        return credentials
    
    
    def _get_service(self):
        credentials = self._get_credentials()
        # Create an httplib2.Http object and authorize it with our credentials
        http = httplib2.Http()
        http = credentials.authorize(http)
        
        # Build the drive API service object
        service = build('drive', 'v2', http=http)
        return service
    
    def _get_link_from_metadata(self, data):
        return FILE_URL.format(file_id=data["id"])
    
    def _build_current_list(self):
        response = self._service.children().list(folderId=FOLDER_ID).execute()
        image_list = response["items"]
        result = {}
        for image in image_list:
            # TODO: get all pages
            image_data = self._service.files().get(fileId=image.get("id")).execute()
            result[image_data["originalFilename"]] = self._get_link_from_metadata(image_data)
        
        return result
    
    def _upload_image_file(self, original_url):
        # Download image from dofus into a temporary file
        opener = urllib2.build_opener()
        opener.addheaders.append(("Cookie", DOFUS_COOKIES))
        resp = opener.open(original_url)
        
        temp_file = NamedTemporaryFile()
        temp_file.write(resp.read())
        
        # Upload the file to GDrive
        file_name = original_url.split("/")[-1]
        mime_type = "image/png"
        media_body = MediaFileUpload(temp_file.name, mimetype=mime_type)
        body = {
            "title": file_name,
            "mimeType": mime_type,
            "parents": [{"id": FOLDER_ID}]
        }
        
        image_data = self._service.files().insert(body=body, media_body=media_body).execute()
        temp_file.close() # Close also destroys the temp file
        
        return self._get_link_from_metadata(image_data)

if __name__ == "__main__":
    manager = PictureManager()
    print manager.get_image_url("http://staticns.ankama.com/dofus/www/game/items/200/2082.png")
    


