import asyncio
from aiohttp import web
from routes import setup_routes
from middlewares import setup_middlewares

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
setup_middlewares(app)
setup_routes(app)
web.run_app(app, host='127.0.0.1', port=8080)

