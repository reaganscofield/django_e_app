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
        await self.send({
            "type": "websocket.accept"
        })

        sender_username = "reaganscofield" # self.scope['user']
        receiver_id = self.scope['url_route']['kwargs']['receiver']
        currentUser = await self.scope_user(sender_username)
        sender_id = currentUser.id

        message_obj = await self.get_messages_obj(sender_id, receiver_id)
        room_chat = await self.room(sender_id, receiver_id)

        await self.send({
            "type": "websocket.send",
            "text": json.dumps(message_obj)
        })

    async def websocket_receive(self, event):
        get_dic = event.get("message", None)

        if get_dic is not None:
            data_parse = json.loads(get_dic)
            sender = data_parse.get("sender")
            receiver = data_parse.get("receiver")
            message = data_parse.get("message")

            request = {
                "sender": sender,
                "receiver": receiver,
                "message": message
            }
            createdObj = await self.object_create(response)

            await self.send({
                "type": "websocket.accept"
            })

            await self.send({
                "type": "websocket.send",
                "text": json.dumps(createdObj)
            })

    async def websocket_disconnect(self, event):
        print(f"event disconnected {event}")

    @database_sync_to_async
    def get_messages_obj(self, sender, receiver):
        messages = ( 
            Message.objects.filter(sender=sender).filter(receiver=receiver) | 
            Message.objects.filter(sender=receiver).filter(receiver=sender)
        )
        serializer = MessageSerializer(messages, many=True)
        return serializer.data


    @database_sync_to_async
    def object_create(self, request):
       objCreate = Message.objects.create(
           sender_id = request["sender"],
           receiver_id = request["receiver"],
           message = request["message"]
       )
       objCreate.save()

       return objCreate


    @database_sync_to_async
    def room(self, sender, receiver):
        messages = ( 
            Message.objects.filter(sender=sender).filter(receiver=receiver).count() | 
            Message.objects.filter(sender=receiver).filter(receiver=sender).count()
        )

        return messages


    @database_sync_to_async
    def scope_user(self, sender_username):
        User = Users.objects.get(username=sender_username)

        return User




    