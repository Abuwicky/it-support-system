from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Ticket, TicketComment


@receiver(pre_save, sender=Ticket)
def store_old_status(sender, instance, **kwargs):
    """Remember the previous status so post_save can detect transitions."""
    if instance.pk:
        try:
            instance._old_status = Ticket.objects.get(pk=instance.pk).status
        except Ticket.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Ticket)
def broadcast_ticket_update(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"ticket_{instance.id}",
        {"type": "status_update", "status": instance.status, "ticket_id": instance.id},
    )

    from .tasks import send_ticket_notification

    if created:
        send_ticket_notification.delay(instance.id, "Created")
    elif instance.status == "resolved" and getattr(instance, "_old_status", None) != "resolved":
        send_ticket_notification.delay(instance.id, "Resolved")


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
