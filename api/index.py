# Vercel serverless function - Flask wrapper
import sys
import os
import json
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app

def handler(req):
    """
    Vercel serverless function handler for Flask app
    Handles both dict and object-style requests
    """
    try:
        # Handle both dict and object-style requests
        if hasattr(req, 'path'):
            # Object-style request
            path = req.path
            method = req.method
            headers = dict(req.headers) if hasattr(req, 'headers') else {}
            body = req.body if hasattr(req, 'body') else b''
            query_string = getattr(req, 'query_string', '')
        else:
            # Dict-style request
            path = req.get('path', '/')
            method = req.get('method', 'GET')
            headers = req.get('headers', {}) or {}
            body = req.get('body', '')
            query_string = req.get('queryStringParameters', {}) or {}
            if isinstance(query_string, dict):
                query_string = '&'.join([f"{k}={v}" for k, v in query_string.items()])
        
        # Remove /api prefix from path
        if path.startswith('/api'):
            path = path[4:]
        if not path:
            path = '/'
        
        # Convert body to bytes
        if isinstance(body, str):
            body_bytes = body.encode('utf-8')
        elif body is None:
            body_bytes = b''
        else:
            body_bytes = body
        
        # Get content type
        content_type = headers.get('content-type', headers.get('Content-Type', ''))
        
        # Create WSGI environment
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': query_string if isinstance(query_string, str) else '',
            'CONTENT_TYPE': content_type,
            'CONTENT_LENGTH': str(len(body_bytes)),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': BytesIO(body_bytes),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'SERVER_NAME': 'vercel',
            'SERVER_PORT': '443',
            'HTTP_HOST': headers.get('host', headers.get('Host', '')),
        }
        
        # Add headers to environ
        for key, value in headers.items():
            if key.lower() not in ['content-type', 'content-length']:
                env_key = 'HTTP_' + key.upper().replace('-', '_')
                environ[env_key] = str(value)
        
        # Response storage
        status_code = [200]
        response_headers = []
        response_body = []
        
        def start_response(status, headers_list):
            status_code[0] = int(status.split()[0])
            response_headers.extend(headers_list)
        
        # Call Flask app
        result = app(environ, start_response)
        
        # Collect response body
        for chunk in result:
            if isinstance(chunk, bytes):
                response_body.append(chunk)
            else:
                response_body.append(str(chunk).encode('utf-8'))
        
        # Convert headers to dict
        headers_dict = {}
        for header in response_headers:
            if len(header) == 2:
                headers_dict[header[0]] = header[1]
        
        # Ensure CORS headers
        if 'Access-Control-Allow-Origin' not in headers_dict:
            headers_dict['Access-Control-Allow-Origin'] = '*'
        
        # Return Vercel format
        body_str = b''.join(response_body).decode('utf-8')
        return {
            'statusCode': status_code[0],
            'headers': headers_dict,
            'body': body_str
        }
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"Error in handler: {error_msg}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'success': False, 'error': str(e), 'traceback': error_msg})
        }

