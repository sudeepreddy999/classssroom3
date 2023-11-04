import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
online_user = 0
class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global online_user
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # self.role = self.scope["user"].role.name
        # print(self.role)
        # if(self.role != "teacher"):
        online_user += 1
        
        
        
        
        

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.send_online_user_count()
        # await self.roleTea()
        
        
        await self.accept()
        
        

        
        
    async def disconnect(self, close_code):
        global online_user
        online_user -= 1
        await self.send_online_user_count()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'message' in text_data_json:
            message = text_data_json['message']
        # print(f'Received message: {message}')
            username = text_data_json['username']
            i = text_data_json['i']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'message':message,
                    'username':username,
                    'i':i
                }
            )
        elif 'end' in text_data_json:
            end = text_data_json['end']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'end_message',
                    'end':end
                    
                }
            )
        
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        i = event['i']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'i':i
        }))
    
    async def end_message(self, event):
        end = event['end']
        

        await self.send(text_data=json.dumps({
            'end': end,
            
        }))
        
        
    async def send_online_user_count(self):
        # Send the online user count to all clients in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_count',
                'count': online_user,
            }
        )
        
    # async def roleTea(self):
    #     # Send the online user count to all clients in the room
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'user_count',
    #             'count': online_user,
    #         }
    #     )
        

    async def user_count(self, event):
        # Send the online user count to the WebSocket
        count = event['count']
        await self.send(text_data=json.dumps({'count': count}))