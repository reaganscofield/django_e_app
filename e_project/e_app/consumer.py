import asyncio
import json
from django.contrib.auth import get_user_model
from .models import Users, Message
from .serializers import MessageSerializer, SerializersUsers
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from django.http.response import JsonResponse

# from channels.layers import get_channel_layer

# channel_layer = get_channel_layer()


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("event connected :: ", event)

        await self.send({
            "type": "websocket.accept"
        })

    
        #sender_id = self.scope['url_route']['kwargs']['sender']
        receiver_id = self.scope['url_route']['kwargs']['receiver']
        sender_id =  '152ceaa2-16f7-4817-a6f3-dac3a2a5ee1e' #self.scope['user']

        print(" rrrr ", receiver_id)
       

        

        message_obj = await self.get_messages_obj(sender_id, receiver_id)

        print(message_obj)


        # print("Obj get ", message_obj)

        #room_chat = f""
        

        
        await self.send({
            "type": "websocket.send",
            "text": json.dumps(message_obj) 
        })

    
    async def websocket_receive(self, event):
        #remember send a json object in client 
        print("event receive :: ", event)

        get_dic = event.get("message", None)

        if get_dic is not None:

            data_parse = json.loads(get_dic)

            sender = data_parse.get("sender")
            receiver = data_parse.get("receiver")
            message = data_parse.get("message")


            response = {
                "sender": sender,
                "receiver": receiver,
                "message": message
            }

            self.object_create(response)

            await self.send({
                "type": "websocket.accept"
            })

            await self.send({
                "type": "websocket.send",
                "text": json.dumps(response)
            })




    async def websocket_disconnect(self, event):
        print("event disconnected :: ", event)


    @database_sync_to_async
    def get_messages_obj(self, sender, receiver):
        messages = ( 
            Message.objects.filter(sender=sender).filter(receiver=receiver) | 
            Message.objects.filter(sender=receiver).filter(receiver=sender)
        )
        serializer = MessageSerializer(messages, many=True)
        return  JsonResponse(serializer.data, safe=False)   # messages

    @database_sync_to_async
    def object_create(self, request):
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)




    