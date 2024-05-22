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
import pickle
from django.core.cache import cache, ConnectionProxy

# class FutureWrapper:
#     def __init__(self):
#         self.future = asyncio.Future()
# 
#     def generate(self):
#         self.future = asyncio.Future()

# async def sse(request, *args, **kwargs):

class Event(generic.View):

    # future = asyncio.Event()
    async def get(self, request, *args, **kwargs):

        # future = asyncio.Event()
        # @receiver(signal=signals.post_save, sender=models.TestModel)
        # def send_notification(sender, instance, created, **kwargs):
        #     print(kwargs)
        #     if created:
        #         future.set()

        async def event_stream():
            while True:
                # try:
                    # await asyncio.wait_for(self.future.wait(), timeout=5)
                # except:
                #     yield "data: {}\n\n".format('data lose')
                #     continue

                # print(event)
                await request.event.wait()
                model = await models.TestModel.objects.alast()
                yield "data: {}\n\n".format(model.text)

                if request.event.is_set():
                    request.event.clear()
                    request.session['event'] = None



        r = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        r['Cache-Control'] = 'no-cache'
        r['Connection'] = 'keep-alive'
        return r

    async def post(self, request, *args, **kwargs):
        form = forms.TestForm(request.POST or None)

        # print(event)

        if request.method == 'POST':
            if form.is_valid():
                await sync_to_async(form.save)()
                request.session['event'] = True
                request.event.set()

        context = {'form': form, 'id': kwargs['id']}
        return shortcuts.render(request, 'realtime/index.html', context=context)


def t1(request, *args, **kwargs):

    form = forms.TestForm()

    context = {'form': form, 'id': kwargs['id']}
    response = shortcuts.render(request, 'realtime/index.html', context=context)


    return response

