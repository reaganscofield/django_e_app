import asyncio
import json
from django.contrib.auth import get_user_model
from .models import Users, Message
from .serializers import MessageSerializer, SerializersUsers
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async



from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("event connected :: ", event)
    

        sender_id = self.scope['url_route']['kwargs']['sender']
        receiver_id = self.scope['url_route']['kwargs']['receiver']

        message_obj = await self.get_messages_obj(sender_id, receiver_id

        #room_chat = f""
        
        await self.send({
            "type": "websocket.accept"
        })

        await self.send({
            "type": "websocket.send",
            "message":  message_obj #"Whatever Message to be send"
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

        await self.send({
            "type": "websocket.accept"
        })

        await self.send({
            "type": "websocket.send",
            "message": json.dumps(response)
        })

    async def websocket_disconnect(self, event):
        print("event disconnected :: ", event)


    @database_sync_to_async
    def get_messages_obj(self, sender_id, receiver_id):
        messages = ( 
            Message.objects.filter(sender_id=sender).filter(receiver_id=receiver) | 
            Message.objects.filter(sender_id=receiver).filter(receiver_id=sender)
        )
        serializer = MessageSerializer(messages, many=True)
        return  JsonResponse(serializer.data, safe=False)   # messages




    