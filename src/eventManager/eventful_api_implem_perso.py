import hashlib
import urllib.parse

import httplib2
import simplejson

__all__ = ['APIError', 'API']


class APIError(Exception):
    pass


class API:
    def __init__(self, app_key, server='api.eventful.com', cache=None):
        self.app_key = app_key
        self.server = server
        self.http = httplib2.Http(cache)

    def call(self, method, **args):
        args['app_key'] = self.app_key
        if hasattr(self, 'user_key'):
            args['user'] = self.user # pragma: no cover
            args['user_key'] = self.user_key # pragma: no cover
        args = urllib.parse.urlencode(args)
        url = "http://%s/json/%s?%s" % (self.server, method, args)

        response, content = self.http.request(url, "GET")

        status = int(response['status'])
        if status == 200:
            try:
                return simplejson.loads(content)
            except ValueError: # pragma: no cover
                raise APIError("Unable to parse API response!") # pragma: no cover
        elif status == 404:
            raise APIError("Method not found: %s" % method)
        else: # pragma: no cover
            raise APIError("Non-200 HTTP response status: %s" % response['status']) # pragma: no cover

    def login(self, user, password): # pragma: no cover
        nonce = self.call('/users/login')['nonce']
        response = hashlib.md5.new(nonce + ':'
                           + hashlib.md5.new(password).hexdigest()).hexdigest()
        login = self.call('/users/login', user=user, nonce=nonce,
                          response=response)
        self.user_key = login['user_key']
        self.user = user
        return user
