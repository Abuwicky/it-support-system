from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Ticket


@shared_task
def send_ticket_notification(ticket_id, action):
    """
    Send email when a ticket is created, assigned, or resolved.
    """
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return

    subject = f"IT Support Ticket #{ticket.id} - {action}"
    message = f"""
Hello,

Ticket #{ticket.id}: {ticket.title}
Status: {ticket.get_status_display()}
Priority: {ticket.get_priority_display()}

Created by: {ticket.created_by.get_full_name() or ticket.created_by.username}

View ticket: http://your-frontend-url/tickets/{ticket.id}   # ← Update later with Next.js URL

Thank you,
IT Support Team
"""

    # Send to the person who created the ticket + the assigned person
    recipients = [ticket.created_by.email]
    if ticket.assigned_to and ticket.assigned_to.email:
        recipients.append(ticket.assigned_to.email)

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
