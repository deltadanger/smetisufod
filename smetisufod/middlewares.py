

class CorsMiddleware(object):
    def process_request(self, request):
        if request.method == 'OPTIONS' and 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response["Access-Control-Allow-Origin"] = "*"
            return response

        return None

    def process_response(self, request, response):
        if request.META.get("PATH_INFO") in ("/search", "/get_item"):
            response["Access-Control-Allow-Origin"] = "*"
        return response