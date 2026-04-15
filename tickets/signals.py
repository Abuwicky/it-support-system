from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ticket, TicketComment


@receiver(post_save, sender=Ticket)
def broadcast_ticket_update(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"ticket_{instance.id}",
        {"type": "status_update", "status": instance.status, "ticket_id": instance.id},
    )


@receiver(post_save, sender=TicketComment)
def broadcast_new_comment(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"ticket_{instance.ticket.id}",
            {
                "type": "new_comment",
                "comment": instance.message[:100],
                "ticket_id": instance.ticket.id,
            },
        )
