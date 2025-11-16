# Vercel serverless function - Simple Flask wrapper
import sys
import os
import json
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app

def handler(request):
    # Extract path from request URL
    path = request.path
    if path.startswith('/api'):
        path = path[4:]  # Remove /api prefix
    
    # Create WSGI environment
    environ = {
        'REQUEST_METHOD': request.method,
        'PATH_INFO': path or '/',
        'QUERY_STRING': request.query_string or '',
        'CONTENT_TYPE': request.headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(request.body or b'')),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(request.body or b''),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers
    for key, value in request.headers.items():
        key = 'HTTP_' + key.upper().replace('-', '_')
        environ[key] = value
    
    # Response storage
    status_code = [200]
    response_headers = []
    response_body = []
    
    def start_response(status, headers):
        status_code[0] = int(status.split()[0])
        response_headers.extend(headers)
    
    # Call Flask app
    result = app(environ, start_response)
    
    # Collect response body
    for chunk in result:
        response_body.append(chunk)
    
    # Return Vercel format
    return {
        'statusCode': status_code[0],
        'headers': dict(response_headers),
        'body': b''.join(response_body).decode('utf-8')
    }

