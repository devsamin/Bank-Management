from mamar_bank.wsgi import application
from vercel_wsgi import handle_request

def handler(environ, start_response):
    return handle_request(application, environ, start_response)
