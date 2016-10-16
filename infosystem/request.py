import flask

class Request(flask.Request):

    @property
    def method(self):
        return self.environ['REQUEST_METHOD']

    @property
    def url(self):
        path_info = flask.request.environ['PATH_INFO'].rstrip('/')
        path_bits = ['<id>' if check_uuid4(i) else i for i in original_path.split('/')]
        return '/'.join(path_bits)
    
    @property
    def token(self):
        return flask.request.headers.get('token')
