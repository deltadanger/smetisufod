import os.path as path, logging

log = logging.getLogger(__name__)

class WebCache():
    def __init__(self, opener, use_cache=True):
        self.opener = opener
        self.use_cache = use_cache
        
    def get(self, url, use_cache=True):
        use_cache = use_cache and self.use_cache
        content = self._get_from_local(url)
        if content and use_cache:
            log.debug("Getting resource from local: " + url)
            
        else:
            log.debug("Getting from remote source: " + url)
            content = self.opener.open(url).read()
            if use_cache:
                self._save_to_local(url, content)
        
        return content
        
    def _get_from_local(self, url):
        local_file = self._get_name_from_url(url)
        
        if path.isfile(local_file):
            with open(local_file, "r") as f:
                content = "".join(f.readlines())
            
            return content
        
        return None
    
    def _save_to_local(self, url, content):
        local_file = self._get_name_from_url(url)
        
        with open(local_file, "w") as f:
            f.write(content)
        
    
    def _get_name_from_url(self, url):
        filename = url.replace(":", "").replace("/", "-").replace("?", "$")
        return path.join(path.dirname(path.abspath(__file__)), "cache", filename)

