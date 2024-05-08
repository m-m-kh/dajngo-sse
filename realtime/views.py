import asyncio

from django import shortcuts
from django.views import generic
from . import models, forms
from django.http import JsonResponse
from django.core import serializers
import json
import time
from django.http import StreamingHttpResponse
import random
from asgiref.sync import sync_to_async
async def sse(request, *args, **kwargs):
    async def event_stream():

        while True:
            model = await sync_to_async(list)(models.TestModel.objects.all())
            for obj in model:
                yield "data: {}\n\n".format(obj.name)
                await asyncio.sleep(1)
        # i = 0
        # while True:
        #     yield f'data: {random.choice(emojis)} {i}\n\n'
        #     i += 1
        #     await asyncio.sleep(1)
    r = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    r['Cache-Control'] = 'no-cache'
    r['Connection'] = 'keep-alive'
    return r

def t1(request):
    form = forms.TestForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()


    context = {'form': form}
    return shortcuts.render(request, 'realtime/index.html', context=context)
