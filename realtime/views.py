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
from django.core.serializers import serialize
from asgiref.sync import sync_to_async, async_to_sync

# class FutureWrapper:
#     def __init__(self):
#         self.future = asyncio.Future()
# 
#     def generate(self):
#         self.future = asyncio.Future()

# async def sse(request, *args, **kwargs):

class Event(generic.View):

    future = asyncio.Event()
    a = [5]
    async def get(self, request, *args, **kwargs):
        # future = asyncio.Event()
        # @receiver(signal=signals.post_save, sender=models.TestModel)
        # def send_notification(sender, instance, created, **kwargs):
        #     print(kwargs)
        #     if created:
        #         future.set()

        async def event_stream():
            while True:
                await self.future.wait()
                model = await models.TestModel.objects.alast()
                yield "data: {}\n\n".format(model.text)
                if self.future.is_set():
                    self.future.clear()

        r = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        r['Cache-Control'] = 'no-cache'
        r['Connection'] = 'keep-alive'
        return r

    async def post(self, request, *args, **kwargs):
        print(self.a)
        self.a[0] +=1
        form = forms.TestForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                await sync_to_async(form.save)()
                self.future.set()

        context = {'form': form}
        return shortcuts.render(request, 'realtime/index.html', context=context)

def t1(request):
    print(request)
    form = forms.TestForm()

    context = {'form': form}
    return shortcuts.render(request, 'realtime/index.html', context=context)

