import json

from channels.generic.websocket import AsyncWebsocketConsumer


class TicketConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time ticket updates.
    Each ticket has its own room: ticket_{ticket_id}
    """

    async def connect(self):
        self.ticket_id = self.scope["url_route"]["kwargs"]["ticket_id"]
        self.room_group_name = f"ticket_{self.ticket_id}"

        # Join the room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket (optional - frontend can send messages too)
    async def receive(self, text_data):
        pass  # We only broadcast from backend for now

    # Custom event handlers (called from views/signals)
    async def status_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "status_update",
                    "status": event["status"],
                    "ticket_id": event["ticket_id"],
                }
            )
        )

    async def new_comment(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "new_comment",
                    "comment": event["comment"],
                    "ticket_id": event["ticket_id"],
                }
            )
        )
