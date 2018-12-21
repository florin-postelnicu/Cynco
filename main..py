
from aiohttp import web

async def index(request):
    return web.Response(text = 'Hello Aiohttp')

def setup_routes(app):
    app.router.add_get('/', index)

app = web.Application()
setup_routes(app)
web.run_app(app, host='127.0.0.1', port=8880)

