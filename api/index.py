# Vercel serverless function - Flask wrapper
import sys
import os
import json
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app

def handler(request):
    """
    Vercel Python serverless function handler
    Converts Vercel request to WSGI and calls Flask app
    """
    try:
        # Extract request data - Vercel passes request as dict
        # The path from Vercel includes the full path including /api
        path = request.get('path', '/')
        method = request.get('method', 'GET')
        headers = request.get('headers', {}) or {}
        body = request.get('body', '') or ''
        query_params = request.get('queryStringParameters', {}) or {}
        
        # Debug logging (will appear in Vercel function logs)
        print(f"Handler called: method={method}, path={path}")
        
        # Build query string
        if query_params:
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
        else:
            query_string = ''
        
        # Keep the full path - Flask routes include /api prefix
        # Don't remove /api prefix since Flask expects it
        if not path:
            path = '/'
        
        # Convert body to bytes
        if isinstance(body, str):
            body_bytes = body.encode('utf-8')
        elif body is None:
            body_bytes = b''
        else:
            body_bytes = body
        
        # Normalize headers (case-insensitive)
        normalized_headers = {}
        for k, v in headers.items():
            normalized_headers[k.lower()] = v
        
        content_type = normalized_headers.get('content-type', '')
        
        # Create WSGI environment
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'SCRIPT_NAME': '',
            'QUERY_STRING': query_string,
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
        }
        
        # Add HTTP headers to environ
        for key, value in headers.items():
            if key.lower() not in ['content-type', 'content-length']:
                env_key = 'HTTP_' + key.upper().replace('-', '_')
                environ[env_key] = str(value)
        
        # Add host header
        host = headers.get('host', headers.get('Host', 'vercel'))
        environ['HTTP_HOST'] = host
        environ['SERVER_NAME'] = host.split(':')[0]
        
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
        print(f"Handler error: {error_msg}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e),
                'message': 'Internal server error'
            })
        }

