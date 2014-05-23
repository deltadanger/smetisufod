import os.path as path, logging

log = logging.getLogger(__name__)

class WebCache():
    def __init__(self, opener, force_refresh=False):
        self.opener = opener
        self.force_refresh = force_refresh
        
    def get(self, url, force_refresh=False):
        content = self._get_from_local(url)
        if content and not force_refresh and not self.force_refresh:
            log.debug("Getting resource from local: " + url)
            
        else:
            log.debug("Getting from remote source: " + url)
            content = self.opener.open(url).read()
            self._save_to_local(url, content)
        
        return content
        
    def _get_from_local(self, url):
        file = self._get_name_from_url(url)
        
        if path.isfile(file):
            with open(file, "r") as f:
                content = "".join(f.readlines())
            
            return content
        
        return None
    
    def _save_to_local(self, url, content):
        file = self._get_name_from_url(url)
        
        with open(file, "w") as f:
            f.write(content)
        
    
    def _get_name_from_url(self, url):
        filename = url.replace(":", "").replace("/", "-").replace("?", "$")
        return path.join(path.dirname(path.abspath(__file__)), "cache", filename)

