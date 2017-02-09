
from aiohttp import web

import json
import jwt

def json_error(message):
    return web.Response(
        body=json.dumps({'error': message}).encode('utf-8'),
        content_type='application/json')

def create_token(user):
    """Creates a user token storing user_id and exp time"""
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')

def parse_token(req):
    """Confirms that a token is valid"""
    auth_string_list = req.headers.get('Authorization')
    # If there is no authorization heade Raise error
    if not auth_string_list:
        raise ValueError('No Authorization found') 

    auth_string_list = auth_string_list.split()

    # Check in correct format i.e. Bearer: 39xds03lda0...
    if len(auth_string_list) == 1:
        raise ValueError('Authorization has invalid format')
    else:
        token = auth_string_list[1]
        data = jwt.decode(token, 'abcxyz123456', algorithms='HS256')
        return data

async def auth_middleware(app, handler):
    async def middleware_handler(request):
        print('checking')
        try:
            parse_token(request)
            response = await handler(request)
            return response
        except Exception as e:
            print(str(e))
            raise web.HTTPUnauthorized()

            return json_error(str(e))
    return middleware_handler

def setup_middlewares(app):
    app.middlewares.append(auth_middleware)


