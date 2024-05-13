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
from django.dispatch import receiver
from django.db.models import signals

# class FutureWrapper:
#     def __init__(self):
#         self.future = asyncio.Future()
# 
#     def generate(self):
#         self.future = asyncio.Future()
async def sse(request, *args, **kwargs):
    future = asyncio.Event()

    @receiver(signal=signals.post_save, sender=models.TestModel)
    def send_notification(sender, instance, created, **kwargs):
        if created:
            future.set()

    async def event_stream():
        while True:
            await future.wait()
            model = await models.TestModel.objects.alast()
            yield "data: {}\n\n".format(model.name)
            if future.is_set():
                future.clear()




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

