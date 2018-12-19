
'''
Example of a Server
'''

from aiohttp import web
async def handle(request):
    name = request.match_info.get('name, "Anonymous')
    text = "Hello,  " + name

app = web.Application()
app.add_routes([web.get('/', handle), web.get('/{name}', handle)])


web.run_app(app)
