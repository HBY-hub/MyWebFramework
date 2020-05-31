from werkzeug.wrappers import BaseRequest, BaseResponse
from werkzeug.exceptions import HTTPException, MethodNotAllowed, \
     NotImplemented, NotFound
from werkzeug.utils import cached_property,redirect
from werkzeug.serving import run_simple
from framework.template import Template


SECRET_KEY = '\xfa\xdd\xb8z\xae\xe0}4\x8b\xea'


class Request(BaseRequest):
    """Encapsulates a request."""

    # @cached_property
    # def client_session(self):
    #     data = self.cookies.get('session_data')
    #     if not data:
    #         return SecureCookie(secret_key=SECRET_KEY)
    #     return SecureCookie.unserialize(data, SECRET_KEY)

class Response(BaseResponse):
    """Encapsulates a response."""


class View(object):
    """Baseclass for our views."""
    def __init__(self):
        self.methods_meta = {
            'GET': self.GET,
            'POST': self.POST,
            'PUT': self.PUT,
            'DELETE': self.DELETE,
        }
    def GET(self):
        raise MethodNotAllowed()
    POST = DELETE = PUT = GET

    def HEAD(self):
        return self.GET()
    def dispatch_request(self, request, *args, **options):
        if request.method in self.methods_meta:
            return self.methods_meta[request.method](request, *args, **options)
        else:
            return '<h1>Unknown or unsupported require method</h1>'

    @classmethod
    def get_func(cls):
        def func(*args, **kwargs):
            obj = func.view_class()
            return obj.dispatch_request(*args, **kwargs)
        func.view_class = cls
        return func

class WebApp(object):
    def __init__(self):
        self.url_map = {}

    def __call__(self, environ, start_response):
        try:
            req = Request(environ)
            url = req.path
            view = self.url_map.get(url, None)
            print(view)
            if view:
                response = MyResponse()
                response = view(req,response)
            else:
                response = MyResponse('<h1>404 Source Not Found<h1>', content_type='text/html; charset=UTF-8', status=404)
        except HTTPException as e:
            response = e
        return response(environ, start_response)

    def add_cookie(self,key,value):
        pass

    def add_url_rule(self, urls):
         for url in urls:
             self.url_map[url['url']] = url['view'].get_func()

    def run(self, port=5000, ip='127.0.0.1', debug=False):
        run_simple(ip, port, self, use_debugger=debug, use_reloader=True)


def render_template(addr, content = None):
    htmlf = open('./static/'+addr, 'r', encoding="utf-8")
    htmlcont = htmlf.read()
    t = Template(htmlcont)
    return t.render(content)


def myRedirect(location):
    return redirect(location)


class MyResponse(Response):
    '''response'''