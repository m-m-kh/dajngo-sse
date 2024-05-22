# myapp/middleware.py
import asyncio
class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.session.get('event'):
            request.session['event'] = False
            request.event = asyncio.Event()
        elif request.session.get('event'):
            request.session['event'] = True
            request.event = asyncio.Event()
            request.event.set()



        response = self.get_response(request)

        return response
